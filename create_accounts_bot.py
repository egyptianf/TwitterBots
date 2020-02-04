from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# To be able to click buttons and etc..
from selenium.webdriver.common.keys import Keys
import time
from cryptography.fernet import Fernet
import string
import os
import sys
from random import *


def create(previous_mail, _username, _password):
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(1)

    driver.find_element_by_id('password').send_keys(_password)
    driver.find_element_by_id('passwordc').send_keys(_password)

    iframe0 = driver.find_elements_by_tag_name('iframe')[0]
    driver.switch_to.frame(iframe0)
    driver.implicitly_wait(4)
    driver.find_element_by_id('username').send_keys(_username)
    driver.switch_to.default_content()

    iframe1 = driver.find_elements_by_tag_name('iframe')[1]
    driver.switch_to.frame(iframe1)
    driver.implicitly_wait(5)
    create_button = driver.find_element_by_name('submitBtn')
    create_button.send_keys(Keys.RETURN)
    driver.switch_to.default_content()

    # Now confirm
    driver.find_element_by_id('confirmModalBtn').send_keys(Keys.RETURN)

    # Select verification by email
    driver.find_element_by_id('id-signup-radio-email').click()
    driver.find_element_by_id('emailVerification').send_keys(previous_mail)
    time.sleep(1)
    driver.find_element_by_class_name(
        'pm_button.primary.codeVerificator-btn-send').click()

    # Now we should login with the previous email, get the verification code, then write it in the box


def create_first_email(username, _password):
    create(base_email, username, _password)


def generate_random_password(_size):
    charcters = string.ascii_letters + string.punctuation + string.digits
    _password = "".join(choice(charcters) for x in range(_size))
    return _password


def read_key(key_path):
    try:
        with open(key_path, 'rb') as file:
            key = file.read()
            return key
    except IOError as ioe:
        print(ioe)
    return None


def encrypt(_password, _key):
    message = _password.encode()
    f = Fernet(_key)
    return f.encrypt(message)


def decrypt(_encrypted, _key):
    f = Fernet(_key)
    decrypted = f.decrypt(_encrypted)
    return decrypted.decode()


def save_account(_username, _encrypted_pass):
    with open('login_data.txt', 'a') as names_file:
        names_file.write(_username + os.linesep)
    with open('passwords.bin', 'ab') as passes_file:
        passes_file.write(_encrypted_pass)


def main():
    url = 'https://mail.protonmail.com/create/new?language=en'
    base_email = 'your base email'

    # Read our encryption key
    current_path = os.getcwd()
    key_path = current_path + '/key.key'
    key = None
    if read_key(key_path) is not None:
        key = read_key(key_path)
    else:
        sys.exit("Key is None and this cannot happen. Terminating....")

    # First email creation
    username = 'randomuser1'
    password = generate_random_password(13)
    encrypted = encrypt(password, key)
    # We need to save the password encrypted
    save_account(username, encrypted)

    create_first_email(username, password)


if __name__ == "__main__":
    pass
