import pyautogui
import time
pyautogui.moveTo(100, 100, duration=1)  # Move mouse to coordinates (100, 100) over 1 second
pyautogui.doubleClick()  # Perform a double-click at the current mouse position
pyautogui.moveTo(200, 200, duration=1)  # Move mouse to coordinates (200, 200) over 1 second
pyautogui.rightClick()  # Perform a right-click at the current mouse position