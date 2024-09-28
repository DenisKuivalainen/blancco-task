STAGE="$1"
export STAGE=$STAGE

cdk synth
cdk deploy --require-approval never

STACK_NAME="$STAGE-blancco-stack"
API_URL=$(aws cloudformation describe-stacks --stack-name "$STACK_NAME" \
  --query "Stacks[0].Outputs[?contains(OutputKey, 'ApiGateway')].OutputValue" \
  --output text)
REGEXP="https://[^ ]*\.execute-api\.[^ ]*\.amazonaws\.com/$STAGE/"
sed -i.bak "s|${REGEXP}|${API_URL}|g" "./README.md"
rm "./README.md.bak"