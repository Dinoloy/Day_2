import pyautogui
import time
import subprocess

# Emergency stop
pyautogui.FAILSAFE = True

# Small delay after every PyAutoGUI command
pyautogui.PAUSE = 0.3

print("Opening Notepad...")

# Open Notepad
subprocess.Popen("notepad.exe")

# Wait for Notepad to open
time.sleep(3)

# Find Notepad window
windows = pyautogui.getWindowsWithTitle("Notepad")

if not windows:
    print("Notepad window not found!")
    exit()

# Activate Notepad
notepad = windows[0]
notepad.activate()

time.sleep(2)

print("Notepad activated.")

# Type text
pyautogui.write(
    "Hello, World! Lets get started!",
    interval=0.1
)

time.sleep(1)

# Select all text
pyautogui.hotkey('ctrl', 'a')

time.sleep(1)

# Copy selected text
pyautogui.hotkey('ctrl', 'c')

time.sleep(1)

# Go to end
pyautogui.press('end')

# New line
pyautogui.press('enter')

# Paste copied text
pyautogui.hotkey('ctrl', 'v')

time.sleep(1)

# New line
pyautogui.press('enter')

# Type another message
pyautogui.write(
    "Keyboard automation completed successfully!",
    interval=0.05
)

print("Keyboard automation completed!")

screenshot = pyautogui.screenshot()
screenshot.save("notepad_screenshot.png")