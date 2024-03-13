import http
import requests
import json

LIMIT = 2

class SilkClient:
    def __init__(self):
        self.base_url = ""
        self.token = 'nehajain.101067@gmail.com_8de3bb3e-c9b5-4d7d-9c35-b520d93ec746'

    def get_type(self):
        return "silk"

    def get_hosts(self,skip):
        headers = {'accept': 'application/json','token': self.token}
        response = requests.post(self.base_url+'?skip='+str(skip)+'&limit='+str(LIMIT), headers=headers)
        if response.status_code != http.HTTPStatus.OK:
            raise Exception('crowdstrike request failed', response.status_code)

        host_list = json.loads(response.content)
        return host_list

class CrowdStrikeClient(SilkClient):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://api.recruiting.app.silk.security/api/crowdstrike/hosts/get'

    def get_type(self):
        return 'crowdstrike'


class QualysClient(SilkClient):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://api.recruiting.app.silk.security/api/qualys/hosts/get'

    def get_type(self):
        return 'qualys'


