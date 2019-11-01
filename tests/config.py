import os
from pathlib import Path
import yaml


class Config:

    def __init__(self, username, password, host, port, using_tls, verify_tls):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.using_tls = using_tls
        self.verify_tls = verify_tls


def get_config(path):
    path_to_config = Path(f"{os.path.dirname(os.path.abspath(__file__))}/config.yaml")
    if not path_to_config.exists(): raise Exception("Invalid Connfiguration directory")

    with open(str(path_to_config.absolute()), 'r') as stream:
        try:
            config_file = yaml.load(stream, Loader=yaml.FullLoader)
            username = config_file['username']
            password = config_file['password']
            aqua_host = config_file['aqua']['host']
            aqua_port = config_file['aqua']['port']
            aqua_tls = config_file['aqua']['using_tls']
            aqua_verify_tls = config_file['aqua']['verify_tls']

            return Config(username, password, aqua_host, aqua_port, aqua_tls, aqua_verify_tls)
        except yaml.YAMLError as exc:
            print(exc)