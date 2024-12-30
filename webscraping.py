import time
import requests
import selectorlib
from sendemail import send_email
import sqlite3
import smtplib,ssl
import os


#Establish a connection and cursor
#connection=sqlite3.connect("data1_db.db")

URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}



class Event:

    def scrap(self,url):
        """Scrape the page resource from url"""
        response=requests.get(url,headers=HEADERS)
        source=response.text
        return source

    def extract(self,source):
        extractor=selectorlib.Extractor.from_yaml_file("extract.yaml")
        value=extractor.extract(source)["tours"]
        return value


class Email:

    def send(self,message):
        host = "smtp.gmail.com"
        port = 465

        username = "saurabhlively@gmail.com"
        password = "tvhenlwfjbcvllbj"

        receiver = "saurabhlively@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host,port,context=context) as server:
            server.login(username,password)
            server.sendmail(username,receiver,message)
            print("Email sent")

class Database:

    def __init__(self,database_path):
        self.connection = sqlite3.connect("database_path")

    def store(self,extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        cursor = self.connection.cursor()
        cursor.execute("INSERT into events VALUES(?,?,?)", row)
        self.connection.commit()


    def read(self,extracted):
        row = extracted.split(",")
        row = [item.strip() for item in row]
        Band,city,datetime = row
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from events where Band = ? and city = ?",(Band,city))
        rows = cursor.fetchall()
        print(rows)
        return rows


"""Running non stop"""
if __name__ == "__main__":
    while True:
        event=Event()
        email = Email()
        scraped = event.scrap(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            database = Database(database_path="data2_db.db")
            row = database.read(extracted)
            if not row:
                database.store(extracted)
                email = Email()
                email.send(message="Hey Saurabh! New event was found")
        time.sleep(2)


