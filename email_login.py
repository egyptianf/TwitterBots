from create_accounts_bot import read_key
from create_accounts_bot import decrypt
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys


def read_names(_names_file):
    names = []
    try:
        with open(_names_file, 'r') as names_file:
            data = names_file.readlines()
            for row in data:
                names.append(row)
            return names
    except IOError as ioe:
        print(ioe)


def read_passwords(_passes_file):
    passes = []
    try:
        with open(_passes_file, 'rb') as passes_file:
            data = passes_file.readlines()
            for row in data:
                passes.append(row)
            return passes
    except IOError as ioe:
        print(ioe)


def login(_driver, _name, _password):
    _driver.find_element_by_id('username').send_keys(_name)
    _driver.find_element_by_id('password').send_keys(_password)
    _driver.find_element_by_id('login_btn').send_keys(Keys.RETURN)


def main():
    # Read our encryption key
    current_path = os.getcwd()
    key_path = current_path + '/key.key'
    key = read_key(key_path)

    # Read the email and password and decrypt the password
    names = read_names(current_path + '/login_data.txt')
    encrypted_passes = read_passwords(current_path + '/passwords.bin')

    # Decrypt the password
    passes = []
    for encrypted in encrypted_passes:
        passes.append(decrypt(encrypted, key))

    if len(passes) != len(names):
        sys.exit("Some names do not have passwords or vice versa.")

    # Now we connect to protonmail with these names and passwords
    url = "https://mail.protonmail.com/login"
    driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(1)
    for i in range(len(names)):
        # This will open a new tab
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        driver.get(url)
        time.sleep(2)
        # Make our login
        login(driver, names[i], passes[i])
        time.sleep(10)
        # Close the tab
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
    driver.close()


if __name__ == "__main__":
    main()
