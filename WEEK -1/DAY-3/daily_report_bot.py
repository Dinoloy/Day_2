import pyautogui
import pyperclip
import subprocess
import time
import re
import threading
import imageio.v2 as imageio

from datetime import datetime
from pathlib import Path


# =========================================================
# SETTINGS
# =========================================================

CITY = "Chennai"

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.4

OUTPUT_FOLDER = Path(__file__).resolve().parent

# Screen recording settings
RECORD_INTERVAL = 0.5   # capture one frame every 0.5 sec
recording = False
frames = []


# =========================================================
# SCREEN RECORDING
# =========================================================

def record_screen():
    """
    Continuously capture screenshots while recording is True.
    """

    global recording, frames

    print("Screen recording started...")

    while recording:
        screenshot = pyautogui.screenshot()

        frames.append(
            screenshot.copy()
        )

        time.sleep(RECORD_INTERVAL)

    print("Screen recording stopped.")


def start_recording():
    """
    Start screen recording in a separate thread.
    """

    global recording, frames

    frames = []
    recording = True

    thread = threading.Thread(
        target=record_screen,
        daemon=True
    )

    thread.start()

    return thread


def stop_recording(thread, gif_path):
    """
    Stop recording and save collected frames as GIF.
    """

    global recording

    recording = False

    thread.join()

    print("Saving GIF...")

    if not frames:
        print("No frames were captured.")
        return

    imageio.mimsave(
        gif_path,
        frames,
        duration=RECORD_INTERVAL,
        loop=0
    )

    print(f"GIF saved:\n{gif_path}")


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def paste_text(text):
    pyperclip.copy(str(text))
    pyautogui.hotkey("ctrl", "v")


def wait(seconds, message="Waiting..."):
    print(f"{message} ({seconds} seconds)")
    time.sleep(seconds)


def open_chrome():

    print("\nSTEP 1: Opening Chrome...")

    pyautogui.hotkey("win", "r")
    time.sleep(1)

    pyautogui.write("chrome")
    pyautogui.press("enter")

    wait(4, "Waiting for Chrome to open")


def get_weather():

    print("\nSTEP 2: Opening weather website...")

    weather_url = f"https://wttr.in/{CITY}?format=3"

    pyautogui.hotkey("ctrl", "l")

    paste_text(weather_url)

    pyautogui.press("enter")

    wait(6, "Waiting for weather page to load")

    screen_width, screen_height = pyautogui.size()

    pyautogui.click(
        screen_width // 2,
        screen_height // 2
    )

    time.sleep(1)

    print("Copying weather information...")

    pyautogui.hotkey("ctrl", "a")
    time.sleep(1)

    pyautogui.hotkey("ctrl", "c")
    time.sleep(1)

    copied_text = pyperclip.paste().strip()

    print("Copied from browser:")
    print(copied_text)

    if not copied_text:
        raise RuntimeError(
            "No weather information was copied from Chrome."
        )

    return copied_text


def extract_temperature(weather_text):

    match = re.search(
        r"([+-]?\d+)\s*°C",
        weather_text
    )

    if match:
        return int(match.group(1))

    return None


def create_comment(temperature):

    if temperature is None:
        return "Weather information recorded"

    if temperature >= 35:
        return "Very hot - stay hydrated"

    elif temperature >= 30:
        return "Warm day - plan outdoor activities carefully"

    elif temperature >= 24:
        return "Good for outdoor activities"

    elif temperature >= 18:
        return "Pleasant and slightly cool"

    else:
        return "Cool weather today"


def open_excel():

    print("\nSTEP 3: Opening Microsoft Excel...")

    pyautogui.hotkey("win", "r")
    time.sleep(1)

    pyautogui.write("excel")
    pyautogui.press("enter")

    wait(6, "Waiting for Excel to open")

    pyautogui.hotkey("ctrl", "n")

    wait(2, "Creating blank workbook")


def enter_excel_data(date_time, weather_data, comment):

    print("\nSTEP 4: Entering report into Excel...")

    screen_width, screen_height = pyautogui.size()

    pyautogui.click(
        screen_width // 3,
        screen_height // 3
    )

    time.sleep(1)

    pyautogui.hotkey("ctrl", "home")

    # Header row
    paste_text("Date & Time")
    pyautogui.press("tab")

    paste_text("Weather Data")
    pyautogui.press("tab")

    paste_text("Comment")

    # Data row
    pyautogui.press("enter")
    pyautogui.press("home")

    paste_text(date_time)
    pyautogui.press("tab")

    paste_text(weather_data)
    pyautogui.press("tab")

    paste_text(comment)

    time.sleep(1)

    print("Formatting Excel sheet...")

    pyautogui.hotkey("ctrl", "a")

    time.sleep(1)

    pyautogui.hotkey("alt", "h")
    pyautogui.press("o")
    pyautogui.press("i")

    time.sleep(2)


def save_excel(file_path):

    print("\nSTEP 5: Saving Excel report...")

    pyautogui.press("f12")

    wait(3, "Opening Save As window")

    paste_text(str(file_path))

    time.sleep(1)

    pyautogui.press("enter")

    wait(4, "Saving workbook")

    print(f"Excel report saved:\n{file_path}")


def take_screenshot(screenshot_path):

    print("\nSTEP 6: Taking screenshot...")

    time.sleep(2)

    screenshot = pyautogui.screenshot()

    screenshot.save(screenshot_path)

    print(f"Screenshot saved:\n{screenshot_path}")


# =========================================================
# MAIN PROGRAM
# =========================================================

def main():

    recording_thread = None

    now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")

    current_date_time = now.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    excel_path = OUTPUT_FOLDER / (
        f"daily_report_{current_date}.xlsx"
    )

    screenshot_path = OUTPUT_FOLDER / (
        f"daily_report_{current_date}.png"
    )

    gif_path = OUTPUT_FOLDER / (
        f"daily_report_execution_{current_date}.gif"
    )

    try:

        print("=" * 60)
        print("DAILY STATUS REPORT BOT")
        print("=" * 60)

        print(
            "\nDo not use the mouse or keyboard "
            "while the bot is running."
        )

        print(
            "\nMove the mouse to the TOP-LEFT "
            "corner for emergency stop."
        )

        time.sleep(3)

        # -------------------------------------------------
        # START SCREEN RECORDING
        # -------------------------------------------------

        recording_thread = start_recording()

        # -------------------------------------------------
        # BROWSER
        # -------------------------------------------------

        open_chrome()

        weather_text = get_weather()

        temperature = extract_temperature(
            weather_text
        )

        if temperature is not None:
            print(
                f"\nTemperature detected: "
                f"{temperature}°C"
            )

        comment = create_comment(
            temperature
        )

        print(f"Comment: {comment}")

        # -------------------------------------------------
        # EXCEL
        # -------------------------------------------------

        open_excel()

        enter_excel_data(
            current_date_time,
            weather_text,
            comment
        )

        # -------------------------------------------------
        # SAVE EXCEL
        # -------------------------------------------------

        save_excel(
            excel_path
        )

        # -------------------------------------------------
        # SCREENSHOT
        # -------------------------------------------------

        take_screenshot(
            screenshot_path
        )

        # -------------------------------------------------
        # STOP RECORDING
        # -------------------------------------------------

        stop_recording(
            recording_thread,
            gif_path
        )

        recording_thread = None

        # -------------------------------------------------
        # COMPLETE
        # -------------------------------------------------

        print("\n" + "=" * 60)
        print("AUTOMATION COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print(
            f"\nExcel file:\n{excel_path}"
        )

        print(
            f"\nScreenshot:\n{screenshot_path}"
        )

        print(
            f"\nExecution GIF:\n{gif_path}"
        )

    except pyautogui.FailSafeException:

        print(
            "\nBot stopped using PyAutoGUI FAILSAFE."
        )

    except KeyboardInterrupt:

        print(
            "\nBot stopped manually."
        )

    except Exception as error:

        print("\nAn error occurred:")
        print(error)

    finally:

        # Make sure recording stops even if an error occurs
        global recording

        if recording:
            recording = False

        if recording_thread is not None:
            recording_thread.join()


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":
    main()