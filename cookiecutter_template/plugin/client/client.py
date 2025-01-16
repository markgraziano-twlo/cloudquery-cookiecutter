from dataclasses import dataclass, field
from cloudquery.sdk.scheduler import Client as ClientABC
from datetime import datetime

from .{{cookiecutter.plugin_name}} import {{cookiecutter.PluginName}}Client

DEFAULT_CONCURRENCY = 100
DEFAULT_QUEUE_SIZE = 10000
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_MAX_RETRIES = 20

@dataclass
class Spec:
    api_key: str = field(default=None)
    concurrency: int = field(default=DEFAULT_CONCURRENCY)
    queue_size: int = field(default=DEFAULT_QUEUE_SIZE)

    def validate(self):
        if self.api_key is None:
            raise ValueError("Must specify an API key")

class Client(ClientABC):
    def __init__(self, spec: Spec) -> None:
        self._spec = spec
        self._client = {{cookiecutter.PluginName}}Client(api_key=spec.api_key)

    def id(self):
        return "{{cookiecutter.plugin_name}}"

    @property
    def client(self) -> {{cookiecutter.PluginName}}Client:
        return self._client

    @property
    def server(self) -> str:
        return self._spec.server
