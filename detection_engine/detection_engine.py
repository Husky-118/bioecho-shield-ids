import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs","probe_logs.log")

def detect_intrusion():
    print("[+] Checking probe logs for suspicious activity...\n")

    if not os.path.exists(LOG_FILE):
        print("No log file found.")
        return

    with open(LOG_FILE, "r") as file:
        logs = file.readlines()

    if not logs:
        print("log file is empty")
        return

    for log in logs:
        if "PROBE_EVENT" in log:
            print("Potential intrusion interaction detected:")
            print(log.strip())

if __name__ == "__main__":
    detect_intrusion()