from selenium import webdriver
from selenium.webdriver.common.keys import Keys # To be able to click buttons and etc..
import time

class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Firefox()  # Will open a Firefox page

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/')
        time.sleep(1) # to wait for the page to load


username = ''
password = ''
nerdo = TwitterBot(username, password)