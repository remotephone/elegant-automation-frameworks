from tarfile import SUPPORTED_TYPES


class Config:
    def __init__(self, env):
        
        # Probably gonna have multiple environments, this class will help
        # Local, Shared/Dev, QA, Staging, Prod
        SUPPORTED_ENVS = ['dev', 'qa']

        if env.lower() not in SUPPORTED_ENVS:
            raise Exception(f'{env} is not a supported environment (supported envs: {SUPPORTED_ENVS}')
        self.base_url = {
            'dev': 'https://mydev-env.com',
            'qa': 'https://myqa-env.com'
        }[env]
        # With this setup all we need is the info that tells us what environment we're in
        # That's the required env arg above
        # This is new syntax to me, define a dictionary and pull a key from it automatically
        # Neat

        self.app_port = {
            'dev': 8080,
            'qa': 80
        }[env]
