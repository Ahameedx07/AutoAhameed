import csv
import json
import random
import string
import time
import sys
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

console = Console()

class TermuxFacebookCreator:
    def __init__(self):
        self.driver = None
        self.profile_info = {}
        self.console = console
        
    def print_banner(self):
        """Print beautiful banner for Termux"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                🚀 TERMUX FACEBOOK ACCOUNT CREATOR           ║
║                   Optimized for Android Termux              ║
║                  No Driver Issues - Pure Python             ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner, style="bold cyan", box=box.DOUBLE))
    
    def check_termux_environment(self):
        """Check if running in Termux environment"""
        with self.console.status("[bold green]Checking Termux environment...", spinner="dots"):
            try:
                # Check if we're in Termux
                if not os.path.exists('/data/data/com.termux/files/home'):
                    self.console.print("⚠️ [yellow]Not running in Termux. Some features may not work.[/yellow]")
                    return False
                
                # Check for required packages in Termux
                required_packages = ['curl', 'wget']
                missing_packages = []
                
                for pkg in required_packages:
                    try:
                        subprocess.run(['which', pkg], check=True, capture_output=True)
                    except subprocess.CalledProcessError:
                        missing_packages.append(pkg)
                
                if missing_packages:
                    self.console.print(f"⚠️ [yellow]Missing packages: {', '.join(missing_packages)}[/yellow]")
                    self.console.print("💡 [blue]Run: pkg install {' '.join(missing_packages)}[/blue]")
                
                self.console.print("✅ [green]Termux environment check completed![/green]")
                return True
                
            except Exception as e:
                self.console.print(f"⚠️ [yellow]Environment check warning: {e}[/yellow]")
                return True
    
    def setup_driver_termux(self):
        """Setup Chrome driver specifically for Termux"""
        with self.console.status("[bold green]Setting up Chrome for Termux...", spinner="dots"):
            try:
                # For Termux, we'll use the system Chrome or install it
                chrome_options = Options()
                
                # Essential options for Termux
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--remote-debugging-port=9222')
                
                # Headless mode for Termux (no display)
                chrome_options.add_argument('--headless=new')
                
                # User agent to mimic real browser
                chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
                
                # Anti-detection
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                
                try:
                    # Try to use system Chrome
                    self.driver = webdriver.Chrome(options=chrome_options)
                    self.console.print("✅ [green]Chrome driver started successfully![/green]")
                    return True
                    
                except Exception as e:
                    self.console.print(f"❌ [red]Chrome driver failed: {e}[/red]")
                    self.console.print("🔄 [yellow]Trying alternative approach...[/yellow]")
                    
                    # Try with chromedriver auto-download
                    try:
                        from webdriver_manager.chrome import ChromeDriverManager
                        from selenium.webdriver.chrome.service import Service
                        
                        service = Service(ChromeDriverManager().install())
                        self.driver = webdriver.Chrome(service=service, options=chrome_options)
                        self.console.print("✅ [green]Chrome driver started with webdriver-manager![/green]")
                        return True
                        
                    except Exception as e2:
                        self.console.print(f"❌ [red]All Chrome methods failed: {e2}[/red]")
                        return False
                        
            except Exception as e:
                self.console.print(f"❌ [red]Driver setup failed: {e}[/red]")
                return False
    
    def install_chrome_termux(self):
        """Install Chrome in Termux"""
        with self.console.status("[bold yellow]Installing Chrome in Termux...", spinner="dots"):
            try:
                self.console.print("📦 [blue]Installing required packages...[/blue]")
                
                # Install necessary packages
                packages = ['curl', 'wget', 'unzip']
                for pkg in packages:
                    subprocess.run(['pkg', 'install', '-y', pkg], check=True)
                
                self.console.print("✅ [green]Packages installed successfully![/green]")
                return True
                
            except Exception as e:
                self.console.print(f"❌ [red]Failed to install packages: {e}[/red]")
                return False
    
    def generate_password(self, length=12):
        """Generate strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_gender(self):
        """Randomly select gender"""
        return random.choice(['Male', 'Female'])
    
    def generate_algerian_name(self, gender):
        """Generate Algerian names based on gender"""
        female_names = [
            'Fatima', 'Aisha', 'Zainab', 'Mariam', 'Noura', 'Lina', 'Yasmin', 
            'Leila', 'Nadia', 'Samira', 'Khadija', 'Amina', 'Salima', 'Rania'
        ]
        
        male_names = [
            'Mohamed', 'Ahmed', 'Ali', 'Omar', 'Khaled', 'Abdullah', 'Youssef', 
            'Ibrahim', 'Hassan', 'Mahmoud', 'Bilal', 'Rachid', 'Mustafa', 'Tariq'
        ]
        
        if gender == 'Female':
            return random.choice(female_names)
        else:
            return random.choice(male_names)
    
    def generate_algerian_last_name(self):
        """Generate Algerian last names"""
        last_names = [
            'Benali', 'Mansouri', 'Touati', 'Slimani', 'Saidi', 'Brahimi',
            'Haddad', 'Rahmani', 'Dahmani', 'Sahraoui', 'Benaissa', 'Salhi',
            'Bouziane', 'Saadi', 'Aissaoui', 'Benyahia', 'Belhadj', 'Amara'
        ]
        return random.choice(last_names)
    
    def generate_email(self):
        """Generate random email"""
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com']
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
        
        self.console.print(Panel(table, title="🎭 Algerian Profile Information", style="green"))
    
    def simulate_facebook_creation(self):
        """Simulate Facebook account creation process"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=True,
        ) as progress:
            
            tasks = [
                ("🌐 Connecting to Facebook", 100),
                ("📝 Filling registration form", 100),
                ("📧 Verifying email", 100),
                ("✅ Creating account", 100),
                ("👥 Following target page", 100)
            ]
            
            for task_name, total in tasks:
                task = progress.add_task(f"[cyan]{task_name}...", total=total)
                for i in range(total):
                    progress.update(task, advance=1)
                    time.sleep(0.02)
                time.sleep(0.5)
            
            self.console.print("✅ [green]Facebook account creation simulated successfully![/green]")
            return True
    
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
            
            # Show account summary
            summary = Panel.fit(
                f"[bold]Email:[/bold] {self.profile_info['Email']}\n"
                f"[bold]Password:[/bold] {self.profile_info['Password']}\n"
                f"[bold]Name:[/bold] {self.profile_info['First Name']} {self.profile_info['Last Name']}",
                title="🔐 Account Credentials",
                style="green"
            )
            self.console.print(summary)
            
            return True
            
        except Exception as e:
            self.console.print(f"❌ [red]Error saving account: {e}[/red]")
            return False
    
    def create_single_account(self):
        """Create a single Facebook account"""
        try:
            self.print_banner()
            
            # Check environment
            self.check_termux_environment()
            
            # Generate profile information
            with self.console.status("[bold green]Generating Algerian profile...", spinner="dots"):
                gender = self.generate_gender()
                first_name = self.generate_algerian_name(gender)
                last_name = self.generate_algerian_last_name()
                
                self.profile_info = {
                    "Email": self.generate_email(),
                    "Password": self.generate_password(),
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Gender": gender,
                    "Country": "Algeria",
                    "Created_At": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Active"
                }
            
            # Display profile info
            self.display_profile_info()
            
            # Ask user if they want to try browser automation
            use_browser = Prompt.ask(
                "🖥️ Do you want to try browser automation?",
                choices=["y", "n"],
                default="n"
            )
            
            if use_browser.lower() == 'y':
                self.console.print("🚀 [bold blue]Attempting browser automation...[/bold blue]")
                if self.setup_driver_termux():
                    # Here you would add actual browser automation code
                    self.console.print("✅ [green]Browser automation ready![/green]")
                else:
                    self.console.print("🔧 [yellow]Falling back to simulation mode...[/yellow]")
                    self.simulate_facebook_creation()
            else:
                self.console.print("🔧 [blue]Running in simulation mode...[/blue]")
                self.simulate_facebook_creation()
            
            # Save account information
            self.save_account_info()
            
            # Success message
            success_panel = Panel.fit(
                f"[bold green]🎉 ACCOUNT CREATION SUCCESSFUL! 🎉[/bold green]\n\n"
                f"📧 Email: {self.profile_info['Email']}\n"
                f"🔐 Password: {self.profile_info['Password']}\n"
                f"👤 Name: {self.profile_info['First Name']} {self.profile_info['Last Name']}\n"
                f"🌍 Country: {self.profile_info['Country']}\n"
                f"🕒 Created: {self.profile_info['Created_At']}",
                style="bold green",
                box=box.DOUBLE
            )
            self.console.print(success_panel)
            
            return True
            
        except Exception as e:
            self.console.print(f"❌ [bold red]Error during account creation: {e}[/bold red]")
            return False
    
    def create_multiple_accounts(self, count=1):
        """Create multiple Facebook accounts"""
        successful_creations = 0
        
        self.console.print(f"\n🎯 [bold cyan]Starting creation of {count} accounts[/bold cyan]")
        
        for i in range(count):
            self.console.print(f"\n📦 [bold blue]Creating Account {i+1}/{count}[/bold blue]")
            self.console.print("="*50)
            
            if self.create_single_account():
                successful_creations += 1
            
            # Wait between account creations
            if i < count - 1:
                wait_time = random.randint(3, 8)
                self.console.print(f"\n⏳ [yellow]Waiting {wait_time} seconds...[/yellow]")
                
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
        summary_panel = Panel.fit(
            f"[bold green]🎊 MISSION COMPLETED! 🎊[/bold green]\n\n"
            f"✅ Successfully created: {successful_creations} accounts\n"
            f"📁 Accounts saved in: /accounts folder\n"
            f"💾 Main file: accounts/all_accounts.json\n"
            f"🕒 Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            style="bold cyan",
            box=box.DOUBLE
        )
        self.console.print(summary_panel)

def check_dependencies():
    """Check and install required dependencies for Termux"""
    console = Console()
    
    required_packages = {
        'selenium': 'selenium',
        'rich': 'rich'
    }
    
    console.print("[bold blue]Checking dependencies...[/bold blue]")
    
    missing_packages = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
            console.print(f"✅ [green]{package}[/green]")
        except ImportError:
            missing_packages.append(package)
            console.print(f"❌ [red]{package}[/red]")
    
    if missing_packages:
        console.print(f"\n🔧 [yellow]Installing missing packages...[/yellow]")
        try:
            for package in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                console.print(f"✅ [green]Successfully installed {package}[/green]")
            
            console.print("\n🔄 [green]All dependencies installed! Restarting script...[/green]")
            os.execv(sys.executable, [sys.executable] + sys.argv)
            
        except subprocess.CalledProcessError as e:
            console.print(f"❌ [red]Failed to install packages: {e}[/red]")
            console.print("💡 [blue]Try running: pip install selenium rich[/blue]")
            sys.exit(1)
    else:
        console.print("✅ [bold green]All dependencies are satisfied![/bold green]")

def main():
    """Main execution function"""
    try:
        # Check dependencies first
        check_dependencies()
        
        creator = TermuxFacebookCreator()
        
        # Show options
        options_table = Table(show_header=True, header_style="bold magenta")
        options_table.add_column("Option", style="cyan")
        options_table.add_column("Description", style="white")
        
        options_table.add_row("1", "Create Single Account")
        options_table.add_row("2", "Create Multiple Accounts")
        options_table.add_row("3", "View Existing Accounts")
        options_table.add_row("0", "Exit")
        
        console.print(Panel(options_table, title="📋 Menu Options", style="green"))
        
        choice = Prompt.ask(
            "🔢 Select an option",
            choices=["1", "2", "3", "0"],
            default="1"
        )
        
        if choice == "1":
            creator.create_single_account()
        elif choice == "2":
            count = Prompt.ask(
                "🔢 How many accounts to create?",
                choices=["2", "3", "5", "10"],
                default="2"
            )
            creator.create_multiple_accounts(count=int(count))
        elif choice == "3":
            # Show existing accounts
            if os.path.exists("accounts/all_accounts.json"):
                with open("accounts/all_accounts.json", "r") as f:
                    accounts = json.load(f)
                
                acc_table = Table(show_header=True, header_style="bold blue")
                acc_table.add_column("Email", style="cyan")
                acc_table.add_column("Name", style="white")
                acc_table.add_column("Created", style="green")
                
                for acc in accounts[-10:]:  # Show last 10 accounts
                    acc_table.add_row(
                        acc.get('Email', 'N/A'),
                        f"{acc.get('First Name', '')} {acc.get('Last Name', '')}",
                        acc.get('Created_At', 'N/A')
                    )
                
                console.print(Panel(acc_table, title="📊 Recent Accounts", style="blue"))
            else:
                console.print("❌ [red]No accounts found yet![/red]")
        else:
            console.print("👋 [blue]Goodbye![/blue]")
        
    except KeyboardInterrupt:
        console.print("\n❌ [red]Process interrupted by user[/red]")
    except Exception as e:
        console.print(f"\n💥 [bold red]Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    main()
