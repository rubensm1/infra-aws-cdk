# Infra AWS CDK

Create a github connection
https://us-east-1.console.aws.amazon.com/codesuite/settings/connections

```
brew install node
npm install -g aws-cdk
cd infra
pip install -r requirements.txt
python3 -m venv .venv
curl -sSL https://install.python-poetry.org | python3 -
export PATH="/<home-dir>/.local/bin:$PATH"
poetry --version
poetry install
poetry shell
aws sso login --profile <profile>
cdk bootstrap --profile <profile> --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess
cdk synth --profile <profile>
cdk deploy --profile <profile>
```