# Log Monitoring and Alert System

A lightweight, memory-efficient Python tool designed to monitor growing log files in real-time. It detects specific error patterns using regular expressions (Regex) and triggers automated alerts when error frequencies surpass configurable thresholds within a sliding time window.

## Features
- **Efficient Log Tailing:** Tracks the file pointer offset (`seek`) to read only newly appended lines, preventing heavy memory usage on large files.
- **Dynamic Configuration:** Decoupled log file paths, search patterns, alert thresholds, and time windows via a central `config.json` file.
- **Sliding Time Window:** Alerts trigger based on precise real-time error density rather than accumulated historical counts.
- **Persistent Evidence:** Outputs matching logs to the console and archives automated alert reports inside an `alerts.log` file.

## Project Structure
```text
├── log_monitoring.py   # Main automation and regex tracking script
├── config.json         # Threshold configuration parameters
└── README.md           # Project documentation
```

## Setup & Execution

1. Clone this repository to your local workspace.
2. Configure your monitoring thresholds inside `config.json`:
   ```json
   {
     "log_file_path": "app.log",
     "error_pattern": "ERROR|CRITICAL",
     "threshold": 5,
     "time_window_seconds": 60
   }
   ```
3. Run the live log monitor using Python:
   ```bash
   python log_monitoring.py
   ```

## Sample Alert Evidence
When the error pattern frequency matches your threshold rules, entries are automatically written to `alerts.log`:
```text
[ALERT] 2026-09-10 14:30:15 - High error frequency detected: 5 errors in the last 60 seconds!
```

## Technical Interview Q&A
* **How would you monitor a continuously growing log file?**
  Instead of loading the entire log file into memory repeatedly, use standard python stream markers (`f.seek(0, os.SEEK_END)`). The script stays active at the file endpoint and reads incoming lines sequentially as they are generated.
* **What is log rotation?**
  Log rotation is an administrative practice where active log files are closed, archived, and renamed (e.g., `app.log` becomes `app.log.1`) based on size or age limits. A clean, empty file is then instantiated in its place to prevent system drive space exhaustion.
* **How can alert fatigue be reduced?**
  Alert fatigue is resolved by implementing grouping strategies, threshold time windows, and post-trigger cooling mechanics (throttling windows) to prevent flooding notifications for repetitive cascading failures.
