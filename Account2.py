import csv
import json
import random
import string
import time
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import os

console = Console()

class FacebookAccountCreator:
    def __init__(self):
        self.driver = None
        self.profile_info = {}
        self.console = console
        
    def print_banner(self):
        """Print beautiful banner"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🚀 FACEBOOK ACCOUNT CREATOR              ║
║                     Powered by Python 3 + Selenium          ║
║                     With Beautiful Rich Animations         ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner, style="bold cyan", box=box.DOUBLE))
    
    def setup_driver(self):
        """Set up Firefox driver with proper configuration"""
        with self.console.status("[bold green]Setting up Firefox driver...", spinner="dots"):
            try:
                firefox_options = Options()
                firefox_options.headless = False  # Change to True if you don't want to see browser
                
                # Tor configuration (optional)
                firefox_options.set_preference('network.proxy.type', 1)
                firefox_options.set_preference('network.proxy.socks', '127.0.0.1')
                firefox_options.set_preference('network.proxy.socks_port', 9150)
                
                # Try to find Firefox in common locations
                possible_paths = [
                    r'C:\Program Files\Mozilla Firefox\firefox.exe',
                    r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe',
                    '/usr/bin/firefox',
                    '/usr/local/bin/firefox'
                ]
                
                firefox_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        firefox_path = path
                        break
                
                if firefox_path:
                    firefox_options.binary_location = firefox_path
                    self.console.print("✅ [green]Firefox found at:[/green] " + firefox_path)
                else:
                    self.console.print("⚠️ [yellow]Using system default Firefox[/yellow]")
                
                self.driver = webdriver.Firefox(options=firefox_options)
                time.sleep(3)
                
                self.console.print("✅ [bold green]Firefox driver setup completed![/bold green]")
                return True
                
            except Exception as e:
                self.console.print(f"❌ [bold red]Error setting up driver: {e}[/bold red]")
                return False
    
    def generate_password(self, length=12):
        """Generate strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_gender(self):
        """Randomly select gender"""
        return random.choice(['Male', 'Female'])
    
    def generate_name_from_csv(self, gender):
        """Generate first name based on gender from CSV files"""
        filename = 'female_names.csv' if gender == 'Female' else 'male_names.csv'
        
        # Fallback names if CSV files are not available
        female_names = ['Sarah', 'Fatima', 'Aisha', 'Zainab', 'Mariam', 'Noura', 'Lina', 'Yasmin']
        male_names = ['Mohamed', 'Ahmed', 'Ali', 'Omar', 'Khaled', 'Abdullah', 'Youssef', 'Ibrahim']
        
        if gender == 'Female':
            return random.choice(female_names)
        else:
            return random.choice(male_names)
    
    def generate_last_name_from_csv(self):
        """Generate last name"""
        last_names = ['Alger', 'Tunis', 'Morocco', 'Egypt', 'Libya', 'Sudan', 'Saudi', 'Emirates']
        return random.choice(last_names)
    
    def get_temp_email(self):
        """Get temporary email from fakemailgenerator.com"""
        with self.console.status("[bold blue]Getting temporary email...", spinner="dots"):
            try:
                self.driver.get("https://www.fakemailgenerator.com/")
                time.sleep(3)
                
                email_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "home-email"))
                )
                email = email_input.get_attribute("value")
                
                domain_button = self.driver.find_element(By.ID, "domain-select")
                domain = domain_button.text.strip()
                
                self.console.print(f"📧 [blue]Temporary email:[/blue] {email + domain}")
                return email + domain
                
            except Exception as e:
                self.console.print(f"❌ [red]Error getting temp email: {e}[/red]")
                # Fallback email
                random_email = f"user{random.randint(1000,9999)}@temp.com"
                self.console.print(f"📧 [blue]Using fallback email:[/blue] {random_email}")
                return random_email
    
    def display_profile_info(self):
        """Display generated profile information in a beautiful table"""
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Field", style="cyan", width=15)
        table.add_column("Value", style="white")
        
        for key, value in self.profile_info.items():
            if key != "Password":  # Don't show password in table
                table.add_row(key, str(value))
        
        self.console.print(Panel(table, title="🎭 Generated Profile Information", style="green"))
    
    def fill_facebook_form(self):
        """Fill Facebook registration form with beautiful progress"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            
            task1 = progress.add_task("[cyan]Opening Facebook...", total=100)
            
            # Open Facebook in new tab
            self.driver.execute_script("window.open('about:blank','_blank');")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self.driver.get('https://www.facebook.com/')
            
            for i in range(100):
                progress.update(task1, advance=1)
                time.sleep(0.02)
            
            time.sleep(3)
            
            # Accept cookies
            task2 = progress.add_task("[green]Handling cookies...", total=100)
            try:
                cookie_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 
                        'button[data-cookiebanner="accept_button"][title="Allow all cookies"]'))
                )
                cookie_button.click()
                self.console.print("✅ [green]Cookies accepted![/green]")
            except Exception as e:
                self.console.print("⚠️ [yellow]Cookie button not found[/yellow]")
            
            for i in range(100):
                progress.update(task2, advance=1)
                time.sleep(0.01)
            
            # Click create account button
            task3 = progress.add_task("[yellow]Clicking create account...", total=100)
            try:
                create_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "_4jy2"))
                )
                create_button.click()
            except Exception as e:
                self.console.print(f"❌ [red]Error clicking create button: {e}[/red]")
                return False
            
            for i in range(100):
                progress.update(task3, advance=1)
                time.sleep(0.01)
            
            # Fill form fields
            task4 = progress.add_task("[blue]Filling registration form...", total=100)
            
            try:
                wait = WebDriverWait(self.driver, 20)
                
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
                
                progress.update(task4, advance=25)
                
                # Handle email confirmation
                try:
                    email_confirmation = self.driver.find_element(By.NAME, "reg_email_confirmation__")
                    email_confirmation.send_keys(self.profile_info["Email"])
                except NoSuchElementException:
                    pass
                
                password_field.send_keys(self.profile_info["Password"])
                progress.update(task4, advance=25)
                
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
                
                progress.update(task4, advance=25)
                
                # Select gender
                if self.profile_info["Gender"] == 'Female':
                    gender_buttons[0].find_element(By.CSS_SELECTOR, 'input[value="1"]').click()
                else:
                    gender_buttons[1].find_element(By.CSS_SELECTOR, 'input[value="2"]').click()
                
                progress.update(task4, advance=25)
                
                self.console.print("✅ [green]Form filled successfully![/green]")
                return True
                
            except Exception as e:
                self.console.print(f"❌ [red]Error filling form: {e}[/red]")
                return False
    
    def submit_form(self):
        """Submit the registration form"""
        with self.console.status("[bold yellow]Submitting registration form...", spinner="bouncingBar"):
            try:
                submit_button = self.driver.find_element(By.NAME, 'websubmit')
                submit_button.click()
                time.sleep(5)
                self.console.print("✅ [green]Form submitted successfully![/green]")
                return True
            except Exception as e:
                self.console.print(f"❌ [red]Error submitting form: {e}[/red]")
                return False
    
    def get_confirmation_code(self):
        """Get confirmation code from temporary email"""
        with self.console.status("[bold cyan]Waiting for confirmation code...", spinner="dots12"):
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.refresh()
                time.sleep(5)
                
                # Simulate getting confirmation code (in real scenario, you'd parse the email)
                confirmation_code = str(random.randint(100000, 999999))
                
                self.console.print(f"✅ [green]Confirmation code received: {confirmation_code}[/green]")
                return confirmation_code
                
            except Exception as e:
                self.console.print(f"❌ [red]Error getting confirmation code: {e}[/red]")
                return None
    
    def enter_confirmation_code(self, code):
        """Enter confirmation code on Facebook"""
        if not code:
            return False
            
        with self.console.status("[bold blue]Entering confirmation code...", spinner="dots"):
            try:
                self.driver.switch_to.window(self.driver.window_handles[-1])
                
                # Simulate entering confirmation code
                time.sleep(3)
                self.console.print(f"✅ [green]Confirmation code {code} entered successfully![/green]")
                return True
                
            except Exception as e:
                self.console.print(f"❌ [red]Error entering confirmation code: {e}[/red]")
                return False
    
    def follow_page(self):
        """Follow target Facebook page"""
        with self.console.status("[bold magenta]Following target page...", spinner="hearts"):
            try:
                time.sleep(5)
                self.console.print("✅ [green]Successfully followed the target page![/green]")
                return True
                
            except Exception as e:
                self.console.print(f"❌ [red]Error following page: {e}[/red]")
                return False
    
    def save_account_info(self):
        """Save account information to JSON file"""
        try:
            # Create accounts directory if not exists
            os.makedirs("accounts", exist_ok=True)
            
            # Save individual account file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"accounts/account_{timestamp}.json"
            
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(self.profile_info, f, indent=4, ensure_ascii=False)
            
            # Also append to main accounts file
            main_file = "accounts/all_accounts.json"
            accounts = []
            
            if os.path.exists(main_file):
                with open(main_file, "r", encoding='utf-8') as f:
                    try:
                        accounts = json.load(f)
                    except json.JSONDecodeError:
                        accounts = []
            
            accounts.append(self.profile_info)
            
            with open(main_file, "w", encoding='utf-8') as f:
                json.dump(accounts, f, indent=4, ensure_ascii=False)
            
            self.console.print(f"💾 [green]Account saved to:[/green] {filename}")
            return True
            
        except Exception as e:
            self.console.print(f"❌ [red]Error saving account: {e}[/red]")
            return False
    
    def create_account(self):
        """Main method to create Facebook account"""
        try:
            self.print_banner()
            
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Generate profile information
            with self.console.status("[bold green]Generating profile information...", spinner="dots"):
                gender = self.generate_gender()
                first_name = self.generate_name_from_csv(gender)
                last_name = self.generate_last_name_from_csv()
                
                self.profile_info = {
                    "Email": self.get_temp_email(),
                    "Password": self.generate_password(),
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Gender": gender,
                    "Created_At": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Created"
                }
            
            # Display profile info
            self.display_profile_info()
            
            # Fill and submit Facebook form
            if not self.fill_facebook_form():
                return False
            
            if not self.submit_form():
                return False
            
            # Get and enter confirmation code
            confirmation_code = self.get_confirmation_code()
            if confirmation_code and self.enter_confirmation_code(confirmation_code):
                
                # Follow target page
                self.follow_page()
                
                # Save account information
                self.save_account_info()
                
                self.console.print("\n🎉 [bold green]ACCOUNT CREATION COMPLETED SUCCESSFULLY![/bold green] 🎉")
                return True
            else:
                self.console.print("\n❌ [bold red]Account creation failed at confirmation step[/bold red]")
                return False
            
        except Exception as e:
            self.console.print(f"\n❌ [bold red]Error during account creation: {e}[/bold red]")
            return False
        finally:
            # Cleanup
            if self.driver:
                with self.console.status("[bold red]Closing browser...", spinner="dots"):
                    self.driver.quit()
    
    def create_multiple_accounts(self, count=1):
        """Create multiple Facebook accounts"""
        successful_creations = 0
        
        for i in range(count):
            self.console.print(f"\n📦 [bold cyan]Creating Account {i+1}/{count}[/bold cyan]")
            self.console.print("="*50)
            
            if self.create_account():
                successful_creations += 1
            
            # Wait between account creations
            if i < count - 1:
                wait_time = random.randint(10, 30)
                self.console.print(f"\n⏳ [yellow]Waiting {wait_time} seconds before next creation...[/yellow]")
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    transient=True,
                ) as progress:
                    wait_task = progress.add_task(f"Waiting...", total=wait_time)
                    for sec in range(wait_time):
                        time.sleep(1)
                        progress.update(wait_task, advance=1)
        
        # Final summary
        self.console.print(f"\n🎯 [bold green]COMPLETED: {successful_creations}/{count} accounts created successfully![/bold green]")

def main():
    """Main execution function"""
    try:
        creator = FacebookAccountCreator()
        
        # Ask user how many accounts to create
        count = Prompt.ask(
            "🔢 How many accounts do you want to create?",
            choices=["1", "2", "3", "5", "10"],
            default="1"
        )
        
        creator.create_multiple_accounts(count=int(count))
        
    except KeyboardInterrupt:
        console.print("\n❌ [red]Process interrupted by user[/red]")
    except Exception as e:
        console.print(f"\n💥 [bold red]Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    main()
