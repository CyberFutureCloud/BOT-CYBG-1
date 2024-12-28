import os
import subprocess
import git
from datetime import datetime

# Define bot configurations
BOTS = [
    {"name": "bots", "script": "bots.py"}
]

# Function to start a bot
def start_bot(bot):
    try:
        subprocess.Popen(["python", bot["script"]])
        print(f"Started {bot['name']}")
    except Exception as e:
        print(f"Failed to start {bot['name']}: {e}")

# Command handlers
def info():
    print("\n--- CYBERGUARD INFO ---")
    print(f"Data wydania: {datetime.now().strftime('%Y-%m-%d')}")
    print("Licencja: Aktualna")
    print("Status: Aktywny")
    print("----------------------\n")

def update():
    try:
        repo_url = "https://github.com/CyberFutureCloud/CYBERBOT-GUARD.git"
        local_path = os.path.dirname(os.path.abspath(__file__))

        if not os.path.exists(local_path):
            os.makedirs(local_path)

        if os.path.exists(os.path.join(local_path, ".git")):
            repo = git.Repo(local_path)
            repo.remotes.origin.pull()
            print("Repository updated.")
        else:
            git.Repo.clone_from(repo_url, local_path)
            print("Repository cloned.")
    except Exception as e:
        print(f"Update failed: {e}")

# Main logic
def main():
    print("Welcome to CYBERGUARD Manager\n")

    while True:
        print("Available commands:")
        print("!info - Display information")
        print("!update - Update bots from repository")
        print("!start - Start all bots")
        print("!exit - Exit the manager\n")

        command = input("Enter a command: ").strip().lower()

        if command == "!info":
            info()
        elif command == "!update":
            update()
        elif command == "!start":
            print("Starting all bots...")
            for bot in BOTS:
                start_bot(bot)
        elif command == "!exit":
            print("Exiting CYBERGUARD Manager. Goodbye!")
            break
        else:
            print("Unknown command. Please try again.\n")

if __name__ == "__main__":
    main()
