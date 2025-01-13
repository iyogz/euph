import random
import string
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

# List of user-agent strings (feel free to add more)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    # You can add more user-agents if you need
]

# Function to automate referral signup on Euphoria Finance waitlist
def automate_referral(referral_code, num_referrals):
    try:
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
            options.add_argument(f"user-agent={user_agent}")  # Set custom user-agent
            driver.quit()  # Close previous instance to reset with new user-agent

            # Restart the browser with the new user-agent
            driver = webdriver.Chrome(options=options)
            print(f"Selected User-Agent: {user_agent}")

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
num_referrals = int(input("How many referrals would you like to make? "))

# Example usage
referral_code = "QI3IBQJ8D"  # Your referral code
automate_referral(referral_code, num_referrals)
