from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    ES_HOST: str = Field("127.0.0.1", env="ELASTIC_HOST")
    ES_PORT: str = Field("9200", env="ELASTIC_PORT")
    REDIS_HOST: str = Field("127.0.0.1", env="REDIS_HOST")
    REDIS_PORT: str = Field("6379", env="REDIS_PORT")


test_settings = TestSettings()
