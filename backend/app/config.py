from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
    app_name:str='NEXTORA API'
    environment:str='production'
    database_url:str
    jwt_secret:str
    jwt_algorithm:str='HS256'
    access_token_minutes:int=30
    cors_origins:str='https://nextora-website.vercel.app'
    registration_enabled:bool=False
settings=Settings()
