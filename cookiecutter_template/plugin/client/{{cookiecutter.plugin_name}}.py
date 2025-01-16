
from typing import List, Any

import structlog
import requests
logger = structlog.getLogger(__name__)


class {{cookiecutter.PluginName}}Client(object):
    def __init__(self, api_key, params={}):
        self.base_url = '{{cookiecutter.APIBaseURL}}'
        self.params = params
        self.api_key = api_key

    def url_for_endpoint(self, version, endpoint, path_params=None):
        endpoint = '{}/{}/{}'.format(self.base_url, version, endpoint)
        if path_params is not None:
            for path_param in path_params:
                if path_param:
                    endpoint += '/{}'.format(path_param)
        return endpoint

    def get_data(self, version, resource, path_params=None):
        url = self.url_for_endpoint(version, resource, path_params)
        items = self.get_endpoint_data(url)
        return items

    def get_raw_data(self, version, resource, path_params=None):
        url = self.url_for_endpoint(version, resource, path_params)
        data = self.get_endpoint(url)
        return data

    def get_endpoint_data(self, url=None, params=None):
        data = self.get_endpoint(url, params)
        items = data['items']
        next_link = data['meta']['next']
        while next_link is not None:
            data = self.get_endpoint(next_link, params)
            next_link = data['meta']['next']
            items.extend(data['items'])
        return items

    def get_endpoint(self, url=None, params=None):
        if not url:
            url = self.url
        if not params:
            params = self.params
        try:
            logger.info("getting {} with params {}".format(url, params))
            response = requests.get(
                url, params=params, auth=self.credentials, timeout=60)
            response.raise_for_status()
            json = response.json()
            logger.debug('url: {} json: {}'.format(url, json))
            return json
        except Exception as e:
            logger.error('{} {} with params {} failed.  Error {}'.format(
                'get', url, params, e))
            raise
