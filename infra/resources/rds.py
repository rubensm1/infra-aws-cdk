import os
from abc import abstractmethod

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_rds as rds
from .resourse import Resource, PathStrFormat
from .parameters_store import ParametersStore
from .secret_manager import SecretManager
from .utils import snake_case


class ServerlessRDS(Resource):
    _vpc: ec2.Vpc
    db_cluster: rds.ServerlessCluster
    store_path_prefix_combined: str

    def __init__(self, scope: str, vpc: ec2.Vpc):
        super().__init__(scope)
        self._vpc = vpc
        self.store_path_prefix_combined = f"{self.store_path_prefix}{self.get_store_path_prefix_append()}"

    def get_path_str_format(self) -> PathStrFormat:
        return PathStrFormat.PASCAL_CASE

    def _create_db_security_group(self):
        db_port = self.get_db_port()
        db_security_group = ec2.SecurityGroup(
            self.scope,
            f"{self.store_path_prefix_combined}SecurityGroup",
            vpc=self._vpc,
            allow_all_outbound=True,
        )
        # allow inbound traffic from anywhere to the db
        db_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(db_port),
            description=f"allow inbound traffic from anywhere to the db on port {db_port}",
        )
        return db_security_group

    def _create_serverless_cluster(self) -> rds.ServerlessCluster:
        # cluster definition
        return rds.ServerlessCluster(
            self.scope,
            f"{self.store_path_prefix_combined}Cluster",
            default_database_name=snake_case(self.store_path_prefix),
            engine=self.get_db_cluster_engine(),
            copy_tags_to_snapshot=True,
            vpc=self._vpc,
            scaling=self.get_scaling_options(),
            security_groups=[self._create_db_security_group()],
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        )

    def get_secret_name(self) -> str:
        return SecretManager.generate_secret_name(self.store_path_prefix_combined)

    def create(self):
        self.db_cluster = self._create_serverless_cluster()
        # Store secret ARN in Parameter Store
        parameters_store = ParametersStore(self.scope)
        parameters_store.create_parameter(self.get_secret_name(), self.db_cluster.secret.secret_arn)

    @abstractmethod
    def get_store_path_prefix_append(self) -> str:
        pass

    @abstractmethod
    def get_db_port(self) -> int:
        pass

    @abstractmethod
    def get_db_cluster_engine(self) -> rds.IClusterEngine:
        pass

    @abstractmethod
    def get_scaling_options(self) -> rds.ServerlessScalingOptions:
        pass


class PostgreSQLAuroraServerless(ServerlessRDS):
    def get_store_path_prefix_append(self) -> str:
        return "AuroraPostgreSQL"

    def get_db_port(self) -> int:
        return 5432

    def get_db_cluster_engine(self) -> rds.IClusterEngine:
        return rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_13_6)

    def get_scaling_options(self) -> rds.ServerlessScalingOptions:
        return rds.ServerlessScalingOptions(
            min_capacity=rds.AuroraCapacityUnit.ACU_2,
            max_capacity=rds.AuroraCapacityUnit.ACU_32,
        )
