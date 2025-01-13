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
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
            print("Email input field found.")
        except Exception as e:
            print("Error: Email input field not found.")
            continue

        # Fill out the form with the generated email
        driver.find_element(By.NAME, "email").send_keys(temp_email)
        print(f"Entered email: {temp_email}")

        # Wait for the popup (if any) to disappear or close
        try:
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "WaitlistPopup_inner__Yybww")))
            print("Popup closed or became invisible.")
        except:
            print("No popup or failed to wait for popup to disappear.")

        # Scroll to the submit button to ensure it's in the viewport
        submit_button = driver.find_element(By.CLASS_NAME, "Button_button__8B4nB")
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)
        print("Scrolled to the submit button.")

        # Wait a bit before clicking (if there's animation or delay)
        time.sleep(1)

        # Try clicking the submit button
        try:
            submit_button.click()
            print(f"Submitted referral for {temp_email}")
        except Exception as e:
            # If normal click fails, use JavaScript to click the button
            driver.execute_script("arguments[0].click();", submit_button)
            print(f"JavaScript click for {temp_email}")

        # Wait for the success message or confirmation (check for URL change, page reload, etc.)
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'success')]")))
            print(f"Referral {temp_email} was successful!")
        except Exception as e:
            print(f"Error or referral not successful for {temp_email}")
        
        # Optional: Check if the URL changes to a confirmation page or a "thank you" page
        current_url = driver.current_url
        print(f"Current URL after submission: {current_url}")

    # Close the browser after completing all referrals
    driver.quit()
    print("Automation completed, browser closed.")
