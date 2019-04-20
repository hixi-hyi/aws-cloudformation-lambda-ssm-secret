# cfn-lambda-ssm-secret
## Description
The `cfn-lambda-ssm-secret` function create a secret value and put to [AWS::SSM::Parameter](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html)

## When do you use it
* Using `MasterUserPassword` of [AWS::RDS::DBCluster](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masteruserpassword)
* Want to put secret for application such as `BasicAuthentication`

## Deploy
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#deploy)

## Usage
```
Resources:
  Secret:
    Type: Custom::SsmSecret
    Properties:
      ServiceToken: !ImportValue cfn-lambda-ssm-secret:LambdaArn
      Name: /demo/cfn-lambda/ssm-secret/secret
Outputs:
  OutputSecret:
    Value: !GetAtt Secret.Secret
```
## Parameters
### Name
- [Docs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ssm-parameter.html#cfn-ssm-parameter-name)
- ***Required:*** Yes
- ***Update requires:*** Replacement

### Pattern
- Character pattern to create a secret string.
- *Default*: abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
- *Required*: No
- *Update requires*: No interruption

### Length
- Character length to create a secret string.
- *Default*: 32
- *Required*: No
- *Update requires*: No interruption

### Policies.Creation
- The policies are used by creation phase of AWS CloudFormation.
- Support values:
  - UseIfExists
    - If ssm parameter already exists, this function use this value.
  - Overwrite
    - If ssm parameter already exists, this function overwrite value.
- *Required*: No
- *Update requires*: No interruption

### Policies.Update
- The policies are user by update phase of AWS CloudFormation.
- Support values:
  - Retain
    - Do not update the value in any case, Even if the `Pattern` or `Length` has changed.
- *Required*: No
- *Update requires*: No interruption

### Policies.Deletion
- The policies are user by deletion phase of AWS CloudFormation.
- Support values:
  - Retain
    - Do not delete the value of `SSM::Parameter`.
  - IgnoreError
    - Ignore same error.
- *Required*: No
- *Update requires*: No interruption


## Contributing
[See here](https://github.com/hixi-hyi/aws-cloudformation-lambda#contributing)
