import pyautogui
import time
import keyboard
import mss
import mss.tools
import numpy as np
import cv2
import pytesseract
from word_finder import get_all_words
from screen import Screen
import psutil


global BOARD_SIZE
BOARD_SIZE = 4

#dif = 106
positions = [[(779, 477), (824, 521)], [(885, 478), (926, 520)], [(986, 474), (1030, 521)], [(1097, 477), (1134, 522)], [(781, 583), (826, 626)], [(883, 579), (930, 630)], [(990, 579), (1035, 631)], [(1095, 584), (1136, 626)], [
    (787, 686), (822, 728)], [(884, 686), (930, 733)], [(992, 688), (1032, 730)], [(1094, 686), (1141, 730)], [(779, 792), (824, 835)], [(884, 789), (930, 844)], [(990, 785), (1033, 835)], [(1086, 788), (1143, 833)]]
results_real_time, all_letters = [], []
screen_coords = []
screen_coords_row = []
for i in positions:
    screen_coords_row.append(
        ((i[0][0] + i[1][0]) // 2, (i[0][1] + i[1][1]) // 2))
    # print(screen_coords_row)
    if len(screen_coords_row) == BOARD_SIZE:
        screen_coords.append(screen_coords_row)
        screen_coords_row = []

# print(screen_coords)

mon = []
for i in positions:
    _screen = Screen(pyautogui.size(), i[0], i[1])
    _mon = _screen.get_mon()
    mon.append(_mon)
# print(mon)

# record current mouse location and store in list of tuples (x,y)
coords = []
pos2 = None


def get_coords():
    while True:
        while True:
            if keyboard.read_key() == "shift":
                if pos2 == None:
                    pos1 = pyautogui.position()
                    print(f"Selected Pos1: {str(pos1)}")
                    pos2 = ()
                    time.sleep(0.5)
                else:
                    pos2 = pyautogui.position()
                    print(f"Selected Pos2: {str(pos2)}")
                    time.sleep(0.5)
                    break
            elif keyboard.read_key() == "q":
                print(coords)
                exit(0)
        coords.append([(pos1.x, pos1.y), (pos2.x, pos2.y)])
        pos1, pos2 = None, None


def clear_letters(letters):
    board_raw, board_raw_row = [], []
    for j in range(BOARD_SIZE**2):
        board_raw_row.append(letters[j].replace(
            "|", "I").replace("\n", "").replace("0", "o").lower()[-1])
        if len(board_raw_row) == BOARD_SIZE:
            board_raw.append(board_raw_row)
            board_raw_row = []
    return letters, board_raw


def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


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
if len(all_letters) != BOARD_SIZE ** 2:
    print("ERROR: COULDN'T FIND LETTERS")
    exit()
letters, board_raw = clear_letters(all_letters)

# Getting words into AI
print("\nLoading letters into AI...")
words_found_dupped, words_only = get_all_words(board_raw)
words_found = []
check_val = set()
for i in words_found_dupped:
    if i[0] not in check_val:
        words_found.append(i)
        check_val.add(i[0])
words_found.sort(key=lambda a: len(a[0]), reverse=True)
# print(words_found)

pyautogui.move(960, 540)
# time.sleep(1)
for word in words_found:
    print(f"Inputing:  {word}")
    # time.sleep(5)
    for coords in word[1:]:
        for coord in coords:
            coords_x, coords_y = screen_coords[coord[0]][coord[1]]
            print(coords_x, coords_y)
            pyautogui.moveTo(coords_x, coords_y)
            pyautogui.mouseDown()
            print(coord)

        """if keyboard.read_key() == "shift":
            exit()
        else:"""
        pyautogui.mouseUp()
        time.sleep(0.7)
