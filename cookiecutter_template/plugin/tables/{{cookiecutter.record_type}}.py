from typing import Any, Generator

import pyarrow as pa
from cloudquery.sdk.scheduler import TableResolver
from cloudquery.sdk.schema import Column
from cloudquery.sdk.schema import Table
from cloudquery.sdk.schema.resource import Resource
from cloudquery.sdk.types import JSONType

from plugin.client import Client
from plugin import PLUGIN_NAME

import structlog
logger = structlog.getLogger(__name__)

ENTITY_NAME = '{{cookiecutter.RecordTypeClass}}'
TABLE_NAME = f"{PLUGIN_NAME}_{ENTITY_NAME}".lower()
TABLE_TITLE= PLUGIN_NAME.title() + f"{ENTITY_NAME}s"

class {{cookiecutter.RecordTypeClass}}(Table):
    def __init__(self) -> None:
        super().__init__(
            name=TABLE_NAME,
            title=TABLE_TITLE,
            columns=[
                Column("id", pa.string()),
                Column("name", pa.string()),
                Column("url", pa.string()),
                Column("fields", JSONType())
            ]
        )

    @property
    def resolver(self):
        return {{cookiecutter.PluginName}}Resolver(table=self)


class {{cookiecutter.PluginName}}Resolver(TableResolver):
    def __init__(self, table) -> None:
        super().__init__(table=table)

    def resolve(
        self, client: Client, parent_resource: Resource
    ) -> Generator[Any, None, None]:

        # This is where you would call your client to get data from your API
        # As you will likely need to change your client in ./client/client.py to match your API, you will need to change this code to match your client's API as well.

        url = client.client.url_for_endpoint('v1', "items")
        data = client.client.get_endpoint(url, params={'param1':'value1'})
        items = data['items']
        for item in items:
            yield item

        # Pagination example - your API for your {{cookiecutter.plugin_name}} data source may be different. Change as needed!

        next_link = data['meta']['next']
        while next_link is not None:
            data = client.client.get_endpoint(next_link, None)
            next_link = data['meta']['next']
            for i in data['items']:
                yield i
