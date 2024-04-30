from resources.deploy_step import DeployStepStack


class ResourceStack(DeployStepStack):

    @staticmethod
    def step_name() -> str:
        return "Resources"

    def deploy(self) -> None:
        return None
