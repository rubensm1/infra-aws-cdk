import os

import aws_cdk as cdk
from application.constants import (
    APP_NAME,
    REP_DIR,
    GIT_REPOSITORY,
    DEV_VPC_ID,
    DEV_GITHUB_CONNECTION_UUID,
    DEV_TRACKING_BRANCH,
    HOM_ACCOUNT_NUMBER,
    HOM_VPC_ID,
    HOM_GITHUB_CONNECTION_UUID,
    HOM_TRACKING_BRANCH,
    PRD_ACCOUNT_NUMBER,
    PRD_VPC_ID,
    PRD_GITHUB_CONNECTION_UUID,
    PRD_TRACKING_BRANCH,
)

acc_number = os.environ["CDK_DEFAULT_ACCOUNT"]
acc_region = os.environ["CDK_DEFAULT_REGION"]

ENV_FILE_DEFAULT = ".env"
ENV_DIR = "../"


def read_env_file(env_file: str) -> dict:
    this_dir = os.path.dirname(__file__)

    with open(os.path.abspath(os.path.join(this_dir, ENV_DIR, env_file))) as fd:
        data = fd.read()

    env_pairs = {}
    for line in data.split("\n"):
        if line and not line.startswith("#"):
            key, value = line.split("=", 1)
            env_pairs[key] = value

    return env_pairs


class BaseEnv:

    ENV: cdk.Environment
    APP_NAME: str
    REP_DIR: str
    GIT_REPOSITORY: str
    TYPE: str
    VPC_ID: str
    GITHUB_CONNECTION_ARN: str
    TRACKING_BRANCH: str

    def __init__(self):
        self.ENV = cdk.Environment(
            account=acc_number,
            region=acc_region,
        )
        self.APP_NAME = APP_NAME
        self.REP_DIR = REP_DIR
        self.GIT_REPOSITORY = GIT_REPOSITORY
        environment = read_env_file(env_file=f"{ENV_FILE_DEFAULT}.common")
        self.__dict__.update(environment)

    def to_dict(self):
        d = vars(self)
        d.pop("ENV")
        return d


class Homolog(BaseEnv):
    def __init__(self):
        super().__init__()
        self.TYPE = "hom"
        self.VPC_ID = HOM_VPC_ID
        self.GITHUB_CONNECTION_ARN = f"arn:aws:codestar-connections:{acc_region}:{acc_number}:connection/{HOM_GITHUB_CONNECTION_UUID}"
        self.TRACKING_BRANCH = HOM_TRACKING_BRANCH
        environment = read_env_file(env_file=f"{ENV_FILE_DEFAULT}.hom")
        self.__dict__.update(environment)


class Production(BaseEnv):
    def __init__(self):
        super().__init__()
        self.TYPE = "prd"
        self.VPC_ID = PRD_VPC_ID
        self.GITHUB_CONNECTION_ARN = f"arn:aws:codestar-connections:{acc_region}:{acc_number}:connection/{PRD_GITHUB_CONNECTION_UUID}"
        self.TRACKING_BRANCH = PRD_TRACKING_BRANCH
        environment = read_env_file(env_file=f"{ENV_FILE_DEFAULT}.prd")
        self.__dict__.update(environment)


class Development(BaseEnv):
    def __init__(self):
        super().__init__()
        self.TYPE = "dev"
        self.VPC_ID = DEV_VPC_ID
        self.GITHUB_CONNECTION_ARN = f"arn:aws:codestar-connections:{acc_region}:{acc_number}:connection/{DEV_GITHUB_CONNECTION_UUID}"
        self.TRACKING_BRANCH = DEV_TRACKING_BRANCH
        environment = read_env_file(env_file=f"{ENV_FILE_DEFAULT}.dev")
        self.__dict__.update(environment)


def get_env():
    if acc_number == HOM_ACCOUNT_NUMBER:
        return Homolog()
    elif acc_number == PRD_ACCOUNT_NUMBER:
        return Production()
    else:
        return Development()
