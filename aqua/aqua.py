from typing import Dict, List
from urllib.parse import urlencode
import json
import requests
import urllib3


class Aqua():

    def __init__(self, id: str = None, password: str = None, host: str = None, port: str = '443', api_version: str = 'v1',\
                 using_tls = True, verify_tls: bool = False, cacert_file: str = None, proxy = None):
        """
        Currently both v1 and v2 calls are abstracted in this client. You currently do not need to specify API version to
        make v2 calls.

        Args:
            id: username
            password: password
            host: CSP console/API server IP address
            port:  CSP console/API server port
            api_version: optional. currently at v1
            using_ssl: optional. used to hit https urls
            verify_tls: optional. Whether to validate certificate. Set to false for self signed certs.
            cacert_file: optional CA certificates to trust for certificate verification
            proxy: optional http/https proxy dictionary

        :return: an Aqua object that represents API endpoint and used for all subsequent calls.
        """

        self.api_version = api_version
        self.verify_tls = verify_tls
        if self.verify_tls is False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        self.id = id
        self.proxy = proxy
        self.host = host
        self.port = port
        self.headers = {'Content-Type': 'application/json', 'api-version': self.api_version}
        self.url_prefix = 'http{}://{}:{}/api/{}'.format('s' if using_tls else '', self.host, self.port, self.api_version)
        self._auth(password)

    def _auth(self, password):
        url = "{}/login".format(self.url_prefix)
        aqua_credentials = json.dumps(dict(id=self.id, password=password))
        response = requests.post(url, data=aqua_credentials, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        response_json = json.loads(response.content.decode('utf-8'))

        if 'token' in response_json:
            self.token = response_json['token']
        else:
            raise Exception("Authentication Error")
        self.role = response_json['user']['role']
        self.is_super = response_json['user']['is_super']
        self.headers['Authorization'] = f"Bearer {self.token}"
        return 'Authentication successful'


    # Registries

    def list_registries(self):
        url = "{}/registries".format(self.url_prefix)
        response = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))
    """
    def create_registry(self, type: str, name: str, description:str, username: str, password: str, url: str = None, prefixes):
        url = "{}/registries".format(self.url_prefix)
        data = json.dumps(dict(type=type, name=name, description=description, username=username, password=password, url=url))
        response = requests.post(url, data=data, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return json.loads(response.content.decode('utf-8'))
    """
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
        #response = requests.put(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        #return response
        return self.send_request(url, 'put')

    def get_profile(self, profile_name: str):
        """
        Return the structure of an image runtime profile

        :param profile_name: name of profile to retrieve
        :return: the structure of an image runtime profile
        """
        url = "{}/securityprofiles/{}".format(self.url_prefix, profile_name)
        return self.send_request(url)

    def modify_profile(self, profile_name: str, profile: str):
        """
        Update an existing image runtime profile

        :param profile_name: name of profile to update
        :param profile: json object i.e. returned from get_suggested_profile
        :return: A successful creation of the new profile will result in a 204 No Content response.
        """
        url = "{}/securityprofiles/{}".format(self.url_prefix, profile_name)
        response = requests.put(url, data=profile, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response



    #image export and import
    def export_images(self, images: List[str]):
        url = "{}/images/export".format(self.url_prefix)
        response = requests.post(url, data=json.dumps(dict(images=images)), verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return response.json()

    #scanning images

    def scan_status(self, registry_name: str, image_name: str, image_tag: str = 'latest') -> Dict:
        """Get status of an image vulnerability scan.

        :param registry_name: name of the registry
        :param image_name: name of container image
        :param image_tag: optional. image tag. defaults to latest
        :return: scan status results as Dict
        """
        url = "{}/scanner/registry/{}/image/{}:{}/status".format(self.url_prefix, registry_name, image_name, image_tag)
        return self.send_request(url)

    def scan_results(self, registry_name: str, image_name: str, image_tag: str = 'latest'):
        url = "{}/scanner/registry/{}/image/{}:{}/scan_result".format(self.url_prefix, registry_name, image_name, image_tag)
        return self.send_request(url)

    def scan_queue(self):
        url = "{}/scanqueue/summary".format(self.url_prefix)
        return self.send_request(url)

    def start_image_scan(self, registry_name: str, image_name: str, image_tag: str = 'latest') -> Dict:
        """Get status of an image vulnerability scan.

        :param registry_name: name of the registry
        :param image_name: name of container image
        :param image_tag: optional. image tag. defaults to latest
        :return: scan status as Dict
        """
        url = "{}/scanner/registry/{}/image/{}:{}/scan".format(self.url_prefix, registry_name, image_name, image_tag)
        return self.send_request(url=url, method='post')

    #secrets
    def list_secrets(self):
        url = "{}/secrets".format(self.url_prefix)
        return self.send_request(url)


    """
    Enforcer Host Management
    """

    def hosts(self):
        url = "{}/hosts".format(self.url_prefix)
        return self.send_request(url=url, method='get')

    def send_request(self, url, method='get', data=None):
        request_method = getattr(requests, method)

        try:
            response = request_method(url=url, data=data, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))
            elif response.status_code == 204:
                return json.loads('{}')
            else:
                return json.loads(response.content)

        except Exception as e:
            print(e)


    """
    v2 calls
    """

    """
    v2 Images
    """
    def register_image(self, registry, image_name, image_tag: str = 'latest'):
        url = "{}/images".format(self.url_prefix.replace('v1', 'v2'))
        data = json.dumps(dict(registry=registry, image=f'{image_name}:{image_tag}'))
        resp = requests.post(url, data=data, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def list_registered_images(self, registry: str = None, repository: str = None, name: str = None, page: int = None, page_size: int = None, order_by: str = None):
        query_string = urlencode({k:v for (k,v) in locals().items() if v is not None and k is not 'self'})   #build query string from parameters that are not None
        url = "{}/images?{}".format(self.url_prefix.replace('v1', 'v2'), query_string)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()


    def get_registered_images(self, registry: str = None, repository: str = None, name: str = None):
        query_string = urlencode({k:v for (k,v) in locals().items() if v is not None and k is not 'self'})   #build query string from parameters that are not None
        url = "{}/images?{}".format(self.url_prefix.replace('v1', 'v2'), query_string)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def get_registered_image(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def list_image_vulnerabilities(self, registry, image_name, image_tag: str = 'latest', page: int = 0, pagesize: int = 50,
                                   show_negligible: bool = True, hide_base_image: bool = False):
        query_string = urlencode({k: v for (k, v) in locals().items() if v is not None and k not in ['self', 'image_tag']})
        print(query_string)
        url = "{}/images/{}/{}/{}/vulnerabilities?{}".format(self.url_prefix.replace('v1', 'v2'), registry, image_name, image_tag, query_string)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def list_image_malware(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}/malware".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def list_image_sensitive_data(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}/sensitive".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        resp =  requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()

    def list_image_layers(self, registry: str, repo: str, tag: str = "latest"):
        url = "{}/images/{}/{}/{}/history_layers".format(self.url_prefix.replace('v1', 'v2'), registry, repo, tag)
        resp = requests.get(url, verify=self.verify_tls, headers=self.headers, proxies=self.proxy)
        return resp.json()