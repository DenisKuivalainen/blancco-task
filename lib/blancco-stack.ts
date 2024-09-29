import { Stack, StackProps, Duration } from "aws-cdk-lib";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as path from "path";
import { Construct } from "constructs";
import * as apigateway from "aws-cdk-lib/aws-apigateway";
import * as secretsmanager from "aws-cdk-lib/aws-secretsmanager";
import * as eventsources from "aws-cdk-lib/aws-lambda-event-sources";
import * as sqs from "aws-cdk-lib/aws-sqs";

export class BlanccoStack extends Stack {
  constructor(
    scope: Construct,
    id: string,
    props: { stage: string } & StackProps
  ) {
    super(scope, id, props);
    const stage = props.stage;

    //#region Core config
    const devicesTable = new dynamodb.Table(this, "DevicesTable", {
      partitionKey: { name: "id", type: dynamodb.AttributeType.STRING },
      tableName: `blancco-${stage}-devices-table`,
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
      stream: dynamodb.StreamViewType.NEW_IMAGE,
    });

    const statisticsTable = new dynamodb.Table(this, "StatisticsTable", {
      partitionKey: { name: "type", type: dynamodb.AttributeType.STRING },
      sortKey: { name: "value", type: dynamodb.AttributeType.STRING },
      tableName: `blancco-${stage}-statistics-table`,
      billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
    });

    const deviceStatisticsQueue = new sqs.Queue(this, "DeviceQueue", {
      queueName: `blancco-${stage}-device-statistics-queue.fifo`,
      fifo: true,
      contentBasedDeduplication: true,
    });

    const apiKeySecret = secretsmanager.Secret.fromSecretNameV2(
      this,
      "ApiKeySecret",
      `blancco-${stage}-api-key`
    );
    //#endregion

    //#region API gateway and related config
    const authorizerFunction = new lambda.Function(this, "AuthorizerFunction", {
      functionName: `blancco-${stage}-authorizer`,
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: "functions.authorizer.handler",
      code: lambda.Code.fromAsset(path.join(__dirname, "../src")),
      environment: {
        API_KEY_SECRET_ARN: apiKeySecret.secretArn,
      },
    });
    apiKeySecret.grantRead(authorizerFunction);

    const uploadDevicesFunction = new lambda.Function(
      this,
      "UploadDevicesFunction",
      {
        functionName: `blancco-${stage}-upload-devices`,
        runtime: lambda.Runtime.PYTHON_3_9,
        handler: "functions.upload_devices.handler",
        code: lambda.Code.fromAsset(path.join(__dirname, "../src")),
        environment: {
          DEVICES_TABLE: devicesTable.tableName,
        },
      }
    );
    devicesTable.grantReadWriteData(uploadDevicesFunction);

    const getDeviceStatisticsFunction = new lambda.Function(
      this,
      "GetDeviceStatisticsFunction",
      {
        functionName: `blancco-${stage}-get-device-statistics`,
        runtime: lambda.Runtime.PYTHON_3_9,
        handler: "functions.get_device_statistics.handler",
        code: lambda.Code.fromAsset(path.join(__dirname, "../src")),
        environment: {
          STATISTICS_TABLE: statisticsTable.tableName,
        },
      }
    );
    statisticsTable.grantReadData(getDeviceStatisticsFunction);

    const apiGateway = new apigateway.RestApi(this, "ApiGateway", {
      restApiName: `blancco-${stage}`,
      deployOptions: {
        stageName: stage,
      },
    });

    const authorizer = new apigateway.RequestAuthorizer(
      this,
      "LambdaAuthorizer",
      {
        handler: authorizerFunction,
        identitySources: [apigateway.IdentitySource.header("Authorization")],
        resultsCacheTtl: Duration.seconds(0),
      }
    );

    const devicesResource = apiGateway.root.addResource("devices");

    devicesResource.addMethod(
      "POST",
      new apigateway.LambdaIntegration(uploadDevicesFunction),
      {
        authorizer: authorizer,
        authorizationType: apigateway.AuthorizationType.CUSTOM,
      }
    );

    devicesResource
      .addResource("statistics")
      .addMethod(
        "GET",
        new apigateway.LambdaIntegration(getDeviceStatisticsFunction),
        {
          authorizer: authorizer,
          authorizationType: apigateway.AuthorizationType.CUSTOM,
        }
      );
    //#endregion

    //#region Dynamodb stream
    const deviceStatisticsStreamFunction = new lambda.Function(
      this,
      "DeviceStatisticsStreamFunction",
      {
        functionName: `blancco-${stage}-device-statistics-stream`,
        runtime: lambda.Runtime.PYTHON_3_9,
        handler: "functions.device_statistics_stram.handler",
        code: lambda.Code.fromAsset(path.join(__dirname, "../src")),
        environment: {
          QUEUE_URL: deviceStatisticsQueue.queueUrl,
        },
      }
    );
    deviceStatisticsQueue.grantSendMessages(deviceStatisticsStreamFunction);

    const streamEventSource = new eventsources.DynamoEventSource(devicesTable, {
      startingPosition: lambda.StartingPosition.LATEST,
      batchSize: 10,
      filters: [
        lambda.FilterCriteria.filter({
          eventName: lambda.FilterRule.isEqual("INSERT"),
        }),
      ],
    });
    deviceStatisticsStreamFunction.addEventSource(streamEventSource);
    //#endregion

    //#region SQS stream
    const deviceStatesticsQueueFunction = new lambda.Function(
      this,
      "DeviceStatesticsQueueFunction",
      {
        functionName: `blancco-${stage}-device-statistics-queue`,
        runtime: lambda.Runtime.PYTHON_3_9,
        handler: "functions.device_statistics_queue.handler",
        code: lambda.Code.fromAsset(path.join(__dirname, "../src")),
        environment: {
          STATISTICS_TABLE: statisticsTable.tableName,
        },
      }
    );
    deviceStatisticsQueue.grantConsumeMessages(deviceStatesticsQueueFunction);
    statisticsTable.grantFullAccess(deviceStatesticsQueueFunction);

    const queueEventSource = new eventsources.SqsEventSource(
      deviceStatisticsQueue,
      {
        batchSize: 10,
      }
    );
    deviceStatesticsQueueFunction.addEventSource(queueEventSource);
    //#endregion
  }
}
