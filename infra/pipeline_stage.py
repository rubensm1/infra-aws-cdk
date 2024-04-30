from aws_cdk import Stage
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
from resources.utils import pascal_case
from resources.deploy_step import DeployStepStack


class PipelineStage(Stage):
    step: DeployStepStack

    def __init__(
        self,
        scope: Construct,
        env: object,
        stack_step,
        step_name: str,
        vpc: ec2.Vpc = None,
        **kwargs,
    ):
        super().__init__(
            scope, f"Deploy{pascal_case(env.APP_NAME)}{step_name}", **kwargs
        )

        self.step = stack_step(
            self,
            f"{pascal_case(env.APP_NAME)}{step_name}",
            env=env,
            vpc=vpc,
        )
