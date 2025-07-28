import os
from utils.Automation import Automation

def set_up_environment():
    # Ensure the store directory exists
    if not os.path.exists("store"):
        os.makedirs("store")

    if not os.path.exists("used_vouchers.txt"):
        with open("used_vouchers.txt", "w") as file:
            pass

    # Ensure the links.txt file exists
    if not os.path.exists("links.txt"):
        raise FileNotFoundError("links.txt file is missing. Please create it with the URLs to scrape.")
        
    print("Environment set up complete.")


if __name__ == "__main__":
    set_up_environment()
    automation = Automation()
    automation.run()