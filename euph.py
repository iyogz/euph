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
    url = "https://gist.github.com/bulletinmybeard/7e8d92b511b7b3681a0dd1438fe78411"
    response = requests.get(url)
    
    if response.status_code == 200:
        user_agents = response.text.splitlines()  # Split the content into lines
        user_agents = [ua.strip() for ua in user_agents if ua.strip() and not ua.startswith('#')]  # Clean up the list
        return user_agents
    else:
        print("Failed to fetch user-agents from the URL.")
        return []

# Function to automate referral signup
def automate_referral(referral_code, num_referrals):
    try:
        # Fetch the user-agent list
        user_agents = fetch_user_agents()
        if not user_agents:
            print("No user-agents found. Exiting.")
            return
        
        # Setup WebDriver options
        options = Options()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        print("Driver initialized. Starting automation...")

        # Loop for the number of referrals
        for i in range(num_referrals):
            temp_email = generate_random_email()  # Generate a random email
            print(f"Referral {i + 1}: Using email {temp_email}")

            user_agent = random.choice(user_agents)  # Select a random user-agent
            print(f"Using User-Agent: {user_agent}")

            # Set the user-agent
            options.add_argument(f"user-agent={user_agent}")
            driver.quit()  # Restart driver to apply new user-agent
            driver = webdriver.Chrome(options=options)

            # Construct the referral URL
            referral_url = f"https://euphoria.finance/?ref_id={referral_code}"
            driver.get(referral_url)
            print(f"Opened URL: {referral_url}")

            # Wait for the email input field
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

            try:
                email_input = driver.find_element(By.NAME, "email")
                email_input.clear()
                email_input.send_keys(temp_email)  # Enter the generated email
                print(f"Entered email: {temp_email}")

                # Wait for and click the submit button
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".Button_button__8B4nB"))
                )
                driver.execute_script("arguments[0].click();", submit_button)  # Click using JavaScript
                print(f"Submitted referral for email: {temp_email}")

                time.sleep(2)  # Short delay before the next iteration

            except Exception as e:
                print(f"Error during referral {i + 1}: {e}")
                continue

        driver.quit()  # Close the browser after finishing
        print("Automation completed. Browser closed.")

    except Exception as e:
        print(f"Error during automation: {e}")

# Main script
referral_code = input("Enter your referral code: ").strip()  # Ask the user for the referral code
num_referrals = int(input("How many referrals would you like to make? ").strip())  # Ask for number of referrals

automate_referral(referral_code, num_referrals)
