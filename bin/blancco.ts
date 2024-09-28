#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { BlanccoStack } from "../lib/blancco-stack";

const stage = process.env.STAGE || "dev";

const app = new cdk.App();
new BlanccoStack(app, `${stage}-blancco-stack`, {
  stage,
  env: {
    region: process.env.REGION || "eu-central-1",
  },
});
