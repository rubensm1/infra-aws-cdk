# Infra AWS CDK

### Installation Steps:

1. First, create a GitHub Connection that has access to your project's Git repository:  
https://us-east-1.console.aws.amazon.com/codesuite/settings/connections

The created connection will have an ARN similar to this:  
`arn:aws:codestar-connections:us-east-1:123456789000:connection/1a2b3c4d-5e6f-7890-1a2b-3c4d5e6f7890`  
Save the final value (`1a2b3c4d-5e6f-7890-1a2b-3c4d5e6f7890` in this example) to be used shortly.

2. Edit the file `infra/aws/application/constants.py`, updating the general variables and those related to your AWS account and deployment target (development/staging/production).  
In the first three lines (general variables):
Change the first line (`APP_NAME`) with your project name
The second (`REP_DIR`) contains the name of the folder where your project source code will be, but if it is all in the root, leave it blank ("")
On the third line (`GIT_REPOSITORY`), should contain the name of your Git repository.  

Now let’s suppose you want to deploy only to a test/development AWS account. In this case, look at lines 5, 6, and 7:  
On line 5, the variable `DEV_VPC_ID` should contain the ID of the VPC where your project infrastructure will be installed. Let's suppose it's: `vpc-090bfb252383707aa`  
On line 6, the variable `DEV_GITHUB_CONNECTION_UUID` is the final part of the GitHub Connection ARN (step 1), in this case: `1a2b3c4d-5e6f-7890-1a2b-3c4d5e6f7890`  
On line 7, the variable `DEV_TRACKING_BRANCH` is the repository branch the AWS CI/CD pipeline will track to obtain the source code for deployment. Here, we’ll keep `dev`, but it could be any valid branch name.

Thus, the file would look like this:

```python
APP_NAME = "infra-cdk"
REP_DIR = "repositories"
GIT_REPOSITORY = "rubensm1/infra-aws-cdk"

DEV_VPC_ID = "vpc-090bfb252383707aa"
DEV_GITHUB_CONNECTION_UUID = "1a2b3c4d-5e6f-7890-1a2b-3c4d5e6f7890"
DEV_TRACKING_BRANCH = "dev"

HOM_ACCOUNT_NUMBER = "000000000000"
HOM_VPC_ID = "vpc-00000000000000000"
HOM_GITHUB_CONNECTION_UUID = "00000000-0000-0000-0000-000000000000"
HOM_TRACKING_BRANCH = "homolog"

PRD_ACCOUNT_NUMBER = "111111111111"
PRD_VPC_ID = "vpc-11111111111111111"
PRD_GITHUB_CONNECTION_UUID = "11111111-1111-1111-1111-111111111111"
PRD_TRACKING_BRANCH = "main"
```

These update rules also apply to the other environments. The difference is that staging/production also have the `..._ACCOUNT_NUMBER` variable referring to your AWS Account ID.  
There is no `DEV_ACCOUNT_NUMBER` because the code always assumes development as default. But if there were one, in this example it would be `123456789000`.

3. With your terminal at the root of the project, run the following commands (assuming `node` and `python` is installed...):

```bash
cd infra/aws
npm install -g aws-cdk
curl -sSL https://install.python-poetry.org | python3 -
# replace <home-dir> by your home directory, for example '/home/myuser/.local/bin:$PATH'
export PATH="/<home-dir>/.local/bin:$PATH"
poetry --version
poetry env activate
poetry install
# run this next line only if you have not yet run cdk bootstrap on your aws account
cdk bootstrap --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess
cdk synth
cdk deploy
```

If successful, a CodePipeline will be created to install your system on AWS.
