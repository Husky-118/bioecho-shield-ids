import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "probe_logs.log")
HONEYPOT_FILE = os.path.join(BASE_DIR, "honeypot_files", "Admin_Credentials.txt")

def log_file_access():
    event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    probe_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    event_message = f"PROBE_EVENT | ID:{probe_id} | Unauthorized file access attempt on Admin_Credentials.txt | Time:{event_time}"

    print("[+] Honeypot file accessed.")
    print(event_message)

    with open(LOG_FILE, "a") as log:
        log.write(event_message + "\n")

    print("[+] File access event logged successfully.")

if __name__ == "__main__":
    log_file_access()