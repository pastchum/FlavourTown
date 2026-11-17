from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "flavourgraph"
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    similarity_top_k: int = 25


settings = Settings()
