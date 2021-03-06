import requests
import json
from json import JSONEncoder
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class CMDBuildNLMK(object):
    def __init__(self, username,password):
        self.service = "https://..../cmdbuild"
        self.username = username
        self.password = password
        self.session_id = None
        
    @property
    def headers(self):
        return {
            'Content-type': 'application/json',
            'Accept': '*/*',
            'CMDBuild-Authorization': self.session_id
        }
    
    def api(self, path):
        ret = "{host}/services/rest/v3/{path}".format(host=self.service.strip('/'), path=path.strip())
        return ret

    def request_get(self,path, data = None):
        api = self.api(path)
        if data is not None:
            data = json.dumps(data)
        req = requests.get(api, data=data, headers=self.headers, verify = False)
        return req.json()

    def request_post(self,path,data):
        api = self.api(path)
        data = json.dumps(data)
        req = requests.post(api, data=data, headers=self.headers, verify = False)
        return req.json()
    
    def connect(self):
        data = json.dumps(dict(username=self.username,password=self.password))
        path = "sessions/?scope=service&returnId=true"
        api = self.api(path)
        ret = requests.post(api, data=data, headers=self.headers, verify = False)
        self.session_id = ret.json()["data"]["_id"]
        return self.session_id
    
    def close(self):
        path = 'sessions/{0}'.format(self.session_id)
        api = self.api(path)
        ret = requests.delete(api, headers = self.headers, verify = False)
        self.session_id = None
        return (ret.json())
    
    def get_classes_NetworkBox(self):
        path = "classes/NetworkBox/"
        return self.request_get(path)
    
    def insert_card_NetworkBox(self, card_data):
        path = "classes/NetworkBox/cards/"
        return self.request_post(path=path, data=card_data)
    
    def get_ProductsInfo(self, bname):
        filter = []
        filter.append(
            {
                'simple':{
                    'attribute' : 'Model',
                    'operator' : 'equal',
                    'value' : [bname],
                }
            }
        )
        data = {"attribute":filter[0]} # for example to use the one filter' attribute
        path = "classes/HWCatalogue/cards?filter={0}".format(data)
        ret = self.request_get(path=path)

        return ret
    
