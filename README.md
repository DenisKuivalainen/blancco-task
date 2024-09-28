# Scalable Backend Solution for Data Ingestion and Processing

This project presents a comprehensive and scalable backend solution designed for efficient data ingestion and processing. Utilizing the power of the AWS Cloud Development Kit (CDK) along with TypeScript for Infrastructure as Code (IaC) and Python for business logic implementation, this solution is engineered to ensure seamless performance and adaptability.

## Key Features

- **Infrastructure as Code**: Built using AWS CDK and TypeScript, enabling automated and reproducible infrastructure management.
- **Cost Efficiency**: Optimized use of AWS services to minimize costs while maximizing performance.
- **Scalability**: Designed to effortlessly scale with increasing data loads and user demands.
- **Reliability**: Leveraging AWS's robust ecosystem to ensure high availability and fault tolerance.

## Deployment Instructions

To deploy this solution, follow the steps below:

#### Install Dependencies

Run the following command to install the necessary dependencies:

```bash
npm install
```

#### Configure AWS Credentials

Ensure that your AWS credentials are configured properly to allow the CDK to deploy resources

```bash
aws configure
```

#### Deploy the Application

Execute the deployment command

```bash
npm run deploy:dev
```

## Data Population

After deployment, you'll need to populate the database with some initial data. Follow these steps

#### Create a `.env` File

Create a file named `.env` in your project root directory and add the following content

```plaintext
URL=https://el1hrhmcsl.execute-api.eu-central-1.amazonaws.com/dev/
API_KEY=provided_api_key
```

#### Fill the Database

Run the script to populate the database

```bash
npm run fill
```

## Statistics Retrieval

To obtain statistics from the application, make a GET request to the following endpoint

```plaintext
GET https://el1hrhmcsl.execute-api.eu-central-1.amazonaws.com/dev/devices/statistics
```

Ensure you set the `Authorization` header with the provided API key.

### Requirements

To successfully run this project, the following software versions are required:

- Node.js: v18
- npm: v8
- Python: v3.8
