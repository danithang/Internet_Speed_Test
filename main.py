from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import smtplib
import time as t
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_EMAIL = os.getenv("GOOGLE_EMAIL")
PASSWORD = os.getenv("GOOGLE_PASSWORD")
YAHOO_EMAIL = os.getenv("YAHOO_EMAIL")

# setting the options for the webdriver to make it headless
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


class InternetSpeed:
    def __init__(self):
        self.down = 0
        self.up = 0
        self.service = Service(executable_path="chromedriver.exe", log_path="NUL")
        self.driver = webdriver.Chrome(options=options, service=self.service)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        t.sleep(2)
        go_button = self.driver.find_element(By.CLASS_NAME, "start-text")
        go_button.click()
        t.sleep(60)
        self.down = float(self.driver.find_element(By.CLASS_NAME, "download-speed").text)
        self.up = float(self.driver.find_element(By.CLASS_NAME, "upload-speed").text)

    def email_speeds(self):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            # start transport layer security to secure the connection to the email server
            connection.starttls()
            # login process
            connection.login(user=GOOGLE_EMAIL, password=PASSWORD)
            # sending the email from one address to the other with message...adding subject and /n to make
            # sure it doesn't go into spam box
            connection.sendmail(from_addr=GOOGLE_EMAIL, to_addrs=YAHOO_EMAIL,
                                msg=f"Subject:Internet Speeds\n\nDownload Speed: {self.down}\nUpload Speed: {self.up}")

    def quit(self):
        self.driver.quit()


bot = InternetSpeed()
bot.get_internet_speed()
bot.email_speeds()
bot.quit()
