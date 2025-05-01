#Get access token from tuya

import hashlib
import hmac
import time
import requests

# Tuya API Credentials (Replace these with actual values)
ACCESS_ID = "jrhutams3vc49ge8qvfk"
ACCESS_SECRET = "9d9ca40de6b74ea399e80a3d5a2f41af"
ENDPOINT = "https://openapi.tuyain.com"  # Change based on your region

# Timestamp
t = int(time.time() * 1000)

# Correct API Path
path = "/v1.0/token?grant_type=1"  # Fix: Correct token path

# Sign Calculation
method = "GET"  # Fix: Tuya uses GET for token requests
str_to_sign = f"{method}\n{hashlib.sha256(b'').hexdigest()}\n\n{path}"
message = f"{ACCESS_ID}{t}{str_to_sign}"

sign = hmac.new(
    ACCESS_SECRET.encode("utf-8"),
    msg=message.encode("utf-8"),
    digestmod=hashlib.sha256,
).hexdigest().upper()

# Headers
headers = {
    "client_id": ACCESS_ID,
    "sign_method": "HMAC-SHA256",
    "t": str(t),
    "sign": sign,
}

# Request the token
response = requests.get(f"{ENDPOINT}{path}", headers=headers)  # Fix: Changed to GET
data = response.json()

# Output response
print(data)
accessToken=data['result']['access_token']
