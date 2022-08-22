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

global BOARD_SIZE
BOARD_SIZE = 4
ELIM_COLOR_MIN = np.array((0, 0, 50))  # BGR
ELIM_COLOR_MAX = np.array((100, 100, 255))

screen_coord = (733, 23, 1186, 1031)
dif = 106
positions = [[(779, 477), (824, 521)], [(885, 478), (926, 520)], [(986, 474), (1030, 521)], [(1097, 477), (1134, 522)], [(781, 583), (826, 626)], [(883, 579), (930, 630)], [(990, 579), (1035, 631)], [(1095, 584), (1136, 626)], [
    (787, 686), (822, 728)], [(884, 686), (930, 733)], [(992, 688), (1032, 730)], [(1094, 686), (1141, 730)], [(779, 792), (824, 835)], [(884, 789), (930, 844)], [(990, 785), (1033, 835)], [(1086, 788), (1143, 833)]]
"""positions = [[(783, 478), (1130, 517)], [(783, 584), (1130, 621)],
             [(783, 690), (1130, 725)], [(783, 794), (1130, 831)]]"""
"""positions = [[(786, 478), (824, 520)], [(783, 584), (1130, 621)],
             [(783, 690), (1130, 725)], [(783, 794), (1130, 831)]]"""
results_real_time, all_letters = [], []

mon = []
for i in positions:
    _screen = Screen(pyautogui.size(), i[0], i[1])
    _mon = _screen.get_mon()
    mon.append(_mon)
print(mon)

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
            "|", "I").replace("\n", "").lower()[-1])
        print(len(board_raw_row))
        if len(board_raw_row) == BOARD_SIZE:
            board_raw.append(board_raw_row)
            board_raw_row = []
    return letters, board_raw


for i in range(BOARD_SIZE**2):
    results_are_consistant = [False * 5]
    results_real_time = []
    with mss.mss() as sct:
        im = np.asarray(sct.grab(mon[i]))
        """im = np.asarray(
            sct.grab({"left": 0, "top": 0, "height": 1920, "width": 1080}))"""
        grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(
            grayImage, 127, 255, cv2.THRESH_BINARY)

        results_real_time.append(pytesseract.image_to_string(
            blackAndWhiteImage, config="--psm 10"))
        # print(text)
        # print(results_real_time)

        #cv2.imshow('Image', im)
        cv2.imshow("BLACKANDWHITE", blackAndWhiteImage)
        # Press "q" to quit
        """if cv2.waitKey(2) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            exit()"""
        # print(text)
        """if len(results_real_time) >= 2:
            print(all(results_are_consistant[-5:-1]))
            results_real_time = results_real_time[-5:-1]
            for i in range(len(results_real_time)-1):
                results_are_consistant.append(
                    results_real_time[i] == results_real_time[i+1])
            if all(results_are_consistant[-5:-1]):
                all_letters.append(results_real_time[-1])
                break"""
        all_letters.append(results_real_time[-1])


letters, board_raw = clear_letters(all_letters)
print(letters, "\n\n\n", board_raw)
words, words_processed = get_all_words(board_raw)
print(words_processed)
