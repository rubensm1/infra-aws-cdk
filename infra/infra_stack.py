import os

from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk.pipelines import (
    CodeBuildStep,
    CodePipeline,
    CodePipelineSource,
    ShellStep,
)
from constructs import Construct
from pipeline_stage import PipelineStage
from application.steps import DEPLOY_STEPS
from resources.utils import pascal_case


class InfraStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, env: object, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, env=env.ENV, **kwargs)

        vpc = ec2.Vpc.from_lookup(self, "ImportVPC", vpc_id=env.VPC_ID)

        source_checkout = CodePipelineSource.connection(
            env.GIT_REPOSITORY,
            env.TRACKING_BRANCH,
            connection_arn=env.GITHUB_CONNECTION_ARN,
            code_build_clone_output=True,
        )

        # Code pipeline definition
        pipeline = CodePipeline(
            self,
            "Pipeline",
            pipeline_name=f"{pascal_case(env.APP_NAME)}Pileline",
            cross_account_keys=True,
            docker_enabled_for_synth=True,
            synth=ShellStep(
                "Synth",
                input=source_checkout,
                commands=[
                    "npm install -g aws-cdk",
                    "curl -sSL https://install.python-poetry.org | python3 -",
                    "cd infra",
                    "/root/.local/bin/poetry install",
                    "/root/.local/bin/poetry run cdk synth",
                ],
                primary_output_directory="infra/cdk.out",
            ),
        )

        # NOTE: This step is necessary otherwise the stages bellow will fail due to the oversized
        # artifact.
        strip_assets_step = CodeBuildStep(
            "StripAssetsFromAssembly",
            input=pipeline.cloud_assembly_file_set,
            commands=[
                'S3_PATH=${CODEBUILD_SOURCE_VERSION#"arn:aws:s3:::"}',
                "ZIP_ARCHIVE=$(basename $S3_PATH)",
                "rm -rfv asset.*",
                "zip -r -q -A $ZIP_ARCHIVE *",
                "aws s3 cp $ZIP_ARCHIVE s3://$S3_PATH",
            ],
        )
        pipeline.add_wave("BeforeDeploy", pre=[strip_assets_step])

        for step in DEPLOY_STEPS:
            stage = PipelineStage(self, env, step, step.step_name(), vpc)
            pipeline.add_stage(stage)

        pipeline.build_pipeline()
        pipeline.pipeline.artifact_bucket.grant_write(strip_assets_step.project)
