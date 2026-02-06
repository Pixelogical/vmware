import time
import subprocess
import psutil
import keyboard
import pyotp

from pywinauto import Application, Desktop
from pywinauto.timings import wait_until_passes
from config import *

# =========================
# CONFIG
# =========================
VMWARE_PATH = r"C:\Program Files\VMware\VMware Horizon View Client\vmware-view.exe"
VMWARE_PROCESS = "vmware-view.exe"



OTP_SECRET = "ICBXZEDMYQVZIG2UQ2NN3Y55RK4NH4LO"

DOUBLE_PRESS_INTERVAL = 0.4


# =========================
# UTILS
# =========================
def is_process_running(name: str) -> bool:
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            return True
    return False


def launch_vmware():
    subprocess.Popen(VMWARE_PATH)
    time.sleep(3)  # initial startup delay


def connect_vmware_app():
    return Application(backend="uia").connect(path=VMWARE_PROCESS)


def wait_for_main_window(timeout=5):
    def _get():
        return Desktop(backend="uia").window(title_re=".*VMware Horizon.*")

    wait_until_passes(timeout, 1, _get)
    return _get()


def generate_otp():
    totp = pyotp.TOTP(OTP_SECRET)
    return totp.now()


# =========================
# CORE AUTOMATION
# =========================
def ensure_vmware_main_page():
    if not is_process_running(VMWARE_PROCESS):
        launch_vmware()
        return connect_vmware_app()

    app = connect_vmware_app()

    try:
        win = wait_for_main_window()

        # go back to main page
        win.set_focus()
        win.type_keys("{ESC}")
        time.sleep(0.4)
        win.type_keys("{ESC}")
        time.sleep(0.5)

    except Exception:
        pass

    return app


def open_server_and_login(app):
    win = wait_for_main_window()
    win.set_focus()

    # double click server
    item = win.child_window(
        title=SERVER_TITLE,
        control_type="ListItem"
    ).wrapper_object()

    item.double_click_input()
    time.sleep(0.5)

    # enter password
    password_box = win.child_window(
        auto_id="passwordBox",
        control_type="Edit"
    ).wrapper_object()

    password_box.set_focus()
    password_box.type_keys("^a{BACKSPACE}")
    password_box.type_keys(PASSWORD, with_spaces=True)

    time.sleep(0.5)
    win.type_keys("{ENTER}")

    # OTP step
    otp = generate_otp()

    otp_box = win.child_window(
        control_type="Edit"
    ).wrapper_object()

    otp_box.set_focus()
    otp_box.type_keys("^a{BACKSPACE}")
    otp_box.type_keys(otp, with_spaces=True)
    time.sleep(0.5)

    win.type_keys("{ENTER}")


# =========================
# HOTKEY LISTENER
# =========================
last_caps_time = 0


def on_capslock(event):
    global last_caps_time
    now = time.time()

    if now - last_caps_time <= DOUBLE_PRESS_INTERVAL:
        run_automation()

    last_caps_time = now


def run_automation():
    try:
        app = ensure_vmware_main_page()
        time.sleep(0.5)
        open_server_and_login(app)

    except Exception as e:
        print("Automation error:", e)


# =========================
# MAIN LOOP
# =========================
def main():
    keyboard.on_press_key("caps lock", on_capslock)
    keyboard.wait()  # invisible background wait


if __name__ == "__main__":
    main()
