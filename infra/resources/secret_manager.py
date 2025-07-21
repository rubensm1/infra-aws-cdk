from aws_cdk import aws_secretsmanager as secrets
from .resourse import Resource, PathStrFormat
from .parameters_store import ParametersStore
from .utils import snake_case


class SecretManager(Resource):
    def get_path_str_format(self) -> PathStrFormat:
        return PathStrFormat.SNAKE_CASE

    def get_complete_secret_from_arn(self, secret_arn) -> secrets.Secret:
        return secrets.Secret.from_secret_complete_arn(
            self.scope, "ImportedSecret", secret_complete_arn=secret_arn
        )

    def get_complete_secret_from_arn_in_parameter(self, secret_name) -> secrets.Secret:
        parameter_store = ParametersStore(self.scope, self.env)
        pgsql_secret_arn = parameter_store.get_parameter_value(secret_name)
        return self.get_complete_secret_from_arn(pgsql_secret_arn)

    @staticmethod
    def generate_secret_name(prefix) -> str:
        return f"{snake_case(prefix)}_secret"
