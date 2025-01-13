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

                # Check for and close any potential popups or overlays
                try:
                    # If there's a close button for an overlay, click it
                    close_button = driver.find_element(By.CLASS_NAME, "close-button-class")  # Replace with actual class if known
                    close_button.click()
                    print("Closed potential overlay.")
                except:
                    print("No overlay or popup found.")

                # Wait for the submit button to be clickable
                submit_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".Button_button__8B4nB"))
                )

                # Scroll to the submit button to ensure it's in the viewport
                driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                print("Scrolled to the submit button.")

                # Click the submit button
                submit_button.click()
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
