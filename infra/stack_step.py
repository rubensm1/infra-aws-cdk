import os
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from .application.constants import get_env
from .resources.utils import pascal_case


class StackStep(Stack):
    vpc: ec2.Vpc
    CONSTANTS = get_env()

    def __init__(
        self, scope: Construct, vpc: ec2.Vpc, **kwargs
    ) -> None:
        super().__init__(scope, f"Deploy{pascal_case(self.CONSTANTS.APP_NAME)}{self.get_step_name()}", **kwargs)
        self.vpc = vpc
        self.execute()

    def execute(self) -> None:
        raise NotImplementedError
    
    def get_step_name(self) -> str:
        raise NotImplementedError
