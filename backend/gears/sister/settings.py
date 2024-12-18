import os
import json
from dotenv import load_dotenv


BASE_DIR     = os.path.dirname(__file__)
CACHE_DIR    = os.path.join(BASE_DIR, '.cache')
CONFIG_DIR   = os.path.join(BASE_DIR, 'config')
CONFIG_FILE  = os.path.join(CONFIG_DIR, 'config.json')
API_KEY_FILE = os.path.join(CACHE_DIR, 'api_key.json')


if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


STATUS_SUCCESS_WITH_REPLY   = 200
STATUS_SUCCESS              = STATUS_SUCCESS_WITH_REPLY
STATUS_SUCCESS_NO_REPLY     = 204
STATUS_REQ_INVALID          = 400
STATUS_TOKEN_INVALID        = 401
STATUS_CHANGES_DENIED       = 403
STATUS_ENDPOINT_NOTFOUND    = 404
STATUS_HTTP_DENIED          = 405
STATUS_ENDPOINT_EXIST       = 409
STATUS_ERROR                = 500


HTTP_METHOD_GET     = 'get'
HTTP_METHOD_POST    = 'post'
HTTP_METHOD_PATCH   = 'patch'
HTTP_METHOD_DELETE  = 'delete'


def save_config_to_json():
    # Memuat variabel lingkungan dari file .env
    load_dotenv()
    config_data = {
        "sister_url"    : os.getenv('SISTER_API_URL'),
        "use_sandbox"   : os.getenv('SISTER_API_USE_SANDBOX') == 'true',  # Konversi string 'true' menjadi boolean
        "username"      : os.getenv('SISTER_API_USERNAME'),
        "password"      : os.getenv('SISTER_API_PASSWORD'),
        "id_pengguna"   : os.getenv('SISTER_API_ID_PENGGUNA')
    }

    with open(config_filename, 'w') as json_file:
        json.dump(config_data, json_file, indent=4)


config_filename = os.path.join(CONFIG_DIR, 'config.json')
if not os.path.isfile(config_filename):
    save_config_to_json()
