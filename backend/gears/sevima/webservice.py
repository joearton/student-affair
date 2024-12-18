from django.conf import settings
from dotenv import load_dotenv
import requests
import json
import time
import os


TOKEN_FILENAME = os.path.join(settings.CACHE_DIR, '.SEVIMA_API_TOKEN')


def is_json(jsonString):
    try:
        json.loads(jsonString)
    except:
        return False
    return True


def check_token_availability(storedToken):
    current_time = time.time()
    expires_in   = storedToken['expires_in']
    ellapse_time = current_time - storedToken['last_request']
    check_expire = ellapse_time < float(expires_in)
    if check_expire:
        print('DEBUG:', 'Sevima Live API using stored token...')
    return check_expire



class BearerAuth(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r



class SevimaAPI:

    def __init__(self):
        self.session = requests.session()
        self.get_sevima_api()


    def get_sevima_api(self):
        load_dotenv()
        self.api_url = os.getenv('SEVIMA_API_URL')
        self.grant_type = os.getenv('SEVIMA_API_GRANT_TYPE')
        self.client_id = os.getenv('SEVIMA_API_CLIENT_ID')
        self.client_secret = os.getenv('SEVIMA_API_CLIENT_SECRET')
        

    def saveTokenDetail(self, jsonToken):
        jsonToken['last_request'] = time.time()
        with open(TOKEN_FILENAME, 'w') as writer:
            json.dump(jsonToken, writer)


    def readStoredToken(self):
        access_token = None
        if os.path.isfile(TOKEN_FILENAME):
            with open(TOKEN_FILENAME, 'r') as reader:
                storedToken = json.load(reader)
                if check_token_availability(storedToken):
                    access_token = storedToken['access_token']
        return access_token


    def requestNewToken(self):
        self.get_sevima_api()
        auth_data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': self.grant_type,
        }
        access_token = ""
        getToken     = self.session.post("{0}/token".format(self.api_url), data = auth_data)
        if getToken.status_code == 200:
            jsonToken = getToken.json()
            if "access_token" in jsonToken:
                access_token = jsonToken['access_token']
                self.saveTokenDetail(jsonToken)
                print('DEBUG:', 'Request new token from sevima SEVIMA_API ...')
        return access_token


    def getAccessToken(self):
        access_token = self.readStoredToken()
        if not access_token:
            access_token = self.requestNewToken()
        return access_token


    def sendRequest(self, scope, query = {}, primary_key = None):
        self.access_token = self.getAccessToken()
        response = {
            'status': False,
            'message': '',
            'data': {},
        }
        scope_url = "{0}/{1}".format(self.api_url, scope)
        # when request is to get single data
        if primary_key:
            scope_url = "{0}/{1}/[{2}]".format(self.api_url, scope, primary_key)
        # when request is to get all data
        try:
            getResult = self.session.get(
                scope_url, params = query,
                auth = BearerAuth(self.access_token),
                timeout = 15,
            )
            if is_json(getResult.text):
                if getResult.status_code == 200:
                    jsonResult = getResult.json()
                    response['status'] = True
                    response['message'] = 'success'
                    response['data'] = jsonResult
                else:
                    jsonResult = getResult.json()
                    if jsonResult['error'].find('token') != -1:
                        response['message'] = jsonResult['error_message']
                        response['data'] = jsonResult
        except Exception as error:
            response['message'] = str(error)
        return response


    def getAllData(self, scope, **kwargs):
        responses = self.sendRequest(scope, query = kwargs)
        return responses


    def getSingleData(self, scope, **kwargs):
        responses = self.getAllData(scope, **kwargs)
        if (len(responses['data']) > 0):
            responses['data'] = responses['data'][0]
        return responses


    def getAllMahasiswa(self, **kwargs):
        responses = self.getAllData('datamahasiswa', **kwargs)
        return responses


    def getSingleMahasiswa(self, nim_mhs):
        response = self.getSingleData('datamahasiswa', nim_mhs = nim_mhs)
        return response


    def getAllDosen(self, **kwargs):
        responses = self.getAllData('datadosen', **kwargs)
        return responses


    def getSingleDosen(self, nidn):
        response = self.getSingleData('datadosen', nidn_dos = nidn)
        if not response['data']:
            response = self.getSingleData('datadosen', nip = nidn)
        return response


    def getAllUsers(self, **kwargs):
        responses = self.getAllData('datauserdetail', **kwargs)
        return responses


    def getSingleUser(self, username):
        response = self.getSingleData('datauserdetail', username = username)
        return response


    def getAllAKM(self, **kwargs):
        responses = self.getAllData('dataakmterakhir', **kwargs)
        return responses


    def getSingleAKM(self, nim_mhs):
        response = self.getSingleData('dataakmterakhir', nim_mhs = nim_mhs)
        return response


    def getAllUnit(self, **kwargs):
        responses = self.getAllData('dataunit', **kwargs)
        return responses


    def getSingleUnit(self, unit_id):
        response = self.getSingleData('dataunit', unit_id = unit_id)
        return response


    def getAllCurriculum(self, **kwargs):
        responses = self.getAllData('datakurikulum', **kwargs)
        return responses


# a = SevimaAPI()
# print(a.getAllData('pendaftar').get('data')[0])