from abc import ABC, abstractmethod

import requests

from azuresearch.service import Endpoint


class BaseApiCall(ABC):
    """
    Abstract class for wrapping common calls to Azure Search services
    """

    def __init__(self, service_name, endpoint=None):
        """
        :param service_name: Name of Azure Search service (e.g. indexes, datasources, skillsets)
        :param endpoint:
        """
        self.service_name = service_name
        if not endpoint:
            self.endpoint = Endpoint(service_name)
        else:
            self.endpoint = endpoint

    @abstractmethod
    def to_dict(self):
        pass

    def create(self):
        result = self.endpoint.post(self.to_dict(), needs_admin=True)
        if result.status_code != requests.codes.created:
            raise Exception(
                "Error posting {service_name}. result: {result}".format(service_name=self.service_name, result=result))

    def get(self):
        result = self.endpoint.get(endpoint=self.name, needs_admin=True)
        if result.status_code != requests.codes.ok:
            raise Exception(
                "Error getting {service_name}. result: {result}".format(service_name=self.service_name, result=result))
        return result

    def delete(self):
        result = self.endpoint.delete(endpoint=self.name, needs_admin=True)
        if result.status_code != requests.codes.no_content:
            raise Exception(
                "Error deleting {service_name}. result: {result}".format(service_name=self.service_name, result=result))

    def update(self):
        self.delete()
        return self.create()

    def verify(self):
        return self.get()

    @staticmethod
    def remove_empty_values_from_dict(dict):
        return {k: v for k, v in dict.items() if v is not None}
