
from datetime import datetime
import os

print(">>> RUNNING UPDATED main.py <<<")

def save_ticket(summary):
    base_dir = "output"

    today = datetime.now().strftime("%Y-%m-%d")
    day_dir = os.path.join(base_dir, today)

    os.makedirs(day_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%H%M%S")
    filename = f"ticket_{timestamp}.txt"
    filepath = os.path.join(day_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(summary)

    return filepath

def ask_text(question):
    while True:
        value = input(f"{question}: ").strip()
        if value:
            return value
        print("Input cannot be empty.")


def ask_yes_no(question):
    while True:
        value = input(f"{question} (yes/no): ").strip().lower()
        if value in ("yes", "no"):
            return value
        print("Invalid input. Please enter 'yes' or 'no'.")


def ask_choice(question, choices):
    while True:
        print(question)
        for key, value in choices.items():
            print(f"{key}. {value}")
        choice = input("Select an option: ").strip()
        if choice in choices:
            return choices[choice]
        print("Invalid selection. Please choose a valid option.")

def show_intro():
    print("\nIT Triage Assistant")
    print("This tool helps you report IT issues clearly and accurately.\n")


def select_category():
    return ask_choice(
        "Select the category that best describes your issue:",
        {
            "1": "Login or Account Access",
            "2": "Network or Wi-Fi Connectivity",
            "3": "Email or Phishing Concern",
            "4": "Slow Computer or Performance Issue",
            "5": "Software Error or Installation Problem"
        }
    )



def handle_login():
    print("\nLogin / Account Access")
    return {
        "device_os": ask_choice("Select operating system:", {"1": "windows", "2": "macos"}),
        "error_message": ask_text("Exact error message"),
        "start_time": ask_text("When did the issue start"),
        "password_change": ask_yes_no("Recent password change"),
        "multiple_users": ask_yes_no("Are other users affected")
    }


def handle_network():
    print("\nNetwork / Wi-Fi Connectivity")
    return {
         "wifi_connected": ask_yes_no("Connected to Wi-Fi"),
        "internet_access": ask_yes_no("Can you access any websites"),
        "multiple_users": ask_yes_no("Are other users affected"),
        "location": ask_choice("Select your location:", {"1": "on-site", "2": "remote"}),
        "start_time": ask_text("When did the issue start")
    }


def handle_phishing():
    print("\nEmail / Phishing Concern")
    return {
         "sender": ask_text("Sender email address"),
        "subject": ask_text("Email subject"),
        "clicked_link": ask_yes_no("Did you click a link"),
        "opened_attachment": ask_yes_no("Did you open an attachment"),
        "received_time": ask_text("When was the email received")
    }


def handle_performance():
    print("\nSlow Computer / Performance Issue")
    return {
        "device_type": ask_choice("Select device type:", {"1": "laptop", "2": "desktop"}),
        "start_time": ask_text("When did the slowness begin"),
        "frequency": ask_choice("Select frequency:", {"1": "constant", "2": "intermittent"}),
        "recent_changes": ask_yes_no("Recent installs or updates"),
        "popups": ask_yes_no("Pop-ups or unusual behavior")
    }

def handle_software():
    print("\nSoftware Error / Installation Problem")
    return {
        "application": ask_text("Application name"),
        "error_message": ask_text("Exact error message"),
        "start_time": ask_text("When did the issue start"),
        "restart_helped": ask_yes_no("Did restarting help"),
        "blocking": ask_yes_no("Is this blocking your work")
    }

def determine_impact(category, data):
    if data.get("multiple_users") == "yes":
        return "High"

    if category == "Email or Phishing Concern":
        if data.get("clicked_link") == "yes" or data.get("opened_attachment") == "yes":
            return "High"

    if data.get("blocking") == "yes":
        return "High"

    if category in ["Login or Account Access", "Software Error or Installation Problem"]:
        return "Medium"

    return "Low"


def map_priority(impact):
    if impact == "High":
        return "P1"
    if impact == "Medium":
        return "P2"
    return "P3"



def generate_summary(category, impact, priority, data):
    submitted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"Category: {category}",
        f"Impact Level: {impact}",
        f"Priority: {priority}",
        f"Submitted At: {submitted_time}",
        "",
        "Issue Details:"
    ]

    for key, value in data.items():
        lines.append(f"- {key.replace('_', ' ').capitalize()}: {value}")

    lines += [
        "",
        "Initial Technician Notes:",
        "- Review user-provided details",
        "- Validate scope and impact",
        "- Proceed with standard troubleshooting"
    ]

    return "\n".join(lines)

def main():
    show_intro()
    category = select_category()

    handlers = {
        "Login or Account Access": handle_login,
        "Network or Wi-Fi Connectivity": handle_network,
        "Email or Phishing Concern": handle_phishing,
        "Slow Computer or Performance Issue": handle_performance,
        "Software Error or Installation Problem": handle_software
    }

    data = handlers[category]()

    impact = determine_impact(category, data)
    priority = map_priority(impact)
    summary = generate_summary(category, impact, priority, data)

    print("\n--- Technician-Ready Ticket Summary ---\n")
    print(summary)

    file_path = save_ticket(summary)
    print(f"\nTicket saved to: {file_path}")


if __name__ == "__main__":
    main()
