import os
import re
import time
import json

CONFIG_FILE = "config.json"

def load_config():
    default_config = {
        "log_file_path": "app.log",
        "error_pattern": "ERROR|CRITICAL",
        "threshold": 5,
        "time_window_seconds": 60
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            print("Failed to read config.json, using defaults.")
    return default_config

def trigger_alert(count, window):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    alert_msg = f"[ALERT] {timestamp} - High error frequency detected: {count} errors in the last {window} seconds!\n"
    print(alert_msg.strip())
    
   
    with open("alerts.log", "a") as alert_file:
        alert_file.write(alert_msg)

def monitor_log():
    config = load_config()
    log_path = config["log_file_path"]
    error_regex = re.compile(config["error_pattern"], re.IGNORECASE)
    threshold = config["threshold"]
    window = config["time_window_seconds"]

    print(f"Monitoring '{log_path}' for pattern '{config['error_pattern']}'...")
    print(f"Alert configuration: {threshold} errors within {window} seconds.")

    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            f.write("--- Log stream initialized ---\n")

    with open(log_path, "r") as f:
       
        f.seek(0, os.SEEK_END)
        error_timestamps = []

        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue

            if error_regex.search(line):
                current_time = time.time()
                error_timestamps.append(current_time)
                print(f"[MATCH] {line.strip()}")

               
                error_timestamps = [t for t in error_timestamps if current_time - t <= window]

                if len(error_timestamps) >= threshold:
                    trigger_alert(len(error_timestamps), window)
                    error_timestamps.clear() 

if __name__ == "__main__":
    try:
        monitor_log()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        