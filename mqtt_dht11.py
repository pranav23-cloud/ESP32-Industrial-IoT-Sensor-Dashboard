import requests

API_KEY = "d55b760fb402a924acc8a4db23a48d4e"

url = "https://www.thingsay.com/api/get/2400ede70d2b/2224"

params = {
    "key": API_KEY
}

response = requests.get(url, params=params)

print("Status:", response.status_code)
print("Response:", response.text)