import requests
import hmac
import hashlib
import time
import AccessToken
# Credentials
ACCESS_ID = "jrhutams3vc49ge8qvfk"
ACCESS_SECRET = "9d9ca40de6b74ea399e80a3d5a2f41af"
ACCESS_TOKEN = AccessToken.accessToken 
DEVICE_ID = "d7ff5afbf3888a86880trt"
BASE_URL = "https://openapi.tuyain.com"

# Timestamp
t = int(time.time() * 1000)

# Sign calculation
def generate_sign(method, path):
    str_to_sign = method + "\n" + hashlib.sha256("".encode("utf-8")).hexdigest() + "\n\n" + path
    message = ACCESS_ID + ACCESS_TOKEN + str(t) + str_to_sign
    return hmac.new(ACCESS_SECRET.encode("utf-8"), msg=message.encode("utf-8"), digestmod=hashlib.sha256).hexdigest().upper()

# Headers
def get_headers(path):
    return {
        "client_id": ACCESS_ID,
        "sign_method": "HMAC-SHA256",
        "t": str(t),
        "access_token": ACCESS_TOKEN,
        "sign": generate_sign("GET", path),
        "Content-Type": "application/json",
    }

# Check if the device is online
device_info_path = f"/v1.0/iot-03/devices/{DEVICE_ID}"
device_info_url = f"{BASE_URL}{device_info_path}"

response = requests.get(device_info_url, headers=get_headers(device_info_path), timeout=5)

if response.status_code == 200:
    device_info = response.json()
    
    if not device_info.get("success"):
        print(f"Failed to check device status: {device_info.get('msg', 'Unknown error')}")
    else:
        is_online = device_info.get("result", {}).get("online", False)

        if not is_online:
            print("The gateway is powered off or offline.")
        else:
            # Device is online, get the status
            status_path = f"/v1.0/iot-03/devices/{DEVICE_ID}/status"
            status_url = f"{BASE_URL}{status_path}"
            
            response = requests.get(status_url, headers=get_headers(status_path), timeout=5)

            if response.status_code == 200:
                data = response.json()
                
                if not data.get("success"):
                    print(f"Failed to fetch data: {data.get('msg', 'Unknown error')}")
                else:
                    status_list = data.get("result", [])
                    Temperature = None
                    Humidity = None

                    # Extract Temp and Hum sensor status value
                    for status in status_list:
                        if status["code"] == "va_temperature":
                            Temperature = round(status["value"] / 10, 1)  # 194 -> 19.4
                        elif status["code"] == "va_humidity":
                            Humidity = round(status["value"] / 10, 1)  # 402 -> 40.2

                    # Output only the Temp and Hum sensor status value
                    if Temperature is not None and Humidity is not None:
                        print(f"Temperature: {Temperature}°C")
                        print(f"Humidity: {Humidity}%")
                    else:
                        print("No valid data received. The gateway might be offline.")
            else:
                print("HTTP Error:", response.status_code, response.text)
else:
    print("HTTP Error:", response.status_code, response.text)

def getTemperature():
    return Temperature
def getHumidity():
    return Humidity
