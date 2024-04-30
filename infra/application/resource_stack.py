from resources.deploy_step import DeployStepStack


class ResourceStack(DeployStepStack):

    @staticmethod
    def step_name() -> str:
        return "Resources"

    def deploy(self) -> None:
        ecs_container = ECS(
            self,
            env=self.env,
            vpc=self.vpc,
            service_port=int(self.env.SERVICE_PORT),
        )
        ecs_container.create()
