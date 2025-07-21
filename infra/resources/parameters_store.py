import os

from .resourse import Resource, PathStrFormat

from aws_cdk import aws_ssm as ssm


class ParametersStore(Resource):
    def get_path_str_format(self) -> PathStrFormat:
        return PathStrFormat.SNAKE_CASE

    def create_parameter(self, name, value):
        ssm.StringParameter(
            scope=self.scope,
            id=f"{self.store_path_prefix}_{name}",
            parameter_name=f"/{self.store_path_prefix}/{name}",
            string_value=value,
        )

    def create_parameters(self, parameters: list):
        for parameter in parameters:
            self.create_parameter(parameter["name"], parameter["value"])

    def get_parameter_value(self, name):
        return self.get_parameter(name).string_value

    def get_parameter(self, name):
        parameter_name = f"/{self.store_path_prefix}/{name}"
        return ssm.StringParameter.from_string_parameter_attributes(
            self.scope,
            f"get{self.store_path_prefix}_{name}",
            parameter_name=parameter_name,
        )
