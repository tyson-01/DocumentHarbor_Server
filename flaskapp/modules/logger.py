from datetime import datetime

def log(message):
    if not message:
        print()
    else:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        print(f"{timestamp} {message}")