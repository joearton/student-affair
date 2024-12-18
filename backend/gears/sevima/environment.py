from dotenv import load_dotenv
import os

# Memuat file .env
load_dotenv()

# Mengakses variabel lingkungan
siakadcloud_url = os.getenv('SIAKADCLOUD_URL')
signin_url = os.getenv('SIGNIN_URL')
liveapi = {
    "url": os.getenv('LIVEAPI_URL'),
    "grant_type": os.getenv('LIVEAPI_GRANT_TYPE'),
    "client_id": os.getenv('LIVEAPI_CLIENT_ID'),
    "client_secret": os.getenv('LIVEAPI_CLIENT_SECRET'),
}

print(siakadcloud_url)
print(liveapi)
