from environment import get_env


def test_get_env():
    cdk_env = get_env()
    assert cdk_env.TYPE == "dev"
