import json

import requests

from azuresearch.service import Endpoint
from azuresearch.skills import Skill


class Skillset(object):
    endpoint = Endpoint("skillset")
    __name__ = "Skillset"

    def __init__(self, name, skills, description=None):

        if name is None:
            raise Exception("Please provide a name for this skillset")

        if skills is None or len(skills) == 0:
            raise Exception("A skillset must have at least one skill")

        if not isinstance(skills[0], Skill):
            raise Exception("Skills must be of type 'Skill'")

        self.name = name
        self.skills = skills
        self.description = description

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'skills': [skill.to_dict() for skill in self.skills]
        }

    @classmethod
    def load(cls, data):
        if type(data) is str:
            data = json.loads(data)
        if type(data) is not dict:
            raise Exception("Failed to parse input as Dict")
        if 'skills' not in data:
            raise Exception("Skills not found")
        if 'name' not in data:
            raise Exception("Skillset name not found")

        if 'description' not in data:
            data['description'] = ''

        return cls(name=data['name'], skills=data['skills'], description=data['description'])

    def create(self):
        result = self.endpoint.post(self.to_dict(), needs_admin=True)
        if result.status_code != requests.codes.created:
            raise Exception("Error posting skillset. result: {}".format(result))

    def get(self):
        result = self.endpoint.get(endpoint=self.name, needs_admin=True)
        if result.status_code != requests.codes.ok:
            raise Exception("Error getting skillset. Result: {}".format(result))
        return result

    def delete(self):
        result = self.endpoint.delete(endpoint=self.name, needs_admin=True)
        if result.status_code != requests.codes.no_content:
            raise Exception("Error deleting skillset. Result: {}".format(result))

    def update(self):
        self.delete()
        return self.create()

    def verify(self):
        return self.get()
