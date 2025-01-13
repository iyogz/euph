import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to generate a random Gmail address
def generate_random_email():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    random_email = random_string + "@gmail.com"
    return random_email

# Function to automate referral signup on Euphoria Finance waitlist
def automate_referral(referral_code, num_referrals):
    # Setup WebDriver (make sure you have ChromeDriver installed)
    driver = webdriver.Chrome()

    # Loop for the number of referrals you want
    for _ in range(num_referrals):
        # Generate a random email
        temp_email = generate_random_email()
        print(f"Using temporary email: {temp_email}")

        # Open the referral URL with the referral code
        referral_url = f"https://euphoria.finance/?ref_id={referral_code}#waitlist"
        driver.get(referral_url)

        # Wait for the page to load
        time.sleep(5)

        # Fill out the form with the generated email (no username or password)
        driver.find_element(By.NAME, "email").send_keys(temp_email)

        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        # Wait for the page to load after submission
        time.sleep(5)

        # Optional: You can check for a success message or other confirmation
        try:
            # This part will depend on the specific confirmation you want to check
            confirmation_message = driver.find_element(By.XPATH, "//div[contains(text(), 'success')]")
            print(f"Referral {temp_email} was successful!")
        except Exception as e:
            print(f"Error or referral not successful for {temp_email}")

    # Close the browser after completing all referrals
    driver.quit()

# Ask the user for the number of referrals to make
num_referrals = int(input("How many referrals would you like to make? "))

# Example usage
referral_code = "QI3IBQJ8D"  # Your referral code
automate_referral(referral_code, num_referrals)
