import requests
from datetime import datetime
import smtplib
import os

MY_LAT = -21.045485
MY_LONG = -40.831738

MY_EMAIL = os.environ.get('SMTP_EMAIL', None)
MY_PASSWORD = os.environ.get('SMTP_PASSWORD', None)


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(f"ISS Latitude: {iss_latitude}")
    print(f"ISS Longitude: {iss_longitude}")

    if MY_LAT - 5 <= iss_latitude >= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude >= MY_LONG + 5:
        print("Is over head!")
        return True

    print("Is not over head!")

def is_night():
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

    if time_now <= sunrise or time_now >= sunset:
        print("Is night!")
        return True

    print("Is not night!")


if is_iss_overhead() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=MY_EMAIL,
        msg="Subject: Look Up\n\nThe ISS is above you in the sky."
    )

exit(0)
