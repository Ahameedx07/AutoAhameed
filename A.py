import csv
import json
import random
import string
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_gender():
    return random.choice(['Male', 'Female'])

def generate_name_from_csv(gender):
    filename = 'ww/ww.csv' if gender == 'Female' else 'bb/wb.csv'
    names, probabilities = [], []
    with open(filename) as f:
        reader = csv.reader(f)
        for row in reader:
            probabilities.append(float(row[0]))
            names.append(row[1])
    return random.choices(names, weights=probabilities)[0]

def generate_last_name_from_csv():
    names, probabilities = [], []
    with open('lastNames.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            names.append(row[0])
            probabilities.append(float(row[1]))
    return random.choices(names, weights=probabilities)[0]

def main():
    firefox_options = Options()
    firefox_options.headless = True  # ✅ Xvfb আর লাগবে না
    firefox_options.set_preference('network.proxy.type', 1)
    firefox_options.set_preference('network.proxy.socks', '127.0.0.1')
    firefox_options.set_preference('network.proxy.socks_port', 9150)
    firefox_options.binary_location = r'C:\\Users\\ASUS\\Desktop\\Tor Browser\\Browser\\firefox.exe'

    driver = webdriver.Firefox(options=firefox_options)
    time.sleep(5)

    # Escape key টা selenium দিয়েই
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.ESCAPE)

    connect_button = driver.find_element(By.ID, "connectButton")
    connect_button.click()
    time.sleep(20)

    driver.get("https://www.fakemailgenerator.com/")
    driver.execute_script("window.stop();")

    email_input = driver.find_element(By.ID, "home-email")
    email = email_input.get_attribute("value")
    domain_button = driver.find_element(By.ID, "domain-select")
    domain = domain_button.text.strip()
    gender = generate_gender()
    first_name = generate_name_from_csv(gender)
    last_name = generate_last_name_from_csv()
    password = generate_password()

    profile_info = {
        "Email": email + domain,
        "Password": password,
        "First Name": first_name,
        "Last Name": last_name,
        "Gender": gender
    }

    print(json.dumps(profile_info))

    driver.execute_script("window.open('about:blank','_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get('https://www.facebook.com/')
    time.sleep(3)

    try:
        button = driver.find_element(By.CSS_SELECTOR, 'button[data-cookiebanner="accept_button"][title="Allow all cookies"]')
        button.click()
    except NoSuchElementException:
        print("Cookie accept button not found.")

    driver.find_element(By.CLASS_NAME, "_4jy2").click()
    wait = WebDriverWait(driver, 50)
    firstname = wait.until(EC.visibility_of_element_located((By.NAME, "firstname")))
    lastname = driver.find_element(By.NAME, "lastname")
    email_field = driver.find_element(By.NAME, "reg_email__")
    password_field = driver.find_element(By.NAME, "reg_passwd__")
    birthday_day = driver.find_element(By.NAME, "birthday_day")
    birthday_month = driver.find_element(By.NAME, "birthday_month")
    birthday_year = driver.find_element(By.NAME, "birthday_year")
    gender_buttons = driver.find_elements(By.CSS_SELECTOR, 'span._5k_2._5dba')

    firstname.send_keys(first_name)
    lastname.send_keys(last_name)
    email_field.send_keys(profile_info["Email"])
    time.sleep(1)
    try:
        email_confirmation = driver.find_element(By.NAME, "reg_email_confirmation__")
        email_confirmation.send_keys(profile_info["Email"])
    except NoSuchElementException:
        pass

    password_field.send_keys(password)
    day = random.randint(1, 28)
    month = random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                           "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    year = random.randint(1988, 2005)

    birthday_month.send_keys(month)
    ActionChains(driver).move_to_element(birthday_day).click().perform()
    driver.find_element(By.XPATH, f'//option[@value="{day}"]').click()
    ActionChains(driver).move_to_element(birthday_year).click().perform()
    driver.find_element(By.XPATH, f'//option[@value="{year}"]').click()

    if gender == 'Female':
        gender_buttons[0].find_element(By.CSS_SELECTOR, 'input[value="1"]').click()
    else:
        gender_buttons[1].find_element(By.CSS_SELECTOR, 'input[value="2"]').click()

    driver.find_element(By.NAME, 'websubmit').click()
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[0])
    driver.refresh()
    confirmation = WebDriverWait(driver, 300).until(
        EC.visibility_of_element_located((By.XPATH, '//dd[contains(text(), "Facebook confirmation code")]'))
    )
    code = confirmation.text.split(' ')[0].replace("FB-", "")
    print(f"Confirmation code: {code}")

    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(By.ID, "code_in_cliff").send_keys(code)
    driver.find_element(By.CSS_SELECTOR, 'button._42ft.mls._4jy0._8iu3._8iu6._4jy4._4jy1.selected._51sy').click()

    time.sleep(15)
    driver.get("https://www.facebook.com/ItzMouhLaad")
    time.sleep(5)
    driver.find_element(By.XPATH, '//div[@aria-label="See options"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//span[text()="Follow"]').click()
    print(f"{profile_info['Email']} followed you")

    with open("accounts.json", "w") as f:
        json.dump(profile_info, f)

    print("Saved profile info.")
    driver.quit()

if __name__ == "__main__":
    main()
