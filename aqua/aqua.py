from typing import Dict
import json
import requests


class Aqua():

    def __init__(self, id: str = None, password: str = None, host: str = None, port: str = '8080', api_version: str = 'v1',\
                 using_ssl = True, verify_tls: bool = False, cacert_file: str = None, proxy = None):

        self.api_version = api_version
        self.verify_tls = verify_tls
        self.id = id
        self.proxy = proxy
        self.host = host
        self.port = port
        self.headers = {'Content-Type': 'application/json', 'api-version': self.api_version}
        self.url_prefix = 'http{}://{}:{}/api/{}'.format('s' if using_ssl else '', self.host, self.port, self.api_version)
        self._auth(password)



    def _auth(self, password):
        url = "{}/login".format(self.url_prefix)
        aqua_credentials = json.dumps(dict(id=self.id, password=password))
        response = requests.post(url, data=aqua_credentials, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        response_json = json.loads(response.content.decode('utf-8'))
        self.token = response_json['token']
        self.role = response_json['user']['role']
        self.is_super = response_json['user']['is_super']
        self.headers['Authorization'] = f"Bearer {self.token}"
        return 'authentication successful'


    # Registries

    def list_registries(self):
        url = "{}/registries".format(self.url_prefix)
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))

    #Image Profiles

    def list_profiles(self):
        """
        Lists of all image runtime profiles in the system

        :return: a list of all image runtime profiles in the system
        """
        url = "{}/securityprofiles".format(self.url_prefix)
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))

    def end_profiling_session(self, registry_name: str, repository: str):
        """
        End a profiling session
        There are two ways to end the profiling session: stopping the containers that were started in the previous stage,
        or issuing an API call. Using the API call will cause the server to cease monitoring the containers' activity,
        but the containers will continue to live, so only use it if you still need them.

        :param registry_name:
        :param repository:
        :return: If the session is successfully terminated, an empty successful response is returned.
        """
        url = "{}/profiler_sessions/{}/{}/stop_containers".format(self.url_prefix, registry_name, repository)
        response = requests.post(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response.content.decode('utf-8')

    def get_suggested_profile(self, registry_name: str, repository: str):
        """
        Get suggested profile generated in a profiling session

        :param registry_name:
        :param repository:
        :return: the suggested image runtime profile in the standard image runtime profile structure.
        """
        url = "{}/profiler_sessions/{}/{}/advice".format(self.url_prefix, registry_name, repository)
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))

    def create_profile(self, profile: str):
        """
        Create a new image runtime profile

        :param profile: json object i.e. returned from get_suggested_profile
        :return: A successful creation of the new profile will result in a 204 No Content response.
        """
        url = "{}/securityprofiles".format(self.url_prefix)
        response = requests.post(url, data=profile, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response

    def attach_profile(self, registry_name: str, repository: str, policy_name: str):
        """
        Attach an image runtime profile to a repository

        :param registry_name:
        :param repository:
        :param policy_name:
        :return:  Upon success, this route will return a 204 No Content response.
        """
        url = "{}/registry/{}/repos/{}/policy/{}".format(self.url_prefix, registry_name, repository, policy_name)
        response = requests.put(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response

