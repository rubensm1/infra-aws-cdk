import os
import pytest
from aws_cdk import aws_ec2 as ec2
import aws_cdk as core


os.environ["CDK_DEFAULT_ACCOUNT"] = "123456789012"
os.environ["CDK_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def env():
    from environment import get_env

    return get_env()


@pytest.fixture
def app():
    return core.App()
