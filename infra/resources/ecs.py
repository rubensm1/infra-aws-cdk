import os

from aws_cdk import Duration
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_secretsmanager as secrets
from aws_cdk import aws_ssm as ssm
from .resourse import Resource, PathStrFormat
from aws_cdk.aws_ecr_assets import DockerImageAsset
from .utils import kebab_case
from .utils import pascal_case
import json


class ECSMemoryCPU:
    def __init__(self, mem: int = 512, cpu: int = 256) -> None:
        self.mem = mem
        self.cpu = cpu
        self.validate()

    def validate(self) -> None:
        if self.mem not in [
            512,
            1024,
            2048,
            3072,
            4096,
            5120,
            6144,
            7168,
            8192,
            9216,
            10240,
            11264,
            12288,
            13312,
            14336,
            15360,
            16384,
            17408,
            18432,
            19456,
            20480,
            21504,
            22528,
            23552,
            24576,
            25600,
            26624,
            27648,
            28672,
            29696,
            30720,
            32768,
            36864,
            40960,
            45056,
            49152,
            53248,
            57344,
            61440,
            65536,
            69632,
            73728,
            81920,
            90112,
            98304,
            106496,
            114688,
            122880,
        ]:
            raise ValueError("Value of Memory is invalid")
        if self.cpu not in [256, 512, 1024, 2048, 4096, 8192, 16384]:
            raise ValueError("Value of CPU is invalid")
        if self.cpu == 256 and self.mem not in [512, 1024, 2048]:
            raise ValueError("Value of CPU is 256 and Memory is not 512, 1024 or 2048")
        if self.cpu == 512 and self.mem not in [1024, 2048, 3072, 4096]:
            raise ValueError(
                "Value of CPU is 512 and Memory is not 1024, 2048, 3072 or 4096"
            )
        if self.cpu == 1024 and self.mem not in [
            2048,
            3072,
            4096,
            5120,
            6144,
            7168,
            8192,
        ]:
            raise ValueError(
                "Value of CPU is 1024 and Memory is not 2048, 3072, 4096, 5120, 6144, 7168 or 8192"
            )
        if self.cpu == 2048 and self.mem not in [
            4096,
            5120,
            6144,
            7168,
            8192,
            9216,
            10240,
            11264,
            12288,
            13312,
            14336,
            15360,
            16384,
        ]:
            raise ValueError(
                "Value of CPU is 2048 and Memory is not 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360 or 16384"
            )
        if self.cpu == 4096 and self.mem not in [
            8192,
            9216,
            10240,
            11264,
            12288,
            13312,
            14336,
            15360,
            16384,
            17408,
            18432,
            19456,
            20480,
            21504,
            22528,
            23552,
            24576,
            25600,
            26624,
            27648,
            28672,
            29696,
            30720,
        ]:
            raise ValueError(
                "Value of CPU is 4096 and Memory is not 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, 30720"
            )
        if self.cpu == 8192 and self.mem not in [
            16384,
            20480,
            24576,
            28672,
            32768,
            36864,
            40960,
            45056,
            49152,
            53248,
            57344,
            61440,
        ]:
            raise ValueError(
                "Value of CPU is 8192 and Memory is not 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344 or 61440"
            )
        if self.cpu == 16384 and self.mem not in [
            32768,
            40960,
            49152,
            57344,
            65536,
            73728,
            81920,
            90112,
            98304,
            106496,
            114688,
            122880,
        ]:
            raise ValueError(
                "Value of CPU is 16384 and Memory is not 32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688 or 122880"
            )


class ECS(Resource):
    _vpc: ec2.Vpc
    service_port: int
    subnet_type: ec2.SubnetType
    mem_cpu: ECSMemoryCPU

    def __init__(
        self,
        scope: str,
        env: object,
        vpc: ec2.Vpc,
        service_port: int = None,
        subnet_type: ec2.SubnetType = ec2.SubnetType.PUBLIC,
        mem_cpu: ECSMemoryCPU = ECSMemoryCPU(),
    ):
        super().__init__(scope, env)
        self._vpc = vpc
        self.service_port = service_port
        self.subnet_type = subnet_type
        self.mem_cpu = mem_cpu

    def get_path_str_format(self) -> PathStrFormat:
        return PathStrFormat.PASCAL_CASE

    def create(
        self,
        task_image_options: ecs_patterns.ApplicationLoadBalancedTaskImageOptions = None,
        health_check_path: str = "/",
    ):
        if not task_image_options:
            task_image_options = self.create_task_image_options()
        task_subnets = ec2.SubnetSelection(subnet_type=self.subnet_type)
        load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self.scope,
            f"{pascal_case(self.store_path_prefix)}Service",
            vpc=self._vpc,
            assign_public_ip=True,
            listener_port=self.service_port,
            health_check_grace_period=Duration.seconds(300),
            service_name=f"{pascal_case(self.env.APP_NAME)}App",
            load_balancer_name=f"{kebab_case(self.store_path_prefix)}-lb",
            # certificate=certificate,
            memory_limit_mib=self.mem_cpu.mem,
            cpu=self.mem_cpu.cpu,
            task_image_options=task_image_options,
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True),
            task_subnets=task_subnets,
            enable_execute_command=True,
        )
        if self.service_port:
            load_balanced_fargate_service.target_group.configure_health_check(
                port=str(self.service_port), path=health_check_path
            )
        return load_balanced_fargate_service

    def create_task_image_options(
        self,
        dockerfile_name="Dockerfile",
        repository_dir=None,
        secret_mapping: dict = {},
        entrypoint: list[str] | None = None,
    ) -> ecs_patterns.ApplicationLoadBalancedTaskImageOptions:
        container_asset = self._create_container_asset(dockerfile_name, repository_dir)
        return ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_docker_image_asset(container_asset),
            environment=self.env.to_dict(),
            secrets=secret_mapping,
            container_port=self.service_port,
            container_name=f"{kebab_case(self.store_path_prefix)}-app",
            entry_point=entrypoint if entrypoint else None,
        )

    def _create_container_asset(
        self, dockerfile_name="Dockerfile", repository_dir=None
    ) -> DockerImageAsset:
        if not repository_dir:
            repository_dir = self.env.REP_DIR
        # Build container
        # token = subprocess.check_output(self.env.TOKEN_CMD, shell=True).decode("utf-8")
        return DockerImageAsset(
            self.scope,
            "app",
            directory=os.path.join(__file__, f"../../../{repository_dir}"),
            file=dockerfile_name,
            # build_args={"CODEARTIFACT_AUTH_TOKEN": token},
        )

    def create_secret_mapping(
        self, secret: secrets.Secret, fields: list[str | tuple[str, str]]
    ) -> dict:
        """
        Create a mapping of secret fields to ECS secrets.
        :param secret: The Secrets Manager secret.
        :param fields: A list of tuples where each tuple contains the field name (to set a ENV var) and the secret field name.
        :return: A dictionary mapping field names to ECS secrets.
        """
        for field in fields:
            if isinstance(field, str):
                field = (field, field)
            if len(field) != 2:
                raise ValueError(
                    "Each field must be a tuple of (env_var_name, secret_field_name)"
                )

        return {
            field[0]: ecs.Secret.from_secrets_manager(secret, field=field[1])
            for field in fields
        }

    def create_secret_mapping_from_parameter(
        self, key_field, parameter_name: str
    ) -> dict:
        param = ssm.StringParameter.from_string_parameter_name(
            self, f"SecretMappingParam{key_field}", string_parameter_name=parameter_name
        )
        return {key_field: ecs.Secret.from_ssm_parameter(param)}

    def consolidate_secret_mapping(
        self, secret_mapping: dict, *additional_mapping: dict
    ) -> dict:
        consolidated_mapping = secret_mapping.copy()
        for mapping in additional_mapping:
            consolidated_mapping.update(mapping)
        return consolidated_mapping
