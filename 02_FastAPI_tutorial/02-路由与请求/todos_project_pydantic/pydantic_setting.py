from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Todos App"
    host: str = "localhost"
    port: int = 8000
    reload: bool
    model_config = {"env_file": ".env"}

settings = Settings()

if __name__ == "__main__":
    print(settings.app_name, settings.host, settings.port, settings.reload)
    print(settings.model_dump())
