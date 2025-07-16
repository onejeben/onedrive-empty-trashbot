from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# === Your Microsoft login credentials ===
EMAIL = "example@mail.com"
PASSWORD = "Password

# === 1. Launch Chrome ===
print("step 1")
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=options)
driver.maximize_window()
wait = WebDriverWait(driver, 30)

# === 2. Go to OneDrive login page directly ===
print("step 2")
driver.get("https://login.microsoftonline.com/")

# === 3. Log in ===
print("step 3")
email_box = wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))
email_box.clear()
email_box.send_keys(EMAIL)
email_box.send_keys(Keys.ENTER)

# Retry password until success
success = False
for attempt in range(5):
    try:
        password_box = wait.until(EC.presence_of_element_located((By.NAME, "passwd")))
        password_box.clear()
        password_box.send_keys(PASSWORD)
        print(f"Attempt {attempt + 1}: Typed password")
        password_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # === Handle Stay Signed In Prompt ===
        print("Checking for 'Stay signed in?' prompt...")
        try:
            stay_signed_in_no = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "idBtn_Back"))
            )
            stay_signed_in_no.click()
            print("❎ Clicked 'No' on stay signed in prompt.")
        except:
            print("ℹ️ No 'Stay signed in?' prompt appeared.")

        # Proceed if redirected to OneDrive
        WebDriverWait(driver, 10).until(lambda d: "live.com" in d.current_url or "microsoft.com" in d.current_url)
        success = True
        print("✅ Logged in successfully.")
        break
    except Exception as e:
        print("Password entry failed, retrying...", e)
        time.sleep(2)

if not success:
    print("❌ Failed to log in after 5 attempts. Exiting.")
    driver.quit()
    exit()

# === 3.5 Handle privacy notice ===
print("step 3.5")
if "privacynotice.account.microsoft.com" in driver.current_url:
    print("On privacy notice page, skipping to OneDrive.")
else:
    print("No privacy notice detected.")

# === 4. Redirect to OneDrive ===
print("Redirecting to OneDrive...")
driver.get("https://onedrive.live.com/")
time.sleep(5)

# === Handle marketing redirect ===
if "microsoft.com/en-us/microsoft-365/onedrive" in driver.current_url:
    print("⚠️ Landed on marketing page. Attempting to click 'Sign In'...")
    try:
        sign_in_btn = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign in")))
        sign_in_btn.click()
        print("✅ Clicked 'Sign in' on marketing page.")
        time.sleep(5)

        # === Handle second Stay Signed In prompt ===
        print("🔄 Checking for second 'Stay signed in?' prompt...")
        try:
            stay_signed_in_no = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "idBtn_Back"))
            )
            stay_signed_in_no.click()
            print("❎ Clicked 'No' on second 'Stay signed in' prompt.")
        except:
            print("ℹ️ No second 'Stay signed in' prompt detected.")

    except Exception as e:
        print("❌ Could not find or click 'Sign in' button on marketing page:", e)
        driver.quit()
        exit()

# === 5. Go to Recycle Bin ===
print("step 4")
driver.get("https://onedrive.live.com/?view=5")
wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(5)

# === 6. Confirm we're on OneDrive ===
try:
    wait.until(lambda d: "onedrive.live.com" in d.current_url)
    print("Login complete, proceeding to recycle bin...")
except:
    print("❌ Not logged in to OneDrive, quitting.")
    driver.quit()
    exit()
# === 6.5 Dismiss Microsoft 365 storage upsell modal if present ===
try:
    print("🔍 Checking for storage upgrade modal...")
    storage_popup_close = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Close']"))
    )
    storage_popup_close.click()
    print("✅ Closed storage upgrade popup.")
    time.sleep(2)
except:
    print("ℹ️ No storage upgrade popup found.")

# === 7.5 Dismiss "Import cloud photos and files" popup if present ===
try:
    print("Checking for import popup...")
    maybe_later_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Maybe later')]"))
    )
    maybe_later_button.click()
    print("✅ Dismissed import popup.")
    time.sleep(2)
except:
    print("ℹ️ No import popup found.")

# === 8. Select All Files and Delete ===
print("step 6")
body = driver.find_element(By.TAG_NAME, "body")
body.send_keys(Keys.CONTROL, 'a')
time.sleep(2)
body.send_keys(Keys.DELETE)
print("🗑️ Pressed DELETE on selected items.")
time.sleep(2)

# === 8.1 Handle confirmation popup ===
try:
    print("🔍 Looking for confirmation dialog...")

    # Try multiple selectors to confirm deletion
    delete_selectors = [
        (By.XPATH, "//button[normalize-space()='Delete']"),
        (By.XPATH, "//button[@data-automationid='confirmButton']"),
        (By.XPATH, "//button[contains(@aria-label, 'Delete')]"),
        (By.XPATH, "//button[contains(text(), 'Permanently delete')]"),
        (By.XPATH, "//button[.//span[text()='Delete']]"),
    ]

    confirm_delete_btn = None
    for by, value in delete_selectors:
        try:
            confirm_delete_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((by, value))
            )
            if confirm_delete_btn:
                confirm_delete_btn.click()
                print(f"✅ Clicked confirmation button using selector: {value}")
                time.sleep(2)
                break
        except:
            continue

    if not confirm_delete_btn:
        print("⚠️ Confirmation delete button not found.")

except Exception as e:
    print(f"❌ Error while trying to confirm deletion: {e}")

