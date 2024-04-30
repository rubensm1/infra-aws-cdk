from application.steps import DEPLOY_STEPS
from pipeline_stage import PipelineStage


def test_make_stages(env, app):
    for step in DEPLOY_STEPS:
        stage = PipelineStage(app, env, step, step.step_name())
