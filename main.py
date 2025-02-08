import requests
import time
import os
import threading
import random
from datetime import datetime
from colorama import init, Fore, Style
import socket
init(autoreset=True)


def print_banner():
    banner = f"{Fore.GREEN}{Style.BRIGHT}Tool Shared By FOREST ARMY (https://t.me/forestarmy) NO NEED TO PURCHASE ANY SCRIPT"
    print(banner)


proxy_tokens = {}


def generate_response_time():
    return round(random.uniform(200.0, 600.0), 1)


def get_local_ip():
    """Function to get the local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to an external server
        local_ip = s.getsockname()[0]  # Get the local IP address
        s.close()
        return local_ip
    except Exception as e:
        print(f"{Fore.RED}Error getting local IP: {e}")
        return None

def get_ip_info(ip_address):
    try:
        response = requests.get(f"https://ipwhois.app/json/{ip_address}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f"{Fore.RED}Failed to get IP info: {err}")
        return None


def submit_bandwidth(email, api_token, ip_info):
    if not ip_info:
        return

    query_params = {
        "email": email,
        "api_token": api_token,
        "ip": ip_info.get("ip", ""),
    }

    url = "https://app.blockmesh.xyz/api/get_token"

    try:
        response = requests.post(
            url, params=query_params, headers=submit_headers)
        response.raise_for_status()
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{ Fore.GREEN} Uptime reported ")
    except requests.RequestException as err:
        if err.response:
            status_code = err.response.status_code
            response_text = err.response.text
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.YELLOW} Failed to report uptime for {email}: {status_code} - {response_text}")
        else:
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.RED} Failed to report uptime for {email}: {err}")


def get_and_submit_task(email, api_token, ip_info):
    if not ip_info:
        return

    try:
        response = requests.post(
            "https://app.blockmesh.xyz/api/get_task",
            json={"email": email, "api_token": api_token},
            headers=submit_headers
        )
        response.raise_for_status()
        task_data = response.json()

        if not task_data or "id" not in task_data:
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.YELLOW} No Task Available")
            return

        task_id = task_data["id"]
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.GREEN} Task successfully retrieved!: {task_id}")
        time.sleep(random.randint(60, 120))

        submit_url = "https://app.blockmesh.xyz/api/submit_task"
        params = {
            "email": email,
            "api_token": api_token,
            "task_id": task_id,
            "response_code": 200,
            "country": ip_info.get("country_code", "VN"),
            "ip": ip_info.get("ip", ""),
            "asn": ip_info.get("asn", "AS0").replace("AS", ""),
            "colo": "SIN",
            "response_time": generate_response_time()
        }

        response = requests.post(
            submit_url, params=params, data="0" * 10, headers=submit_headers)
        response.raise_for_status()
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.GREEN} Task submitted: {task_id}")
    except requests.RequestException as err:
        print(f'{err} {err.response}')
        if err.response:
            status_code = err.response.status_code
            response_text = err.response.text
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.YELLOW} Failed to process task: {task_id} | {status_code} - {response_text}")
        else:
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.RED} Failed to process task: {err}")


print_banner()


def read_credentials(file_path):
    credentials = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                email, password = line.strip().split('|')
                credentials.append((email, password))
    except Exception as e:
        print(f"{Fore.RED}Error reading {file_path}: {e}")
    return credentials


login_endpoint = "https://api.blockmesh.xyz/api/get_token"

login_headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://app.blockmesh.xyz",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}

submit_headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "chrome-extension://obfhoiefijlolgdmphcekifedagnkfjp",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
}


def authenticate(email, password):
    login_data = {"email": email, "password": password}

    try:
        response = requests.post(
            login_endpoint, json=login_data, headers=login_headers)
        response.raise_for_status()
        auth_data = response.json()
        api_token = auth_data.get("api_token")
        proxy_tokens[email] = api_token  # Store the token by email
        print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.GREEN} Login successful for {email}")
        return api_token
    except requests.RequestException as err:
        if err.response:
            status_code = err.response.status_code
            response_text = err.response.text
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.RED} Login failed for {email}: {status_code} - {response_text}")
        else:
            print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.RED} Login failed for {email}: {err}")
        return None


def process_credentials(credentials):
    email_input, password_input = credentials
    api_token = proxy_tokens.get(email_input)  # Check for existing token

    if not api_token:  # Authenticate if no token is found
        api_token = authenticate(email_input, password_input)

    while True:
        if api_token:
            # Replace with your actual public IP if needed
            local_ip = get_local_ip()
            ip_info = get_ip_info(local_ip) 
            submit_bandwidth(email_input, api_token, ip_info)
            time.sleep(random.randint(60, 120))
            get_and_submit_task(email_input, api_token, ip_info)
            time.sleep(random.randint(60, 120))


def main():
    print(f"\n{Style.BRIGHT}Starting ...")
    credentials_list = read_credentials('data.txt')
    threads = []
    for credentials in credentials_list:
        thread = threading.Thread(
            target=process_credentials, args=(credentials,))
        thread.daemon = True
        threads.append(thread)
        thread.start()
        time.sleep(1)

    print(f"{Fore.LIGHTCYAN_EX}[{datetime.now().strftime('%H:%M:%S')}]{Fore.LIGHTCYAN_EX}[✓] DONE! Delay before next cycle. Not Stuck! Just wait...{Style.RESET_ALL}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Stopping ...")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}")
