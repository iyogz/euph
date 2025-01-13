from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Function to automate referral signup on Euphoria Finance waitlist
def automate_referral(referral_code, num_referrals):
    # Setup WebDriver with headless option
    options = Options()
    options.add_argument('--headless')  # Headless mode for environments without GUI
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)

    # Loop for the number of referrals you want
    for _ in range(num_referrals):
        # Generate a random email
        temp_email = generate_random_email()
        print(f"Using temporary email: {temp_email}")

        # Open the referral URL with the referral code
        referral_url = f"https://euphoria.finance/?ref_id={referral_code}#waitlist"
        driver.get(referral_url)

        # Wait for the email input field to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

        # Fill out the form with the generated email (no username or password)
        driver.find_element(By.NAME, "email").send_keys(temp_email)

        # Wait for the popup (if any) to disappear or close
        try:
            # Wait for the modal or popup to disappear (adjust the element or timeout if necessary)
            WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, "WaitlistPopup_inner__Yybww")))
        except:
            print("Popup did not appear or timed out.")

        # Scroll to the submit button to ensure it's in the viewport
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        driver.execute_script("arguments[0].scrollIntoView();", submit_button)

        # Wait a bit before clicking (if there's animation or delay)
        time.sleep(1)

        # Try clicking the submit button
        try:
            submit_button.click()
        except:
            # If normal click fails, use JavaScript to click the button
            driver.execute_script("arguments[0].click();", submit_button)

        # Wait for the page to load after submission
        time.sleep(5)

        # Optional: Check for a success message or other confirmation
        try:
            confirmation_message = driver.find_element(By.XPATH, "//div[contains(text(), 'success')]")
            print(f"Referral {temp_email} was successful!")
        except Exception as e:
            print(f"Error or referral not successful for {temp_email}")

    # Close the browser after completing all referrals
    driver.quit()
    
