"""
credit: https://github.com/AlfredoSequeida/etext/ for making integration of the sms so easy
and https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j
for helping fix an issue regarding authentication

The job of this is to send my local weather forecast every morning via text because I'm usually too tired to figure out
how to dress for the day. the automation of this is handled by windows task scheduler.

objectives:

1. Get local weather via api request then convert json in to a dictonary to begin working on getting the info we need.
    1a. get current temperature and returns it's value
    1b. gets current date and returns it's value
    1c. gets minimum temperature for the day and returns it's value
    1d. gets maximum temperature for the day and returns it's value
2. Send a text to my phone
    2a. automate this
3. make a CLI so a user can enter their own info
4. BONUS: make a gui
"""
import requests
import json
from etext import send_sms_via_email


class textstorm:
    #TODO: Set up user input to make a custom query
    def get_user_input(self):
        api_key = input()
        pass

    def get_local_weather(self):
        # get api key from: https://www.weatherapi.com/
        key = "" # Enter your Api key here
        query = "" # Enter your city here
        days = "1" # Enter number of days of weather forecast. Value ranges from 1 to 10
        aqi = "no" # yes or no
        alerts = "no" # yes or no

        api_call = f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={query}&days={days}&aqi={aqi}&alerts={alerts}"
        print(api_call)
        response = requests.get(api_call)
        weather_json = response.text
        weather_dict = json.loads(weather_json)
        return weather_dict

    def get_city(self):
        get_city_dict = self.get_local_weather()
        current_city = ""
        for i in get_city_dict.keys():
            if i == "location":
                for key, value in get_city_dict[i].items():
                    if key == "name":
                        current_city = value
        return current_city

    def get_current_temp(self):
        current_temp_dict = self.get_local_weather()
        current_temp = ""
        for i in current_temp_dict.keys():
            if i == "current":
                for k,v in current_temp_dict[i].items():
                    if k == "temp_f":
                        current_temp = v
        return current_temp

    def get_date(self):
        max_temp_dict = self.get_local_weather()
        todays_date = ""
        # Here we are iterating through our api call to find information about our forecast
        for i in max_temp_dict.keys():
            if i == "forecast":
                # here we are looking for just today's forecast in the dictonary of information provided
                for j in max_temp_dict[i].keys():
                    if j == "forecastday":
                        # Iterating throughout list of dictonaries to find the date dictonary
                        for l in max_temp_dict[i][j]:
                            for k,v in l.items():
                                if k == "date":
                                    todays_date = v
        return todays_date

    def get_min_temp(self):
        min_temp_dict = self.get_local_weather()
        min_temp = 0
        # Here we are iterating through our api call to find information about our forecast
        for i in min_temp_dict.keys():
            if i == "forecast":
                # here we are looking for just today's forecast in the dictonary of information provided
                for j in min_temp_dict[i].keys():
                    if j == "forecastday":
                        # Iterating throughout list of dictonaries to find the date dictonary
                        for l in min_temp_dict[i][j]:
                            for k, v in l.items():
                                if k == "day":
                                    for key,value in v.items():
                                        if key == "mintemp_f":
                                            min_temp = value

        return min_temp

    def get_max_temp(self):
        max_temp_dict = self.get_local_weather()
        max_temp = 0
        # Here we are iterating through our api call to find information about our forecast
        for i in max_temp_dict.keys():
            if i == "forecast":
                # here we are looking for just today's forecast in the dictonary of information provided
                for j in max_temp_dict[i].keys():
                    if j == "forecastday":
                        # Iterating throughout list of dictonaries to find the date dictonary
                        for l in max_temp_dict[i][j]:
                            for k, v in l.items():
                                if k == "day":
                                    for key, value in v.items():
                                        if key == "maxtemp_f":
                                            max_temp = value
        return max_temp

    #TODO: Get whether it will rain and if it will send a notification
    def get_rain(self):
        pass

    def send_text_message(self, phone_number):
        min_temp = self.get_min_temp()
        max_temp = self.get_max_temp()
        today = self.get_date()
        city = self.get_city()
        current_temp = self.get_current_temp()
        provider = "" # Enter your credentials here
        sender_credentials = ("Enter email","Enter email app password")
        message = f"Today's date is: {today}:  The temperature in {city} is currently: {current_temp}F. The Minimum temp: {min_temp}F. The Maximum: {max_temp}F."
        #message = f"Today's date is {today}. The temperature in {city} is currently: {current_temp} Fahrenheit. \n\t The minimum temp will be: {min_temp} Fahrenheit.\n\t the maximum temp will be: {max_temp} Fahrenheit."
        send_sms_via_email(phone_number,message,provider,sender_credentials,subject="Daily weather")

def main():
    run = textstorm()
    # provide a phone number as an argument
    run.send_text_message()


if __name__ == "__main__":
    main()