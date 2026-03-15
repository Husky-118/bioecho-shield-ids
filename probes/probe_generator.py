import os
import datetime
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "probe_logs.log")

PROBE_EVENTS = [
     "Fake admin login attempt created",
     "Unauthorized file access attempt on sensitive_data.txt",
     "Multiple failed login attempts detected for test_users",
     "Probe access to hidden admin panel detected"
   ]

def generate_probe():
    probe_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    event_message = random.choice(PROBE_EVENTS)

    probe_message = f"PROBE_EVENT | ID:{probe_id} | {event_message}"

    print("[+] Generating probe event...")
    print(probe_message)

    with open(LOG_FILE, "a") as log:
        log.write(probe_message + "\n")

    print("[+] Probe logged successfully.")

if __name__ == "__main__":
    generate_probe()