from pytest import mark

# so now our config takes in the env argument, sets up the environment for us
# We can test and  these will pass or fail depending on what we pass


def test_environment_is_qa(app_config):
    base_url = app_config.base_url
    port = app_config.app_port
    assert base_url == "https://myqa-env.com"
    assert port == 80


@mark.skip(reason="broken by deploy, needs to be fixed")
def test_environment_is_dev(app_config):
    base_url = app_config.base_url
    port = app_config.app_port
    assert base_url == "https://mydev-env.com"
    assert port == 8080


@mark.xfail(reason="This has been deprecated, want to be sure it doesn't work")
def test_environment_is_staging(app_config):
    base_url = app_config.base_url
    port = app_config.app_port
    assert base_url == "staging"
