import random as rand
import pyautogui
import time
import keyboard
import mss
import mss.tools
import numpy as np
import cv2
import pytesseract
from word_finder import get_all_words
from get_coords import Board
from screen import Screen
from process import checkIfProcessRunning
import psutil
import os
import subprocess
from datetime import datetime, timedelta

global CLICK_PAUSE_BASE_MS, CLICK_PAUSE_DELTA_MS
CLICK_PAUSE_BASE_MS = 32
CLICK_PAUSE_DELTA_MS = 10

OP_MODE = False

SERIAL = "42a91663"
round_time = timedelta(seconds=76)
if SERIAL == "":
    print("Please fill in the SERIAL variable according to your device's.")
    exit(0)

global BOARD_SIZE
BOARD_SIZE = 4


def random_pause_sec():
    pyautogui.PAUSE = (CLICK_PAUSE_BASE_MS +
                       rand.randint(-CLICK_PAUSE_DELTA_MS//2, CLICK_PAUSE_DELTA_MS//2))/1000


def clear_letters(letters):
    board_raw, board_raw_row, only_letters = [], [], []
    error = False
    if not len(letters) == BOARD_SIZE**2:
        error = True
        return only_letters, board_raw, error
    for j in range(BOARD_SIZE**2):
        board_raw_row.append(letters[j].replace(
            "|", "I").replace("\n", "").replace("0", "o").replace(")", "s").replace("4", "x").replace("¥", "y").replace("$", "s").replace("(", "s").replace(")", "s").replace("£", "e").replace("§", "s").lower()[-1])
        only_letters.append(letters[j].replace(
            "|", "I").replace("\n", "").replace("0", "o").replace(")", "s").replace("4", "x").replace("¥", "y").replace("$", "s").replace("(", "s").replace(")", "s").replace("£", "e").replace("§", "s").lower()[-1])
        if len(board_raw_row) == BOARD_SIZE:
            board_raw.append(board_raw_row)
            board_raw_row = []
    return only_letters, board_raw, error


"""positions_real = [[(779, 477), (824, 521)], [(885, 478), (926, 520)], [(986, 474), (1030, 521)], [(1097, 477), (1134, 522)], [(781, 583), (826, 626)], [(883, 579), (930, 630)], [(990, 579), (1035, 631)], [(1095, 584), (1136, 626)], [
    (787, 686), (822, 728)], [(884, 686), (930, 733)], [(992, 688), (1032, 730)], [(1094, 686), (1141, 730)], [(779, 792), (824, 835)], [(884, 789), (930, 844)], [(990, 785), (1033, 835)], [(1086, 788), (1143, 833)]]"""
board = Board((762, 450), (1158, 843), 4)
board.fill_coords()
positions_real = board.board
# print(positions_real)

screen_coords = []
screen_coords_row = []
for i in positions_real:
    screen_coords_row.append(
        ((i[0][0] + i[1][0]) // 2, (i[0][1] + i[1][1]) // 2))
    # print(screen_coords_row)
    if len(screen_coords_row) == BOARD_SIZE:
        screen_coords.append(screen_coords_row)
        screen_coords_row = []

mon = []
for i in positions_real:
    _screen = Screen(pyautogui.size(), i[0], i[1])
    _mon = _screen.get_mon()
    mon.append(_mon)

while True:
    results_real_time, all_letters = [], []
    print("Checking if scrcpy is running:", end=" ")
    if checkIfProcessRunning("scrcpy.exe"):
        print("Online.")
    else:
        old_dir = os.getcwd()
        print("Offline\n  => Starting adb...")
        os.chdir("scrcpy-win64-v1.24")
        # os.system("taskkill /f /im adb.exe")
        """if (f'cscript scrcpy-noconsole.vbs -s {SERIAL}') == 0:
            print("scrcpy and adb started successfully.")"""

        process = subprocess.Popen(
            f"scrcpy.exe -s {SERIAL}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        for i in range(60):
            if checkIfProcessRunning("scrcpy.exe"):
                print("scrcpy started... initiating letters scan on input.")
                break
            else:
                time.sleep(0.5)

        else:
            print("couldn't start scrcpy nor adb. Please try again.")
            exit(-1)
        os.chdir(old_dir)

    print("  => Press shift to start")
    while True:
        if keyboard.read_key() == "shift":
            end_time = datetime.now()+round_time
            board.write_pic()
            break
        elif keyboard.read_key() == "q":
            exit(0)

    print("Finding letters.", end="")
    for i in range(BOARD_SIZE**2):
        print(".", end="")
        with mss.mss() as sct:
            im = np.asarray(sct.grab(mon[i]))
            grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            (thresh, blackAndWhiteImage) = cv2.threshold(
                grayImage, 127, 255, cv2.THRESH_BINARY)
            all_letters.append(pytesseract.image_to_string(
                blackAndWhiteImage, config="--psm 10"))
    print()
    if len(all_letters) != BOARD_SIZE ** 2:
        print("ERROR: COULDN'T FIND LETTERS")
        exit()
    only_letters, board_raw, error = clear_letters(all_letters)
    if error:
        break
    for i in board_raw:
        for j in i:
            print(j, end=" ")
        print()

    # Getting words into AI
    print("\nLoading letters into AI...")
    words_found_dupped, words_only = get_all_words(board_raw)
    words_found = []
    check_val = set()
    for i in words_found_dupped:
        if i[0] not in check_val:
            words_found.append(i)
            check_val.add(i[0])
    if OP_MODE:
        words_found.sort(key=lambda a: len(a[0]), reverse=True)
    print()

    # pyautogui.move(960, 540)
    # time.sleep(1)
    for word in words_found:
        random_pause_sec()
        print(f"Inputing:  {word}")
        # time.sleep(5)
        first_down = True
        #print(datetime.now(), end_time)
        if datetime.now() >= end_time:
            break
        for coords in word[1:]:
            for coord in coords:
                coords_x, coords_y = screen_coords[coord[0]][coord[1]]
                # print(coords_x, coords_y)

                pyautogui.moveTo(coords_x, coords_y, duration=0.05)
                if first_down:
                    pyautogui.mouseDown()
                # pyautogui.mouseDown()
            pyautogui.mouseUp()
            # time.sleep(0.7)
            time.sleep(0.12)
        first_down = False
