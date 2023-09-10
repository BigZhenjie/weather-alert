import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient



# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'exmaplesid'
auth_token = 'exmapleauth'
client = Client(account_sid, auth_token)

api_key = "exampleapikey"

sf_parameters = {
    "lat":37.774929,
    "lon":-122.419418,
    "exclude": "current,minutely,hourly",
    "appid": api_key,
    "units": "imperial",

}

# slo_parameters = {
#     "lat":35.270378,
#     "lon":-120.680656,
#     "exclude": "current,minutely,hourly",
#     "appid": api_key,
#     "units": "imperial",

# }
OWM_endpoint = "https://api.openweathermap.org/data/2.5/onecall"


sf_data = requests.get(url = OWM_endpoint, params = sf_parameters)
# slo_data = requests.get(url = OWM_endpoint, params = slo_parameters)



sf_data.raise_for_status()
sf_data_json = sf_data.json()

# slo_data.raise_for_status()
# slo_data_json = slo_data.json()

sf_will_rain = False
sf_data_slice = sf_data_json["daily"][0]

# slo_will_rain = False
# slo_data_slice = slo_data_json["daily"][0]



sf_max_f = sf_data_slice["temp"]["max"]
sf_min_f = sf_data_slice["temp"]["min"]

# slo_max_f = slo_data_slice["temp"]["max"]
# slo_min_f = slo_data_slice["temp"]["min"]


if sf_data_slice["weather"][0]["id"] < 700:
    sf_will_rain = True

# if slo_data_slice["weather"][0]["id"] < 700:
#     slo_will_rain = True

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https':os.environ['https_proxy']}
client = Client(account_sid, auth_token, http_client = proxy_client)

# if slo_will_rain or sf_will_rain:
#     message = client.messages.create(to="+14157340673", from_='+18155423240', body=f'----------------\nRainning in SF: {sf_will_rain} --- SLO: {slo_will_rain}\nTemp for SF: Max Temp: {str(sf_max_f)}\nMin Temp: {str(sf_min_f)}\nTemp for SLO: Max Temp: {str(slo_max_f)}\nMin Temp: {str(slo_min_f)}')
# else:
#     message = client.messages.create(to="+14157340673", from_='+18155423240', body=f'----------------\nTemp for SF: Max Temp: {str(sf_max_f)}\nMin Temp: {str(sf_min_f)}\nTemp for SLO: Max Temp: {str(slo_max_f)}\nMin Temp: {str(slo_min_f)}')

if slo_will_rain or sf_will_rain:
    message = client.messages.create(to="+14157340673", from_='+18155423240', body=f'----------------\nRainning in SF: {sf_will_rain} --- SLO: {slo_will_rain}\nTemp for SF: Max Temp: {str(sf_max_f)}\nMin Temp: {str(sf_min_f)}')
else:
    message = client.messages.create(to="+14157340673", from_='+18155423240', body=f'----------------\nTemp for SF: Max Temp: {str(sf_max_f)}\nMin Temp: {str(sf_min_f)}')




