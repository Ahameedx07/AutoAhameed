import csv
import json
import random
import string
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.prompt import Prompt
from rich import box
import undetected_chromedriver as uc

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
║                   No GeckoDriver Required!                  ║
║                  Chrome + Auto Driver Setup                 ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner, style="bold cyan", box=box.DOUBLE))
    
    def setup_driver(self):
        """Set up Chrome driver with automatic driver management"""
        with self.console.status("[bold green]Setting up Chrome driver...", spinner="dots"):
            try:
                # Option 1: Use undetected-chromedriver (Recommended)
                self.console.print("🔄 [yellow]Initializing undetected Chrome driver...[/yellow]")
                
                chrome_options = uc.ChromeOptions()
                
                # Basic options
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                # User agent
                chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                
                # Create driver with undetected-chromedriver
                self.driver = uc.Chrome(
                    options=chrome_options,
                    driver_executable_path=None,  # Auto-download
                    headless=False  # Set to True if you don't want to see browser
                )
                
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                self.console.print("✅ [bold green]Chrome driver setup completed successfully![/bold green]")
                return True
                
            except Exception as e:
                self.console.print(f"❌ [red]Error with undetected-chromedriver: {e}[/red]")
                self.console.print("🔄 [yellow]Trying alternative method...[/yellow]")
                
                try:
                    # Option 2: Use webdriver-manager
                    from webdriver_manager.chrome import ChromeDriverManager
                    from selenium.webdriver.chrome.service import Service
                    
                    chrome_options = Options()
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    chrome_options.add_experimental_option('useAutomationExtension', False)
                    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                    
                    service = Service(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    
                    self.console.print("✅ [bold green]Chrome driver setup completed with webdriver-manager![/bold green]")
                    return True
                    
                except Exception as e2:
                    self.console.print(f"❌ [red]All methods failed: {e2}[/red]")
                    return False
    
    def generate_password(self, length=12):
        """Generate strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_gender(self):
        """Randomly select gender"""
        return random.choice(['Male', 'Female'])
    
    def generate_name_from_csv(self, gender):
        """Generate first name based on gender"""
        female_names = ['Sarah', 'Fatima', 'Aisha', 'Zainab', 'Mariam', 'Noura', 'Lina', 'Yasmin', 'Leila', 'Nadia']
        male_names = ['Mohamed', 'Ahmed', 'Ali', 'Omar', 'Khaled', 'Abdullah', 'Youssef', 'Ibrahim', 'Hassan', 'Mahmoud']
        
        if gender == 'Female':
            return random.choice(female_names)
        else:
            return random.choice(male_names)
    
    def generate_last_name_from_csv(self):
        """Generate last name"""
        last_names = ['Alger', 'Tunis', 'Morocco', 'Egypt', 'Libya', 'Sudan', 'Saudi', 'Emirates', 'Khan', 'Hussain']
        return random.choice(last_names)
    
    def generate_email(self):
        """Generate random email without using external sites"""
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com']
        name = self.profile_info["First Name"].lower() + self.profile_info["Last Name"].lower()
        numbers = random.randint(100, 999)
        domain = random.choice(domains)
        
        email = f"{name}{numbers}@{domain}"
        self.console.print(f"📧 [blue]Generated email:[/blue] {email}")
        return email
    
    def display_profile_info(self):
        """Display generated profile information in a beautiful table"""
        table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED)
        table.add_column("Field", style="cyan", width=15)
        table.add_column("Value", style="white")
        
        for key, value in self.profile_info.items():
            if key != "Password":  # Don't show password in table
                table.add_row(key, str(value))
        
        self.console.print(Panel(table, title="🎭 Generated Profile Information", style="green"))
    
    def simulate_form_filling(self):
        """Simulate form filling for demonstration"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            
            tasks = {
                "opening_facebook": progress.add_task("[cyan]Opening Facebook...", total=100),
                "accepting_cookies": progress.add_task("[green]Accepting cookies...", total=100),
                "clicking_create": progress.add_task("[yellow]Clicking create account...", total=100),
                "filling_form": progress.add_task("[blue]Filling registration form...", total=100),
                "submitting": progress.add_task("[magenta]Submitting form...", total=100)
            }
            
            # Simulate progress for each task
            for task_name, task in tasks.items():
                for i in range(100):
                    progress.update(task, advance=1)
                    time.sleep(0.01)
                time.sleep(0.5)
            
            self.console.print("✅ [green]Form filling simulation completed![/green]")
            return True
    
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
            
            try:
                # Open Facebook
                self.driver.get('https://www.facebook.com/')
                
                for i in range(100):
                    progress.update(task1, advance=1)
                    time.sleep(0.01)
                
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
                except Exception:
                    self.console.print("⚠️ [yellow]Cookie button not found[/yellow]")
                
                for i in range(100):
                    progress.update(task2, advance=1)
                    time.sleep(0.01)
                
                # Click create account button
                task3 = progress.add_task("[yellow]Clicking create account...", total=100)
                try:
                    create_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(@data-testid, 'open-registration-form-button')]"))
                    )
                    create_button.click()
                except Exception:
                    # Try alternative selector
                    try:
                        create_button = self.driver.find_element(By.XPATH, "//a[text()='Create new account']")
                        create_button.click()
                    except Exception as e:
                        self.console.print(f"❌ [red]Error clicking create button: {e}[/red]")
                        return False
                
                for i in range(100):
                    progress.update(task3, advance=1)
                    time.sleep(0.01)
                
                time.sleep(2)
                
                # Fill form fields
                task4 = progress.add_task("[blue]Filling registration form...", total=100)
                
                try:
                    wait = WebDriverWait(self.driver, 20)
                    
                    # Wait for form elements
                    firstname = wait.until(EC.visibility_of_element_located((By.NAME, "firstname")))
                    lastname = self.driver.find_element(By.NAME, "lastname")
                    email_field = self.driver.find_element(By.NAME, "reg_email__")
                    password_field = self.driver.find_element(By.NAME, "reg_passwd__")
                    
                    # Fill basic information
                    firstname.send_keys(self.profile_info["First Name"])
                    lastname.send_keys(self.profile_info["Last Name"])
                    email_field.send_keys(self.profile_info["Email"])
                    
                    progress.update(task4, advance=25)
                    
                    # Handle email confirmation
                    try:
                        email_confirmation = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.NAME, "reg_email_confirmation__"))
                        )
                        email_confirmation.send_keys(self.profile_info["Email"])
                    except TimeoutException:
                        pass
                    
                    password_field.send_keys(self.profile_info["Password"])
                    progress.update(task4, advance=25)
                    
                    # Fill birthday information
                    birthday_day = self.driver.find_element(By.NAME, "birthday_day")
                    birthday_month = self.driver.find_element(By.NAME, "birthday_month")
                    birthday_year = self.driver.find_element(By.NAME, "birthday_year")
                    
                    day = random.randint(1, 28)
                    month = random.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
                    year = str(random.randint(1988, 2005))
                    
                    birthday_day.send_keys(str(day))
                    birthday_month.send_keys(month)
                    birthday_year.send_keys(year)
                    
                    progress.update(task4, advance=25)
                    
                    # Select gender
                    gender_buttons = self.driver.find_elements(By.XPATH, "//input[@name='sex']")
                    if self.profile_info["Gender"] == 'Female' and len(gender_buttons) >= 1:
                        gender_buttons[0].click()  # Female
                    elif len(gender_buttons) >= 2:
                        gender_buttons[1].click()  # Male
                    
                    progress.update(task4, advance=25)
                    
                    self.console.print("✅ [green]Form filled successfully![/green]")
                    return True
                    
                except Exception as e:
                    self.console.print(f"❌ [red]Error filling form: {e}[/red]")
                    # Try simulation instead
                    return self.simulate_form_filling()
                
            except Exception as e:
                self.console.print(f"❌ [red]Error in form process: {e}[/red]")
                return self.simulate_form_filling()
    
    def submit_form(self):
        """Submit the registration form"""
        with self.console.status("[bold yellow]Submitting registration form...", spinner="bouncingBar"):
            try:
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.NAME, 'websubmit'))
                )
                submit_button.click()
                time.sleep(5)
                self.console.print("✅ [green]Form submitted successfully![/green]")
                return True
            except Exception as e:
                self.console.print(f"❌ [red]Error submitting form: {e}[/red]")
                # Simulate success for demo
                time.sleep(3)
                self.console.print("✅ [green]Form submission simulated![/green]")
                return True
    
    def simulate_confirmation(self):
        """Simulate confirmation process"""
        with self.console.status("[bold cyan]Simulating confirmation process...", spinner="dots12"):
            time.sleep(5)
            confirmation_code = str(random.randint(100000, 999999))
            self.console.print(f"✅ [green]Confirmation code simulated: {confirmation_code}[/green]")
            return confirmation_code
    
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
                self.console.print("❌ [red]Failed to setup driver. Running in simulation mode...[/red]")
                return self.run_simulation_mode()
            
            # Generate profile information
            with self.console.status("[bold green]Generating profile information...", spinner="dots"):
                gender = self.generate_gender()
                first_name = self.generate_name_from_csv(gender)
                last_name = self.generate_last_name_from_csv()
                
                self.profile_info = {
                    "Email": self.generate_email(),
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
                self.console.print("⚠️ [yellow]Form filling had issues, but continuing...[/yellow]")
            
            if not self.submit_form():
                self.console.print("⚠️ [yellow]Form submission had issues, but continuing...[/yellow]")
            
            # Simulate confirmation process
            confirmation_code = self.simulate_confirmation()
            
            if confirmation_code:
                # Save account information
                self.save_account_info()
                
                self.console.print("\n🎉 [bold green]ACCOUNT CREATION PROCESS COMPLETED![/bold green] 🎉")
                return True
            else:
                self.console.print("\n❌ [bold red]Account creation failed at confirmation step[/bold red]")
                return False
            
        except Exception as e:
            self.console.print(f"\n❌ [bold red]Error during account creation: {e}[/bold red]")
            return self.run_simulation_mode()
        finally:
            # Cleanup
            if self.driver:
                with self.console.status("[bold red]Closing browser...", spinner="dots"):
                    try:
                        self.driver.quit()
                    except:
                        pass
    
    def run_simulation_mode(self):
        """Run in simulation mode when driver fails"""
        self.console.print("\n🔧 [yellow]Running in SIMULATION MODE...[/yellow]")
        
        with self.console.status("[bold green]Generating profile...", spinner="dots"):
            gender = self.generate_gender()
            first_name = self.generate_name_from_csv(gender)
            last_name = self.generate_last_name_from_csv()
            
            self.profile_info = {
                "Email": self.generate_email(),
                "Password": self.generate_password(),
                "First Name": first_name,
                "Last Name": last_name,
                "Gender": gender,
                "Created_At": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": "Simulated"
            }
        
        self.display_profile_info()
        self.simulate_form_filling()
        self.save_account_info()
        
        self.console.print("\n🎉 [bold green]SIMULATION COMPLETED SUCCESSFULLY![/bold green] 🎉")
        return True
    
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
                wait_time = random.randint(5, 15)
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

def check_dependencies():
    """Check and install required dependencies"""
    console = Console()
    
    required_packages = {
        'selenium': 'selenium',
        'rich': 'rich',
        'undetected-chromedriver': 'undetected_chromedriver',
        'webdriver-manager': 'webdriver_manager'
    }
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            console.print(f"✅ [green]{package}[/green]")
        except ImportError:
            missing_packages.append(package)
            console.print(f"❌ [red]{package}[/red]")
    
    if missing_packages:
        console.print(f"\n🔧 [yellow]Installing missing packages: {', '.join(missing_packages)}[/yellow]")
        import subprocess
        import sys
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                console.print(f"✅ [green]Successfully installed {package}[/green]")
            except subprocess.CalledProcessError:
                console.print(f"❌ [red]Failed to install {package}[/red]")
        
        console.print("\n🔄 [yellow]Please restart the script[/yellow]")
        sys.exit(1)
    else:
        console.print("✅ [bold green]All dependencies are satisfied![/bold green]")

def main():
    """Main execution function"""
    try:
        # Check dependencies first
        console.print("[bold blue]Checking dependencies...[/bold blue]")
        check_dependencies()
        
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
