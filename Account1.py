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
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class FacebookAccountCreator:
    def __init__(self):
        self.driver = None
        self.profile_info = {}
        
    def setup_driver(self):
        """Set up Firefox driver with Tor configuration"""
        firefox_options = Options()
        firefox_options.headless = True
        firefox_options.set_preference('network.proxy.type', 1)
        firefox_options.set_preference('network.proxy.socks', '127.0.0.1')
        firefox_options.set_preference('network.proxy.socks_port', 9150)
        firefox_options.binary_location = r'C:\Users\ASUS\Desktop\Tor Browser\Browser\firefox.exe'
        
        self.driver = webdriver.Firefox(options=firefox_options)
        time.sleep(5)
        
        # Handle Tor connection
        body = self.driver.find_element(By.TAG_NAME, 'body')
        body.send_keys(Keys.ESCAPE)
        
        connect_button = self.driver.find_element(By.ID, "connectButton")
        connect_button.click()
        time.sleep(20)
    
    def generate_password(self, length=12):
        """Generate strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_gender(self):
        """Randomly select gender"""
        return random.choice(['Male', 'Female'])
    
    def generate_name_from_csv(self, gender):
        """Generate first name based on gender from CSV files"""
        filename = 'ww/ww.csv' if gender == 'Female' else 'bb/wb.csv'
        names, probabilities = [], []
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        probabilities.append(float(row[0]))
                        names.append(row[1])
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Using default names.")
            return "Sarah" if gender == 'Female' else "Mohamed"
        
        return random.choices(names, weights=probabilities)[0] if names else "DefaultName"
    
    def generate_last_name_from_csv(self):
        """Generate last name from CSV file"""
        names, probabilities = [], []
        
        try:
            with open('lastNames.csv', 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        names.append(row[0])
                        probabilities.append(float(row[1]))
        except FileNotFoundError:
            print("Warning: lastNames.csv not found. Using default last name.")
            return "Smith"
        
        return random.choices(names, weights=probabilities)[0] if names else "DefaultLastName"
    
    def get_temp_email(self):
        """Get temporary email from fakemailgenerator.com"""
        self.driver.get("https://www.fakemailgenerator.com/")
        self.driver.execute_script("window.stop();")
        
        email_input = self.driver.find_element(By.ID, "home-email")
        email = email_input.get_attribute("value")
        
        domain_button = self.driver.find_element(By.ID, "domain-select")
        domain = domain_button.text.strip()
        
        return email + domain
    
    def fill_facebook_form(self):
        """Fill Facebook registration form"""
        # Open Facebook in new tab
        self.driver.execute_script("window.open('about:blank','_blank');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get('https://www.facebook.com/')
        time.sleep(3)
        
        # Accept cookies
        try:
            cookie_button = self.driver.find_element(
                By.CSS_SELECTOR, 
                'button[data-cookiebanner="accept_button"][title="Allow all cookies"]'
            )
            cookie_button.click()
        except NoSuchElementException:
            print("Cookie accept button not found.")
        
        # Click create account button
        self.driver.find_element(By.CLASS_NAME, "_4jy2").click()
        
        wait = WebDriverWait(self.driver, 50)
        
        # Wait for form elements
        firstname = wait.until(EC.visibility_of_element_located((By.NAME, "firstname")))
        lastname = self.driver.find_element(By.NAME, "lastname")
        email_field = self.driver.find_element(By.NAME, "reg_email__")
        password_field = self.driver.find_element(By.NAME, "reg_passwd__")
        birthday_day = self.driver.find_element(By.NAME, "birthday_day")
        birthday_month = self.driver.find_element(By.NAME, "birthday_month")
        birthday_year = self.driver.find_element(By.NAME, "birthday_year")
        gender_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'span._5k_2._5dba')
        
        # Fill basic information
        firstname.send_keys(self.profile_info["First Name"])
        lastname.send_keys(self.profile_info["Last Name"])
        email_field.send_keys(self.profile_info["Email"])
        
        time.sleep(1)
        
        # Handle email confirmation field if present
        try:
            email_confirmation = self.driver.find_element(By.NAME, "reg_email_confirmation__")
            email_confirmation.send_keys(self.profile_info["Email"])
        except NoSuchElementException:
            pass
        
        password_field.send_keys(self.profile_info["Password"])
        
        # Fill birthday information
        day = random.randint(1, 28)
        month = random.choice(["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
        year = random.randint(1988, 2005)
        
        birthday_month.send_keys(month)
        
        ActionChains(self.driver).move_to_element(birthday_day).click().perform()
        self.driver.find_element(By.XPATH, f'//option[@value="{day}"]').click()
        
        ActionChains(self.driver).move_to_element(birthday_year).click().perform()
        self.driver.find_element(By.XPATH, f'//option[@value="{year}"]').click()
        
        # Select gender
        if self.profile_info["Gender"] == 'Female':
            gender_buttons[0].find_element(By.CSS_SELECTOR, 'input[value="1"]').click()
        else:
            gender_buttons[1].find_element(By.CSS_SELECTOR, 'input[value="2"]').click()
        
        # Submit form
        self.driver.find_element(By.NAME, 'websubmit').click()
        time.sleep(5)
    
    def get_confirmation_code(self):
        """Get confirmation code from temporary email"""
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.refresh()
        
        try:
            confirmation_element = WebDriverWait(self.driver, 300).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//dd[contains(text(), "Facebook confirmation code")]')
                )
            )
            code = confirmation_element.text.split(' ')[0].replace("FB-", "")
            print(f"Confirmation code: {code}")
            return code
        except TimeoutException:
            print("Timeout waiting for confirmation code")
            return None
    
    def enter_confirmation_code(self, code):
        """Enter confirmation code on Facebook"""
        if not code:
            return False
            
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        try:
            input_field = self.driver.find_element(By.ID, "code_in_cliff")
            input_field.send_keys(code)
            
            continue_button = self.driver.find_element(
                By.CSS_SELECTOR, 
                'button._42ft.mls._4jy0._8iu3._8iu6._4jy4._4jy1.selected._51sy'
            )
            continue_button.click()
            return True
        except NoSuchElementException:
            print("Confirmation input field not found")
            return False
    
    def follow_page(self):
        """Follow target Facebook page"""
        time.sleep(15)
        self.driver.get("https://www.facebook.com/ItzMouhLaad")
        time.sleep(5)
        
        try:
            menu_button = self.driver.find_element(
                By.XPATH, 
                '//div[@aria-label="See options"]'
            )
            menu_button.click()
            time.sleep(3)
            
            follow_option = self.driver.find_element(
                By.XPATH, 
                '//span[text()="Follow"]'
            )
            follow_option.click()
            print(f"{self.profile_info['Email']} followed you")
            return True
        except NoSuchElementException:
            print("Follow button not found")
            return False
    
    def save_account_info(self):
        """Save account information to JSON file"""
        try:
            # Read existing accounts if file exists
            try:
                with open("accounts.json", "r", encoding='utf-8') as f:
                    existing_accounts = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_accounts = []
            
            # Ensure existing_accounts is a list
            if not isinstance(existing_accounts, list):
                existing_accounts = [existing_accounts]
            
            # Add new account
            existing_accounts.append(self.profile_info)
            
            # Save updated list
            with open("accounts.json", "w", encoding='utf-8') as f:
                json.dump(existing_accounts, f, indent=2)
            
            print("Profile information saved to accounts.json file.")
        except Exception as e:
            print(f"Error saving account info: {e}")
    
    def create_account(self):
        """Main method to create Facebook account"""
        try:
            # Setup driver
            self.setup_driver()
            
            # Generate profile information
            gender = self.generate_gender()
            first_name = self.generate_name_from_csv(gender)
            last_name = self.generate_last_name_from_csv()
            
            self.profile_info = {
                "Email": self.get_temp_email(),
                "Password": self.generate_password(),
                "First Name": first_name,
                "Last Name": last_name,
                "Gender": gender,
                "Created_At": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            print("Generated Profile Info:")
            print(json.dumps(self.profile_info, indent=2))
            
            # Fill Facebook form
            self.fill_facebook_form()
            
            # Get and enter confirmation code
            confirmation_code = self.get_confirmation_code()
            if confirmation_code:
                self.enter_confirmation_code(confirmation_code)
                
                # Follow target page
                self.follow_page()
                
                # Save account information
                self.save_account_info()
            else:
                print("Failed to get confirmation code")
            
            return True
            
        except Exception as e:
            print(f"Error during account creation: {e}")
            return False
        finally:
            # Cleanup
            if self.driver:
                self.driver.quit()
    
    def create_multiple_accounts(self, count=1):
        """Create multiple Facebook accounts"""
        successful_creations = 0
        
        for i in range(count):
            print(f"\n=== Creating Account {i+1}/{count} ===")
            
            if self.create_account():
                successful_creations += 1
            
            # Wait between account creations
            if i < count - 1:
                wait_time = random.randint(30, 60)
                print(f"Waiting {wait_time} seconds before next creation...")
                time.sleep(wait_time)
        
        print(f"\n=== Completed: {successful_creations}/{count} accounts created successfully ===")

def main():
    """Main execution function"""
    creator = FacebookAccountCreator()
    
    # Create single account
    # creator.create_account()
    
    # Create multiple accounts (change the number as needed)
    creator.create_multiple_accounts(count=1)

if __name__ == "__main__":
    main()
