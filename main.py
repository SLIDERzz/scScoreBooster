
import ctypes, time, pyautogui, keyboard, threading, json
from os import system
import os
from colorama import Fore, Style, init

import getPosition

init(autoreset=True)

os.system('mode con: lines=25 cols=100')

titleText = """
 ____  _     ___ ____  _____ ____           
/ ___|| |   |_ _|  _ \| ____|  _ \  ________
\___ \| |    | || | | |  _| | |_) ||_  /_  /
 ___) | |___ | || |_| | |___|  _ < / / / / 
|____/|_____|___|____/|_____|_| \_\/___/___|
"""

sentSnaps = 0

def styled_input(prompt_text: str) -> str:
    return input(Fore.CYAN + Style.BRIGHT + "> " + prompt_text + Fore.RESET)

def info(text: str):
    print(Fore.GREEN + Style.BRIGHT + text)

def warn(text: str):
    print(Fore.RED + Style.BRIGHT + text)

def status(text: str):
    print(Fore.YELLOW + text)

# Läs JSON-fil
def get_positions(file: str) -> dict[str, list]:
    try:
        with open(file, "r") as pos_file:
            return json.load(pos_file)
    except FileNotFoundError:
        warn(f"File with given name: '{file}' was not found.")
        exit()

# Uppdatera fönstertitel
def updateTitle(sec_to_complete):
    global sentSnaps
    ctypes.windll.kernel32.SetConsoleTitleW(
        f"Score Booster | {sentSnaps} sent | ~{int(sec_to_complete)}s left | @SLIDERzz"
    )

# Huvudfunktionen som skickar snaps
def sendSnap(count: int, interval: float, delay: float, positions: dict[str, list], user: str, prompt=True):
    """Send snaps on snapchat using mouse movements.
    :param count: The amount of snaps to send
    :param interval: Time between each snap
    :param delay: The delay between each step/action
    :param positions: Dictionary including the names and positions of each step
    :param user: The username of the recipient whom the snaps will be sent to
    """
    global sentSnaps
    sec_to_complete: float = (count * (len(positions) * (delay * 2))) + (count - 1) * interval

    if prompt:
        proceed = styled_input(
            f"Estimated time until finished: "
            f"{int(sec_to_complete / 60)} minute{'s' if int(sec_to_complete / 60) > 1 else ''} "
            f"{int(sec_to_complete % 60)} second{'s' if int(sec_to_complete % 60) > 1 else ''}\n"
            f"Continue? [ENTER] / [N]: "
        ).lower()

        if "n" in proceed:
            return
    else:
        info(f"Estimated time until finished: "
             f"{int(sec_to_complete / 60)} minute{'s' if int(sec_to_complete / 60) > 1 else ''} "
             f"{int(sec_to_complete % 60)} second{'s' if int(sec_to_complete % 60) > 1 else ''}")

    # ... fortsätt som vanligt ...

    system("cls||clear")
    print(Fore.MAGENTA + titleText)
    info("Running\n")

    for i in range(count):
        if i:
            system("cls||clear") # Rensar efter varje runda
            print(Fore.MAGENTA + titleText)
            time.sleep(interval)

        sentSnaps += 1
        remaining = sec_to_complete - (i * (len(positions) * (delay * 2)) + i * interval)
        updateTitle(remaining)

        for stage, coords in positions.items():
            print(Fore.YELLOW + "[DEBUG]: " + Fore.LIGHTRED_EX + f"Stage: {stage}, " + Fore.LIGHTWHITE_EX + f"Coords: {coords}")
            pyautogui.click(x=coords[0], y=coords[1])
            time.sleep(delay)

            if stage == "usernameInputField":
                print(Fore.YELLOW + "[DEBUG]: " + Fore.LIGHTRED_EX + "Entered Name: " +  Fore.LIGHTWHITE_EX + user)
                pyautogui.write(user)
                time.sleep(.5) # Väntar så den hinner skriva.

    print(" " * 50, end="\r")

    pyautogui.press("esc")

# Avsluta med knapptryck
def exit_on_button_press(button: str = "esc"):
    while True:
        keyboard.wait(button)
        system("cls||clear")
        print(Fore.MAGENTA + titleText)
        warn("Exiting.")
        return True

# Huvudprogram
def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Score Booster | @SLIDERzz")
    system("cls||clear")
    print(Fore.MAGENTA + titleText)

    stage_positions: dict[str, list] = get_positions(file="ButtonPosition.json")

    count = styled_input("Snaps you wanna send (Default: 10): ")
    interval = styled_input("Interval between snaps (Default: 2): ")
    delay = styled_input("Delay between buttonClick (Default: .5): ")
    user = styled_input("Enter Name: ")
                     
    main_process = threading.Thread(
        target=sendSnap,
        args=(
            int(count) if count else 10,
            float(interval) if interval else 2,
            float(delay) if delay else .5,
            stage_positions,
            user,
            False
        ),
        daemon=True,
    )
    main_process.start()

    if exit_on_button_press():
        exit()

if __name__ == '__main__':
    print(Fore.MAGENTA + titleText)
    # Remove comments to ask everytime instead of checking for JSON file.
    #if "n" not in input("Calibrate positions (recommended)? [y/n]:\n > "):
        #getPosition.getPos() # Kan vara lika ostabila som mitt ex och alla talkin stages men man är problemlösare och gjorde ett simpelt tool för det.
    if not os.path.isfile("ButtonPosition.json"):
        warn("Position file not found.")
        info("Running calibration...")
        getPosition.getPos() # Running positioning automatically
    else:
        info("Position file found. Skipping calibration.")
    main()
