import random
import string
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to generate a random Gmail address
def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    random_email = random_string + "@gmail.com"
    return random_email

# Function to fetch the list of user-agent strings from the provided URL
def fetch_user_agents():
    url = "https://gist.github.com/pzb/b4b6f57144aea7827ae4"
    response = requests.get(url)
    
    if response.status_code == 200:
        user_agents = response.text.splitlines()  # Split the content into lines
        # Filter out any empty lines or comments (if any)
        user_agents = [ua.strip() for ua in user_agents if ua.strip() and not ua.startswith('#')]
        return user_agents
    else:
        print("Failed to fetch user-agents from the URL.")
        return []

# Function to automate referral signup on Euphoria Finance waitlist
def automate_referral(referral_code, num_referrals):
    try:
        # Fetch the user-agent list from the provided URL
        user_agents = fetch_user_agents()
        if not user_agents:
            print("No user-agents found. Exiting.")
            return
        
        # Setup WebDriver with headless option
        options = Options()
        options.add_argument('--headless')  # Headless mode for environments without GUI
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        print("Driver initialized, starting automation.")

        # Loop for the number of referrals you want
        for i in range(num_referrals):
            # Generate a random email
            temp_email = generate_random_email()
            print(f"Referral {i + 1}: Using temporary email: {temp_email}")

            # Randomly select a user-agent for this referral
            user_agent = random.choice(user_agents)
            print(f"Using User-Agent: {user_agent}")

            # Apply the selected user-agent for this referral
            options.add_argument(f"user-agent={user_agent}")
            driver.quit()  # Close the existing driver to apply the new user-agent

            # Re-initialize the driver with the updated options (new user-agent)
            driver = webdriver.Chrome(options=options)

            # Open the referral URL with the referral code
            referral_url = f"https://euphoria.finance/?ref_id={referral_code}#waitlist"
            driver.get(referral_url)
            print(f"Opened referral URL: {referral_url}")

            # Wait for the email input field to be present
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

            try:
                # Find the email input field and fill it
                email_input = driver.find_element(By.NAME, "email")
                email_input.clear()  # Clear the field, in case it is pre-filled
                email_input.send_keys(temp_email)
                print(f"Entered email: {temp_email}")

                # Wait for the submit button to be present and visible
                submit_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".Button_button__8B4nB"))
                )

                # Scroll to the submit button aggressively
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom
                time.sleep(1)  # Allow some time for scrolling to finish
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                print("Scrolled to the submit button.")

                # Wait a bit for any potential animations or issues
                time.sleep(1)

                # Use JavaScript to click the submit button if normal click is not working
                driver.execute_script("arguments[0].click();", submit_button)
                print(f"Submitted referral for {temp_email}")

                # Wait a few seconds before proceeding to the next referral
                time.sleep(2)

            except Exception as e:
                print(f"Error during referral {i + 1}: {str(e)}")
                continue

        # Close the browser after completing all referrals
        driver.quit()
        print("Automation completed, browser closed.")

    except Exception as e:
        print(f"Error during automation: {str(e)}")

# Ask the user for the number of referrals to make
num_referrals = int(input("How many referrals would you like to make? "))  # Manually input number of referrals

# Example usage
referral_code = "QI3IBQJ8D"  # Your referral code
automate_referral(referral_code, num_referrals)
