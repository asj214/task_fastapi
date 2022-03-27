import logging
from typing import Any, Dict, List, Tuple
from pydantic import BaseSettings, SecretStr


class AppSettings(BaseSettings):
    debug: bool
    docs_url: str = '/docs'
    openapi_prefix: str = ''
    openapi_url: str = '/openapi.json'
    redoc_url: str = '/redoc'
    title: str = 'FastAPI Tutorials'
    version: str = '0.0.0'

    max_connection_count: int = 10
    min_connection_count: int = 10

    mysql_host: str
    mysql_port: int
    mysql_db_name: str
    mysql_user: str
    mysql_password: str

    secret_key: SecretStr
    api_prefix: str = '/api'

    jwt_token_prefix: str = 'Token'

    allowed_hosts: List[str] = ['*']

    logging_level: int = logging.INFO
    loggers: Tuple[str, str] = ('uvicorn.asgi', 'uvicorn.access')

    class Config:
        env_file = '.env'
        validate_assignment = True

    
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            'debug': self.debug,
            'docs_url': self.docs_url,
            'openapi_prefix': self.openapi_prefix,
            'openapi_url': self.openapi_url,
            'redoc_url': self.redoc_url,
            'title': self.title,
            'version': self.version,
        }

    @property
    def database_url(self) -> str:
        return 'mysql://{}:{}@{}:{}/{}'.format(
            self.mysql_user,
            self.mysql_password,
            self.mysql_host,
            self.mysql_port,
            self.mysql_db_name
        )
