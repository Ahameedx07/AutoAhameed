import csv
import json
import random
import string
import time
import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.text import Text

console = Console()

class TermuxFacebookSimulator:
    def __init__(self):
        self.profile_info = {}
        self.console = console
        self.accounts_created = 0
        
    def print_banner(self):
        """Print beautiful banner for Termux"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                🚀 TERMUX FACEBOOK SIMULATOR                 ║
║                   No Browser - Pure Python                  ║
║                 Algerian Account Generator                  ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner, style="bold cyan", box=box.DOUBLE))
    
    def animate_loading(self, text, duration=3):
        """Show animated loading"""
        with self.console.status(f"[bold green]{text}", spinner="dots") as status:
            time.sleep(duration)
    
    def generate_password(self, length=12):
        """Generate strong random password"""
        chars = string.ascii_letters + string.digits + "!@#$%"
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_gender(self):
        """Randomly select gender"""
        return random.choice(['Male', 'Female'])
    
    def generate_algerian_name(self, gender):
        """Generate authentic Algerian names based on gender"""
        female_names = [
            'Fatima', 'Aisha', 'Zainab', 'Mariam', 'Noura', 'Lina', 'Yasmin', 
            'Leila', 'Nadia', 'Samira', 'Khadija', 'Amina', 'Salima', 'Rania',
            'Soraya', 'Djamila', 'Yamina', 'Habiba', 'Fella', 'Widad'
        ]
        
        male_names = [
            'Mohamed', 'Ahmed', 'Ali', 'Omar', 'Khaled', 'Abdullah', 'Youssef', 
            'Ibrahim', 'Hassan', 'Mahmoud', 'Bilal', 'Rachid', 'Mustafa', 'Tariq',
            'Karim', 'Nasser', 'Farid', 'Samir', 'Adel', 'Mounir'
        ]
        
        if gender == 'Female':
            return random.choice(female_names)
        else:
            return random.choice(male_names)
    
    def generate_algerian_last_name(self):
        """Generate authentic Algerian last names"""
        last_names = [
            'Benali', 'Mansouri', 'Touati', 'Slimani', 'Saidi', 'Brahimi',
            'Haddad', 'Rahmani', 'Dahmani', 'Sahraoui', 'Benaissa', 'Salhi',
            'Bouziane', 'Saadi', 'Aissaoui', 'Benyahia', 'Belhadj', 'Amara',
            'Abbas', 'Merabet', 'Mokhtari', 'Taleb', 'Bouzid', 'Khaldi',
            'Hamdi', 'Talbi', 'Cherifi', 'Bouras', 'Belaid', 'Chaib'
        ]
        return random.choice(last_names)
    
    def generate_algerian_email(self, first_name, last_name):
        """Generate Algerian-style email"""
        domains = [
            'gmail.com', 'yahoo.fr', 'hotmail.com', 'outlook.com',
            'live.com', 'protonmail.com'
        ]
        
        name_variations = [
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}_{last_name.lower()}",
            f"{first_name[0].lower()}{last_name.lower()}",
            f"{first_name.lower()}{last_name[0].lower()}",
        ]
        
        variation = random.choice(name_variations)
        numbers = random.randint(1970, 2005)  birth year style
        domain = random.choice(domains)
        
        email = f"{variation}{numbers}@{domain}"
        return email
    
    def generate_algerian_phone(self):
        """Generate Algerian phone number"""
        prefixes = ['05', '06', '07']
        prefix = random.choice(prefixes)
        number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"+213 {prefix} {number[:2]} {number[2:4]} {number[4:6]} {number[6:8]}"
    
    def generate_birth_date(self):
        """Generate realistic birth date"""
        year = random.randint(1985, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{day:02d}/{month:02d}/{year}"
    
    def generate_city(self):
        """Generate Algerian city"""
        cities = [
            'Algiers', 'Oran', 'Constantine', 'Annaba', 'Batna', 'Blida',
            'Setif', 'Chlef', 'Djelfa', 'Tebessa', 'Skikda', 'Tizi Ouzou',
            'Béjaïa', 'Sidi Bel Abbès', 'Biskra', 'Tiaret', 'Guelma'
        ]
        return random.choice(cities)
    
    def display_profile_card(self):
        """Display profile information in a beautiful card"""
        profile_card = Panel(
            f"[bold cyan]👤 Name:[/bold cyan] {self.profile_info['First Name']} {self.profile_info['Last Name']}\n"
            f"[bold cyan]📧 Email:[/bold cyan] {self.profile_info['Email']}\n"
            f"[bold cyan]🔐 Password:[/bold cyan] {self.profile_info['Password']}\n"
            f"[bold cyan]⚧ Gender:[/bold cyan] {self.profile_info['Gender']}\n"
            f"[bold cyan]📅 Birth Date:[/bold cyan] {self.profile_info['Birth Date']}\n"
            f"[bold cyan]📞 Phone:[/bold cyan] {self.profile_info['Phone']}\n"
            f"[bold cyan]🏙️ City:[/bold cyan] {self.profile_info['City']}\n"
            f"[bold cyan]🌍 Country:[/bold cyan] {self.profile_info['Country']}\n"
            f"[bold cyan]🆔 Profile ID:[/bold cyan] {self.profile_info['Profile ID']}",
            title="🎭 Algerian Facebook Profile",
            style="green",
            box=box.DOUBLE
        )
        self.console.print(profile_card)
    
    def simulate_facebook_creation(self):
        """Simulate Facebook account creation with beautiful animation"""
        steps = [
            ("🌐 Connecting to Facebook", 2),
            ("📝 Filling registration form", 3),
            ("📧 Verifying email address", 2),
            ("✅ Creating profile", 2),
            ("👥 Adding basic information", 2),
            ("🔒 Securing account", 1),
            ("🎉 Account ready!", 1)
        ]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            transient=False,
        ) as progress:
            
            tasks = {}
            for step_name, duration in steps:
                task_id = progress.add_task(f"[cyan]{step_name}", total=duration*10)
                tasks[task_id] = (step_name, duration)
            
            for task_id, (step_name, duration) in tasks.items():
                for i in range(duration * 10):
                    progress.update(task_id, advance=1)
                    time.sleep(0.1)
                
                if step_name == "✅ Creating profile":
                    self.console.print(f"✨ [green]{step_name} completed![/green]")
        
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
            return True
            
        except Exception as e:
            self.console.print(f"❌ [red]Error saving account: {e}[/red]")
            return False
    
    def show_creation_animation(self):
        """Show beautiful creation animation"""
        frames = [
            "⠋ Creating Facebook Account ⠋",
            "⠙ Creating Facebook Account ⠙", 
            "⠹ Creating Facebook Account ⠹",
            "⠸ Creating Facebook Account ⠸",
            "⠼ Creating Facebook Account ⠼",
            "⠴ Creating Facebook Account ⠴",
            "⠦ Creating Facebook Account ⠦",
            "⠧ Creating Facebook Account ⠧",
            "⠇ Creating Facebook Account ⠇",
            "⠏ Creating Facebook Account ⠏"
        ]
        
        for i in range(20):
            frame = frames[i % len(frames)]
            self.console.print(f"\r{frame}", style="bold blue", end="")
            time.sleep(0.1)
        
        self.console.print()
    
    def create_single_account(self):
        """Create a single Facebook account"""
        try:
            self.print_banner()
            
            # Generate profile information with animation
            self.animate_loading("Generating Algerian profile", 2)
            
            gender = self.generate_gender()
            first_name = self.generate_algerian_name(gender)
            last_name = self.generate_algerian_last_name()
            
            self.profile_info = {
                "Email": self.generate_algerian_email(first_name, last_name),
                "Password": self.generate_password(),
                "First Name": first_name,
                "Last Name": last_name,
                "Gender": gender,
                "Birth Date": self.generate_birth_date(),
                "Phone": self.generate_algerian_phone(),
                "City": self.generate_city(),
                "Country": "Algeria",
                "Profile ID": f"FB_{random.randint(100000000, 999999999)}",
                "Created_At": time.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": "Active"
            }
            
            # Display profile info
            self.display_profile_card()
            
            # Simulate creation process
            self.console.print("\n🚀 [bold blue]Starting Facebook account creation...[/bold blue]")
            self.show_creation_animation()
            self.simulate_facebook_creation()
            
            # Save account information
            self.save_account_info()
            
            # Success message
            success_panel = Panel.fit(
                f"[bold green]🎉 FACEBOOK ACCOUNT CREATED SUCCESSFULLY! 🎉[/bold green]\n\n"
                f"📧 [bold]Email:[/bold] {self.profile_info['Email']}\n"
                f"🔐 [bold]Password:[/bold] {self.profile_info['Password']}\n"
                f"👤 [bold]Name:[/bold] {self.profile_info['First Name']} {self.profile_info['Last Name']}\n"
                f"🌍 [bold]Location:[/bold] {self.profile_info['City']}, {self.profile_info['Country']}\n"
                f"🆔 [bold]Profile ID:[/bold] {self.profile_info['Profile ID']}\n"
                f"🕒 [bold]Created:[/bold] {self.profile_info['Created_At']}",
                style="bold green",
                box=box.DOUBLE
            )
            self.console.print(success_panel)
            
            self.accounts_created += 1
            return True
            
        except Exception as e:
            self.console.print(f"❌ [bold red]Error during account creation: {e}[/bold red]")
            return False
    
    def create_multiple_accounts(self, count=1):
        """Create multiple Facebook accounts"""
        successful_creations = 0
        
        self.console.print(f"\n🎯 [bold cyan]Starting creation of {count} Algerian Facebook accounts[/bold cyan]")
        
        for i in range(count):
            self.console.print(f"\n📦 [bold blue]Account {i+1}/{count}[/bold blue]")
            self.console.print("="*50)
            
            if self.create_single_account():
                successful_creations += 1
            
            # Wait between account creations
            if i < count - 1:
                wait_time = random.randint(2, 5)
                self.console.print(f"\n⏳ [yellow]Preparing next account in {wait_time} seconds...[/yellow]")
                
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
            f"🕒 Completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"🇩🇿 All accounts are Algerian profiles",
            style="bold cyan",
            box=box.DOUBLE
        )
        self.console.print(summary_panel)
        
        return successful_creations
    
    def show_statistics(self):
        """Show creation statistics"""
        if os.path.exists("accounts/all_accounts.json"):
            with open("accounts/all_accounts.json", "r") as f:
                accounts = json.load(f)
            
            stats = {
                "Total Accounts": len(accounts),
                "Male Accounts": len([a for a in accounts if a.get('Gender') == 'Male']),
                "Female Accounts": len([a for a in accounts if a.get('Gender') == 'Female']),
                "Latest Creation": accounts[-1]['Created_At'] if accounts else "None"
            }
            
            stats_table = Table(show_header=True, header_style="bold magenta")
            stats_table.add_column("Metric", style="cyan")
            stats_table.add_column("Value", style="green")
            
            for key, value in stats.items():
                stats_table.add_row(key, str(value))
            
            self.console.print(Panel(stats_table, title="📊 Creation Statistics", style="blue"))
        else:
            self.console.print("❌ [red]No accounts found yet! Create some accounts first.[/red]")

def check_dependencies():
    """Check and install required dependencies for Termux"""
    console = Console()
    
    required_packages = {
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
            console.print("💡 [blue]Try running: pip install rich[/blue]")
            sys.exit(1)
    else:
        console.print("✅ [bold green]All dependencies are satisfied![/bold green]")

def main():
    """Main execution function"""
    try:
        # Check dependencies first
        check_dependencies()
        
        creator = TermuxFacebookSimulator()
        
        while True:
            # Show menu
            options_table = Table(show_header=True, header_style="bold magenta")
            options_table.add_column("Option", style="cyan")
            options_table.add_column("Description", style="white")
            
            options_table.add_row("1", "Create Single Account")
            options_table.add_row("2", "Create Multiple Accounts")
            options_table.add_row("3", "View Statistics")
            options_table.add_row("4", "View Recent Accounts")
            options_table.add_row("0", "Exit")
            
            console.print(Panel(options_table, title="📋 Algerian Facebook Simulator", style="green"))
            
            choice = Prompt.ask(
                "🔢 Select an option",
                choices=["1", "2", "3", "4", "0"],
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
                creator.show_statistics()
            elif choice == "4":
                # Show recent accounts
                if os.path.exists("accounts/all_accounts.json"):
                    with open("accounts/all_accounts.json", "r") as f:
                        accounts = json.load(f)
                    
                    acc_table = Table(show_header=True, header_style="bold blue")
                    acc_table.add_column("No.", style="cyan")
                    acc_table.add_column("Email", style="white")
                    acc_table.add_column("Name", style="green")
                    acc_table.add_column("Gender", style="yellow")
                    
                    for i, acc in enumerate(accounts[-10:][::-1]):  # Show last 10 accounts
                        acc_table.add_row(
                            str(i+1),
                            acc.get('Email', 'N/A'),
                            f"{acc.get('First Name', '')} {acc.get('Last Name', '')}",
                            acc.get('Gender', 'N/A')
                        )
                    
                    console.print(Panel(acc_table, title="📜 Recent Accounts (Latest First)", style="blue"))
                else:
                    console.print("❌ [red]No accounts found yet![/red]")
            else:
                console.print("👋 [blue]Shukran! Goodbye![/blue]")
                break
            
            # Ask to continue
            if choice != "0":
                continue_choice = Prompt.ask(
                    "🔄 Continue to main menu?",
                    choices=["y", "n"],
                    default="y"
                )
                if continue_choice.lower() != 'y':
                    console.print("👋 [blue]Shukran! Goodbye![/blue]")
                    break
        
    except KeyboardInterrupt:
        console.print("\n❌ [red]Process interrupted by user[/red]")
    except Exception as e:
        console.print(f"\n💥 [bold red]Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    main()
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
