import os
import json
import sqlite3
import psutil
import subprocess
import socket
from datetime import datetime
import hashlib
import requests
import time

class CyberGuardian:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.cyberguardian")
        self.config_file = os.path.join(self.config_dir, "config.json")
        self.database_file = os.path.join(self.config_dir, "cyberguardian.db")
        self.bots = {
            "John": self.bot_john,
            "Jonathan": self.bot_jonathan,
            "Elizabeth": self.bot_elizabeth,
            "Jerry": self.bot_jerry,
            "Alice": self.bot_alice,
            "Guard": self.bot_guard,
            "Defender": self.bot_defender,
            "Watcher": self.bot_watcher,
            "Clean": self.bot_clean,
            "Watchdog": self.bot_watchdog,
            "Network": self.bot_network,
            "Integrity": self.bot_integrity,
            "Firewall": self.bot_firewall,
            "LiveMonitor": self.bot_live_monitor,
            "AI_Responder": self.bot_ai_responder
        }
        self.init_system()

    def init_system(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
        if not os.path.exists(self.database_file):
            self.setup_database()
        self.load_configuration()

    def setup_database(self):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS licenses (
                key TEXT PRIMARY KEY,
                valid_until DATE
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                event_type TEXT,
                message TEXT
            )
        """)
        conn.commit()
        conn.close()

    def load_configuration(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "language": "English",
                "license_key": None,
                "auto_update": True
            }
            with open(self.config_file, "w") as f:
                json.dump(self.config, f)

    def log_event(self, event_type, message):
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (timestamp, event_type, message) VALUES (?, ?, ?)",
                       (datetime.now(), event_type, message))
        conn.commit()
        conn.close()

    def bot_john(self):
        try:
            connections = psutil.net_connections(kind="inet")
            suspicious_ips = {}
            threshold = 50
            for conn in connections:
                if conn.status == "ESTABLISHED" and conn.raddr:
                    ip = conn.raddr.ip
                    suspicious_ips[ip] = suspicious_ips.get(ip, 0) + 1
                    if suspicious_ips[ip] > threshold:
                        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
                        self.log_event("ALERT", f"Blocked suspicious IP: {ip}")
        except Exception as e:
            self.log_event("ERROR", f"Bot John encountered an issue: {e}")

    def bot_jonathan(self):
        try:
            monitored_paths = ["/home", "/tmp"]
            for path in monitored_paths:
                if os.path.exists(path):
                    for root, _, files in os.walk(path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            with open(file_path, "rb") as f:
                                file_hash = hashlib.sha256(f.read()).hexdigest()
                                if self.check_file_in_virus_db(file_hash):
                                    os.remove(file_path)
                                    self.log_event("ALERT", f"Malicious file removed: {file_path}")
        except Exception as e:
            self.log_event("ERROR", f"Bot Jonathan encountered an issue: {e}")

    def check_file_in_virus_db(self, file_hash):
        virus_db = ["bad_hash1", "bad_hash2"]
        return file_hash in virus_db

    def bot_alice(self):
        try:
            suspicious_urls = self.get_suspicious_urls()
            for url in suspicious_urls:
                response = requests.get(url)
                if response.status_code == 200:
                    subprocess.run(["iptables", "-A", "INPUT", "-s", url, "-j", "DROP"], check=True)
                    self.log_event("ALERT", f"Blocked phishing URL: {url}")
        except Exception as e:
            self.log_event("ERROR", f"Bot Alice encountered an issue: {e}")

    def get_suspicious_urls(self):
        return ["http://example-phishing.com", "http://fakebank-login.com"]

    def bot_guard(self):
        try:
            data = {"cpu_usage": psutil.cpu_percent(), "ram_usage": psutil.virtual_memory().percent}
            if data["cpu_usage"] > 90:
                self.log_event("ALERT", "High CPU usage detected. Taking action.")
        except Exception as e:
            self.log_event("ERROR", f"Bot Guard encountered an issue: {e}")

    def run_all_bots(self):
        for bot_name, bot_function in self.bots.items():
            try:
                bot_function()
            except Exception as e:
                self.log_event("ERROR", f"Error running {bot_name}: {e}")

guardian = CyberGuardian()
guardian.run_all_bots()
