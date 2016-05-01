"""
Wrapper for communicating with Gamemaster API.
"""

import requests
from functools import partial
from urlparse import urljoin


class Gamemaster(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.stockfighter.io/gm/'

        self._urljoin = partial(urljoin, self.base_url)
        self.session = requests.Session()
        headers = {'X-Starfighter-Authorization': self.api_key}
        self.session.headers.update(headers)

    def start_level(self, level_name):
        """
        Begin a certain level.

        :type level_name: str
        """
        url = 'levels/{0}'.format(level_name)
        response = self.session.post(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError('Level might not exist: {}'.format(level_name))

    def restart_level(self, instance_id):
        """
        Pass a known instance id to restart a level.

        :type instance_id: int
        """
        url = 'instances/{0}/restart'.format(instance_id)
        response = self.session.post(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError('Level restart failed: {0}'.format(instance_id))

    def stop_level(self, instance_id):
        """
        Stop a level with a given instance id.

        :type instance_id: int
        """
        url = 'instances/{0}/stop'.format(instance_id)
        response = self.session.post(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError('Level stop failed: {0}'.format(instance_id))

    def resume_level(self, instance_id):
        """
        Resume a level with a given instance id.

        :type instance_id: int
        """
        url = 'instances/{0}/resume'.format(instance_id)
        response = self.session.post(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError('Level resume failed: {0}'.format(instance_id))

    def status(self, instance_id):
        """
        Get status of level.

        :type instance_id: int
        """
        url = 'instances/{0}'.format(instance_id)
        response = self.session.get(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            raise KeyError('Level key error: {0}'.format(instance_id))

    def levels(self):
        """
        Retrieve list of available levels.
        """
        url = 'levels'
        response = self.session.get(self._urljoin(url))
        if response.ok:
            return response.json()
        else:
            return None
