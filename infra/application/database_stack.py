from resources.deploy_step import DeployStepStack


class ServerlessDatabaseStack(DeployStepStack):

    @staticmethod
    def step_name() -> str:
        return "Database"

    def deploy(self) -> None:
        return None
