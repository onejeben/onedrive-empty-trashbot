import webbrowser
import time
import pyautogui

try:

# Specify the full path to Chrome executable

    # Specify the full path to Chrome executable
    chrome_path = webbrowser.get('C:/Program Files/Google/Chrome/Application/chrome.exe %s')
    # 1. Open OneDrive in Google Chrome
    chrome_path.open('https://onedrive.live.com/login')
    print("Please log in to OneDrive in your browser.")
    time.sleep(15)  # Wait for manual login

    # --- Recycle Bin Automation ---
    # 2. Close pop-up
    pyautogui.hotkey('esc')
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(3)

    # 2b. Open browser search and type 'recycle bin'
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    pyautogui.typewrite('recycle bin')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)

    # 3. Empty the Recycle Bin 
    # Select all items (Ctrl+A)
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(1)
    # Press Delete
    pyautogui.press('delete')
    time.sleep(2)
    # Confirm deletion (press Enter if confirmation dialog appears)
    pyautogui.press('enter')
    time.sleep(3)
    print("Recycle bin emptied (if items were present).")



except KeyboardInterrupt:
    print("Script stopped by user.")
