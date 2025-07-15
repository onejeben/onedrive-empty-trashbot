import webbrowser
import time
import pyautogui

# 1. Open OneDrive in default browser
webbrowser.open('https://onedrive.live.com/')
print("Please log in to OneDrive in your browser.")
time.sleep(5)  # Wait for website and popup to load

# 2. Go to Recycle Bin
#webbrowser.open('https://onedrive.live.com/?id=5')
#print("Navigating to Recycle Bin...")
#time.sleep(10)  # Wait for Recycle Bin to load


# 3. Close pop-up
pyautogui.hotkey('esc')
time.sleep(1)
pyautogui.hotkey('enter')
time.sleep(3)

# 4. Open browser search and type 'recycle bin'
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


# 5. Confirm deletion (press Enter if confirmation dialog appears)

print("Recycle bin emptied (if items were present).")
