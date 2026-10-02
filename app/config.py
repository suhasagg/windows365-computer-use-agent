from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    env:str="dev"; w365_mcp_endpoint:str=""; w365_computer_id:str=""; w365_token_scope:str=""
    jwt_secret:str="change-me"; approval_secret:str="change-me"
    database_url:str="postgresql+asyncpg://cua:cua@localhost:5432/cua"
    redis_url:str="redis://localhost:6379/0"
    max_steps:int=30; max_retries:int=2; tool_timeout_seconds:float=30
    allowed_browser_hosts:str="example.com,learn.microsoft.com"
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    @property
    def hosts(self): return {x.strip().lower() for x in self.allowed_browser_hosts.split(",") if x.strip()}
settings=Settings()
