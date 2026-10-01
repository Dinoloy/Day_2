from playwright.sync_api import sync_playwright
from datetime import datetime

import pyautogui
import imageio.v2 as imageio
import numpy as np
import threading
import time


# =========================================================
# SETTINGS
# =========================================================

CHANNEL_URL = "https://www.youtube.com/@TheAIDude-Tamil"

# How long the latest video should play
VIDEO_PLAY_SECONDS = 15

# Capture one GIF frame every 0.5 seconds
CAPTURE_INTERVAL = 0.5

# PyAutoGUI emergency stop
pyautogui.FAILSAFE = True


# =========================================================
# GIF RECORDING
# =========================================================

recording = False
frames = []


def record_screen():
    """
    Capture the whole desktop repeatedly while recording is enabled.
    """

    global recording, frames

    print("GIF recording started...")

    while recording:

        try:
            screenshot = pyautogui.screenshot()

            frame = np.array(screenshot)

            frames.append(frame)

        except Exception as error:
            print(f"Screen capture error: {error}")

        time.sleep(CAPTURE_INTERVAL)

    print("GIF recording stopped.")


def start_recording():
    """
    Start screen recording in a background thread.
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
    Stop recording and convert the captured frames into a GIF.
    """

    global recording

    recording = False

    thread.join()

    if not frames:
        print("No GIF frames were captured.")
        return

    print("\nSaving GIF...")

    imageio.mimsave(
        gif_path,
        frames,
        duration=CAPTURE_INTERVAL,
        loop=0
    )

    print(f"GIF saved as: {gif_path}")


# =========================================================
# CREATE OUTPUT FILE NAMES
# =========================================================

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

channel_screenshot = (
    f"ai_dude_channel_{timestamp}.png"
)

videos_screenshot = (
    f"ai_dude_videos_{timestamp}.png"
)

video_screenshot = (
    f"ai_dude_latest_video_{timestamp}.png"
)

gif_path = (
    f"ai_dude_complete_execution_{timestamp}.gif"
)


# =========================================================
# START GIF RECORDING
# =========================================================

recording_thread = start_recording()

browser = None


# =========================================================
# PLAYWRIGHT AUTOMATION
# =========================================================

try:

    print("\nStarting test...")

    with sync_playwright() as p:

        # -------------------------------------------------
        # STEP 1 — OPEN GOOGLE CHROME
        # -------------------------------------------------

        print(
            "\nSTEP 1: Launching installed Google Chrome..."
        )

        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=300
        )

        print(
            "STEP 2: Chrome opened successfully."
        )

        # -------------------------------------------------
        # CREATE PAGE
        # -------------------------------------------------

        page = browser.new_page(
            viewport={
                "width": 1280,
                "height": 800
            }
        )

        print(
            "STEP 3: New page created."
        )

        # -------------------------------------------------
        # OPEN AI DUDE CHANNEL
        # -------------------------------------------------

        print(
            "\nSTEP 4: Opening AI Dude Tamil YouTube channel..."
        )

        page.goto(
            CHANNEL_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        # Allow YouTube to finish rendering
        page.wait_for_timeout(5000)

        print(
            "AI Dude YouTube channel loaded successfully."
        )

        # -------------------------------------------------
        # CHANNEL SCREENSHOT
        # -------------------------------------------------

        page.screenshot(
            path=channel_screenshot
        )

        print(
            f"Channel screenshot saved as:\n"
            f"{channel_screenshot}"
        )

        # -------------------------------------------------
        # OPEN VIDEOS PAGE
        # -------------------------------------------------

        print(
            "\nSTEP 5: Opening channel Videos page..."
        )

        videos_url = CHANNEL_URL + "/videos"

        page.goto(
            videos_url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        page.wait_for_timeout(5000)

        print(
            "Videos page loaded."
        )

        page.screenshot(
            path=videos_screenshot
        )

        print(
            f"Videos screenshot saved as:\n"
            f"{videos_screenshot}"
        )

        # -------------------------------------------------
        # FIND LATEST VIDEO
        # -------------------------------------------------

        print(
            "\nSTEP 6: Looking for latest uploaded video..."
        )

        # YouTube channel video cards
        video_links = page.locator(
            "a#video-title-link"
        )

        video_links.first.wait_for(
            state="visible",
            timeout=30000
        )

        video_count = video_links.count()

        print(
            f"Visible videos found: {video_count}"
        )

        latest_video = video_links.first

        # Get video title
        latest_video_title = latest_video.get_attribute(
            "title"
        )

        if not latest_video_title:
            latest_video_title = (
                latest_video.inner_text()
            )

        print(
            "\nLatest video detected:"
        )

        print(
            latest_video_title
        )

        # -------------------------------------------------
        # CLICK LATEST VIDEO
        # -------------------------------------------------

        print(
            "\nSTEP 7: Opening latest video..."
        )

        latest_video.click()

        page.wait_for_load_state(
            "domcontentloaded"
        )

        page.wait_for_timeout(5000)

        print(
            "Latest video page opened."
        )

        # -------------------------------------------------
        # WAIT FOR YOUTUBE PLAYER
        # -------------------------------------------------

        print(
            "\nSTEP 8: Waiting for YouTube player..."
        )

        video_player = page.locator(
            "video.html5-main-video"
        )

        video_player.wait_for(
            state="attached",
            timeout=30000
        )

        print(
            "YouTube video player detected."
        )

        # -------------------------------------------------
        # START VIDEO PLAYBACK
        # -------------------------------------------------

        print(
            "\nSTEP 9: Starting video playback..."
        )

        # Check whether video is paused
        is_paused = page.evaluate(
            """
            () => {
                const video =
                    document.querySelector(
                        'video.html5-main-video'
                    );

                return video ? video.paused : true;
            }
            """
        )

        if is_paused:

            print(
                "Video is paused. Clicking player..."
            )

            video_player.click(
                position={
                    "x": 500,
                    "y": 300
                }
            )

            page.wait_for_timeout(2000)

        # -------------------------------------------------
        # VERIFY PLAYBACK
        # -------------------------------------------------

        playback_status = page.evaluate(
            """
            () => {
                const video =
                    document.querySelector(
                        'video.html5-main-video'
                    );

                if (!video) {
                    return {
                        found: false
                    };
                }

                return {
                    found: true,
                    paused: video.paused,
                    currentTime: video.currentTime,
                    duration: video.duration
                };
            }
            """
        )

        print(
            f"Playback status: {playback_status}"
        )

        # -------------------------------------------------
        # DISPLAY PAGE TITLE
        # -------------------------------------------------

        page_title = page.title()

        print(
            f"\nCurrent page title:\n{page_title}"
        )

        # -------------------------------------------------
        # ALLOW VIDEO TO PLAY
        # -------------------------------------------------

        print(
            f"\nSTEP 10: Playing latest video for "
            f"{VIDEO_PLAY_SECONDS} seconds..."
        )

        for second in range(
            1,
            VIDEO_PLAY_SECONDS + 1
        ):

            print(
                f"Playing... {second}/"
                f"{VIDEO_PLAY_SECONDS} seconds"
            )

            time.sleep(1)

        # -------------------------------------------------
        # FINAL SCREENSHOT
        # -------------------------------------------------

        print(
            "\nSTEP 11: Taking final video screenshot..."
        )

        page.screenshot(
            path=video_screenshot
        )

        print(
            f"Video screenshot saved as:\n"
            f"{video_screenshot}"
        )

        # -------------------------------------------------
        # CHECK PLAYBACK POSITION
        # -------------------------------------------------

        current_time = page.evaluate(
            """
            () => {
                const video =
                    document.querySelector(
                        'video.html5-main-video'
                    );

                return video
                    ? video.currentTime
                    : 0;
            }
            """
        )

        print(
            f"\nVideo playback position: "
            f"{current_time:.1f} seconds"
        )

        # -------------------------------------------------
        # KEEP FINAL SCREEN VISIBLE
        # -------------------------------------------------

        print(
            "\nKeeping final video screen visible "
            "for 5 seconds..."
        )

        time.sleep(5)

        # -------------------------------------------------
        # CLOSE BROWSER
        # -------------------------------------------------

        print(
            "\nSTEP 12: Closing Chrome..."
        )

        browser.close()

        browser = None

        print(
            "Chrome closed successfully."
        )


# =========================================================
# ERROR HANDLING
# =========================================================

except Exception as error:

    print("\n" + "=" * 60)

    print("AUTOMATION ERROR")

    print("=" * 60)

    print(error)

    print(
        "\nKeeping browser visible for "
        "15 seconds for debugging..."
    )

    time.sleep(15)


# =========================================================
# STOP GIF RECORDING
# =========================================================

finally:

    print(
        "\nSTEP 13: Stopping GIF recording..."
    )

    stop_recording(
        recording_thread,
        gif_path
    )


# =========================================================
# COMPLETE
# =========================================================

print("\n" + "=" * 60)

print("AUTOMATION COMPLETED")

print("=" * 60)

print(
    f"\nChannel screenshot:\n"
    f"{channel_screenshot}"
)

print(
    f"\nVideos screenshot:\n"
    f"{videos_screenshot}"
)

print(
    f"\nLatest video screenshot:\n"
    f"{video_screenshot}"
)

print(
    f"\nFull execution GIF:\n"
    f"{gif_path}"
)