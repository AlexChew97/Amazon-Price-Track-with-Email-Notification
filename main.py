import os
from bs4 import BeautifulSoup
import requests
from smtplib import SMTP

headers = {
    "User-Agent": os.environ["user_agent"],
    "Accept-Language": "en-US,en;q=0.9",
}
url = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463&th=1"
respnose = requests.get(url, headers=headers)
soup = BeautifulSoup(respnose.text, "html.parser")
price = soup.find(name="span", class_="olpWrapper").getText()
price_float = float(price.split("$")[1])
title = soup.find(name="span", id="productTitle").getText()
message = f"Subject:Amazon Price Alert!\n\n{title.strip()} is now ${price_float}\n{url}"

my_email = os.environ["my_email"]
my_pass = os.environ["my_pass"]
send_email = os.environ["send_email"]
if price_float < 100:
    with SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, my_pass)
        connection.sendmail(my_email, send_email, message.encode("utf-8"))
