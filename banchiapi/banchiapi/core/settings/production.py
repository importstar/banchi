from banchaiapi.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):

    MONGODB_HOST: str = "banchai-mongodb"

    class Config(AppSettings.Config):
        env_file = "prod.env"
