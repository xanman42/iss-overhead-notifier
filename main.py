import requests
from datetime import datetime
import smtplib
import time

MY_LAT = -25.747868  # Your latitude
MY_LONG = 28.229271  # Your longitude

email = 'xanderpython1@gmail.com'
password = 'wrhqffdfbtvdmuim'


def is_close():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    # Your position is within +5 or -5 degrees of the ISS position.
    if iss_latitude - 5 < MY_LAT < iss_latitude + 5 and iss_longitude - 5 < MY_LONG < iss_longitude + 5:
        return True


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    if time_now > sunset or time_now < sunrise:
        return True


def send_mail():
    if is_close() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs='xanderkirsten3@gmail.com',
                msg='Subject:ISS notifier\n\nGo outside and look up, the ISS is visible where you are.'
            )


while True:
    send_mail()
    time.sleep(60)
# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
