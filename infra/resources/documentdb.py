from aws_cdk import aws_docdb as docdb
from aws_cdk import aws_ec2 as ec2
from .parameters_store import ParametersStore
from .secret_manager import SecretManager

from .resourse import Resource, PathStrFormat


class DocumentDB(Resource):

    _vpc: ec2.Vpc
    db_cluster: docdb.DatabaseCluster
    store_path_prefix_combined: str

    def __init__(self, scope: str, env: object, vpc: ec2.Vpc):
        super().__init__(scope, env)
        self._vpc = vpc
        self.store_path_prefix_combined = f"{self.store_path_prefix}MongoDB"

    def get_path_str_format(self) -> PathStrFormat:
        return PathStrFormat.PASCAL_CASE

    def _create_db_security_group(self):
        vpc_cidr = self._vpc.vpc_cidr_block
        db_sg = ec2.SecurityGroup(
            self,
            "MongoDBSecurityGroup",
            vpc=self._vpc,
            allow_all_outbound=True,
        )
        db_sg.add_ingress_rule(
            peer=ec2.Peer.ipv4(vpc_cidr),
            connection=ec2.Port.tcp(27017),
            description="allow inbound traffic from VPC to MongoDB on port 27017",
        )
        return db_sg

    def _create_documentdb_cluster(self) -> docdb.DatabaseCluster:
        return docdb.DatabaseCluster(
            self.scope,
            f"{self.store_path_prefix_combined}Cluster",
            master_user=docdb.Login(
                username="admin",
                secret_name=self.get_secret_name(),
                exclude_characters='"/@:[]#!*',
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.T3, ec2.InstanceSize.MEDIUM
            ),
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            vpc=self._vpc,
            security_groups=[self._create_db_security_group()],
            deletion_protection=True,
        )

    def get_secret_name(self) -> str:
        return SecretManager.generate_secret_name(self.store_path_prefix_combined)

    def create(self):
        self.db_cluster = self._create_documentdb_cluster()
        # Store secret ARN in Parameter Store
        parameters_store = ParametersStore(self.scope)
        parameters_store.create_parameter(
            self.get_secret_name(), self.db_cluster.secret.secret_arn
        )
