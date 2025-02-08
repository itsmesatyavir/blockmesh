import os
import subprocess
import sys

#itsmesatyavir 
BRIGHT_CYAN = "\033[1;36m"
RESET_COLOR = "\033[0m"

def print_banner():
    print(f"{BRIGHT_CYAN}𝐅 𝐎 𝐑 𝐄 𝐒 𝐓 𝐀 𝐑 𝐌 𝐘")
    print("https://t.me/forestarmy")
    print(f"{RESET_COLOR}\n")

def print_menu():
    print("1. Account Setup")
    print("2. Install Requirements")
    print("3. Enter Proxy")
    print("4. Run Script [Without Proxy]")
    print("5. Run Script [With Proxy]")
    print("6. Exit")

def account_setup():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    with open("data.txt", "a") as file:
        file.write(f"{email}|{password}\n")
    print("Account credentials saved to data.txt.")

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")

def enter_proxy():
    proxy = input("Enter your proxy (format: ip:port): ")
    with open("proxies.txt", "w") as file:
        file.write(proxy + "\n")
    print("Proxy saved to proxies.txt.")

def run_script_without_proxy():
    print("WARNING: Running the script without a proxy may expose your IP address.")
    confirmation = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirmation == "yes":
        try:
            subprocess.check_call([sys.executable, "main.py"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to run the script: {e}")
    else:
        print("Operation canceled.")

def run_script_with_proxy():
    print("WARNING: Running the script with a proxy may affect performance.")
    confirmation = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirmation == "yes":
        try:
            subprocess.check_call([sys.executable, "mainp.py"])
        except subprocess.CalledProcessError as e:
            print(f"Failed to run the script: {e}")
    else:
        print("Operation canceled.")

def main():
    while True:
        print_banner()  # Display the banner in bright cyan
        print_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            account_setup()
        elif choice == "2":
            install_requirements()
        elif choice == "3":
            enter_proxy()
        elif choice == "4":
            run_script_without_proxy()
        elif choice == "5":
            run_script_with_proxy()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option (1-6).")

if __name__ == "__main__":
    main()
