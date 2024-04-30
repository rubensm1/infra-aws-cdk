import os
from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from abc import abstractmethod


class DeployStepStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        env: object,
        vpc: ec2.Vpc = None,
        **kwargs
    ):
        super().__init__(scope, construct_id, env=env.ENV)
        self.env = env
        if vpc is None and env is not None and hasattr(env, "VPC_ID"):
            self.vpc = ec2.Vpc.from_lookup(
                self,
                "ImportVPC",
                vpc_id=env.VPC_ID,
            )
        else:
            self.vpc = vpc
        self.deploy()

    @abstractmethod
    # must be anoted with @staticmethod in subclasses
    def step_name(self) -> str:
        pass

    @abstractmethod
    def deploy(self) -> None:
        pass
