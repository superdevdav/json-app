from pydantic import BaseModel

class Configuration(BaseModel):
  specification: dict
  settings: dict

class Engine(BaseModel):
  kind: str = 'Engine'
  name: str
  version: str
  description: str
  configuration: Configuration
