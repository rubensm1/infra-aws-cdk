#!/usr/bin/env python3
import aws_cdk as cdk
from environment import get_env
from infra_stack import InfraStack

CONSTANTS = get_env()

app = cdk.App()

InfraStack(app, f"{CONSTANTS.APP_NAME}InfraStack", env=CONSTANTS)

app.synth()
