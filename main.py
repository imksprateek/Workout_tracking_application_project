import os
import requests
import datetime

#----------------------------------------------------VARIABLES&CONSTANTS----------------------------------------------------
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = "https://api.sheety.co/a85a19cc5c131644350165b2c5789239/myWorkouts/workouts"
TODAYS_DATE = datetime.datetime.now().today().date().strftime("%d/%m/%Y")
TIME_NOW = datetime.datetime.now().time().strftime("%H:%M:%S")

#----------------------------------------------------NUTRITIONIX REQUESTS----------------------------------------------------
input_string = input("What did you do today?: ")

nutritionix_params = {
    "query" : input_string,
    "gender" : "male",
    "weight_kg" : "80",
    "height_cm" : "182",
    "age" : "18"
}
nutritionix_header = {
    "x-app-id" : str(os.getenv("NUTRITIONIX_APP_ID")),
    "x-app-key" : str(os.getenv("NUTRITIONIX_API_KEY")),
}

nutritionix_response = requests.post(url=NUTRITIONIX_ENDPOINT, json=nutritionix_params, headers=nutritionix_header)
nutritionix_response.raise_for_status()
nutritionix_response_json = nutritionix_response.json()
print(nutritionix_response_json)

#----------------------------------------------------SHEETY REQUESTS----------------------------------------------------
sheety_header = {
    "Authorization" : "Bearer "+ os.getenv("SHEETY_BEARER_TOKEN")
}
for exercise in nutritionix_response_json["exercises"]:
    sheet_inputs = {
        "workout":{
            "date" : TODAYS_DATE,
            "time" : TIME_NOW,
            "exercise" : exercise["name"].title(),
            "duration" : exercise["duration_min"],
            "calories" : exercise["nf_calories"]
        }
    }
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=sheet_inputs, headers=sheety_header)
    sheety_response.raise_for_status()
    sheety_response_text = sheety_response.text
    print(sheety_response_text)

#I ran 4 miles in 1.5 hours and walked for half a mile