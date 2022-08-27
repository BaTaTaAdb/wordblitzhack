import cv2
import mss
import mss.tools
import numpy as np
import time
import keyboard
import pyautogui
import random


class Board:
    def __init__(self, coord_top_left, coord_bottom_right, size):
        self.size = size
        self.top_left = coord_top_left
        self.bottom_right = coord_bottom_right
        self.margin_top = 28
        self.margin_bottom = 18
        self.margin_left = 23
        self.margin_right = 30
        self.delta_x = (self.bottom_right[0] - self.top_left[0]) // self.size
        self.delta_y = (self.bottom_right[1] - self.top_left[1]) // self.size

        # print(self.delta_x, self.delta_y)
        """        self.delta_x = 300
        self.delat_y = 300"""

    def fill_coords(self):
        self.board = []
        for y in range(self.size):
            for x in range(self.size):
                coord_top_x = self.top_left[0]+self.delta_x*x+self.margin_left
                coord_top_y = self.top_left[1]+self.delta_y*y+self.margin_top

                coord_bottom_x = self.top_left[0] + \
                    self.delta_x*(x+1)-self.margin_right
                coord_bottom_y = self.top_left[1] + \
                    self.delta_y*(y+1)-self.margin_bottom

                self.board.append([(coord_top_x, coord_top_y),
                                   (coord_bottom_x, coord_bottom_y)])
            # self.board.append(row)

    def write_pic(self):
        t = time.localtime()
        timestamp = time.strftime('%b-%d-%Y_%H%M', t)

        mon = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        # time.sleep(5)
        with mss.mss() as sct:
            im = np.asarray(sct.grab(mon))
            grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        image = cv2.cvtColor(grayImage, cv2.COLOR_GRAY2BGR)
        for i in range(16):
            rgbl = [255, 0, 0]
            random.shuffle(rgbl)
            Color = tuple(rgbl)
            # print(Color)
            image = cv2.rectangle(image,
                                  pt1=self.board[i][0], pt2=self.board[i][1], color=Color, thickness=2)
        cv2.imwrite(f"{timestamp}.png", image)


def get_coords():
    coords = []
    pos1, pos2 = None, None
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


def main():
    board = Board((762, 450), (1158, 843), 4)
    # board = Board((200, 200), (0, 0), 4)
    board.fill_coords()
    positions_real = board.board
    print(positions_real)

    # positions_real = [[(779, 477), (824, 521)], [(885, 478), (926, 520)], [(986, 474), (1030, 521)], [(1097, 477), (1134, 522)], [(781, 583), (826, 626)], [(883, 579), (930, 630)], [(990, 579), (1035, 631)], [(1095, 584), (1136, 626)], [
    #    (787, 686), (822, 728)], [(884, 686), (930, 733)], [(992, 688), (1032, 730)], [(1094, 686), (1141, 730)], [(779, 792), (824, 835)], [(884, 789), (930, 844)], [(990, 785), (1033, 835)], [(1086, 788), (1143, 833)]]

    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M', t)

    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    # time.sleep(5)
    im = cv2.imread("screen.png")
    grayImage = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(
        grayImage, 127, 255, cv2.THRESH_BINARY)
    image = cv2.cvtColor(blackAndWhiteImage, cv2.COLOR_GRAY2BGR)
    for i in range(16):
        if i == 5:
            pass
            # break
        rgbl = [255, 0, 0]
        random.shuffle(rgbl)
        Color = tuple(rgbl)
        print(Color)
        image = cv2.rectangle(image,
                              pt1=positions_real[i][0], pt2=positions_real[i][1], color=Color, thickness=2)
        """image = cv2.rectangle(image,
                            pt1=(0, 0), pt2=(200, 200), color=Color, thickness=i*2)"""
    cv2.imshow("positions highlighted", image)
    cv2.imwrite(f"{timestamp}.png", image)
    cv2.waitKey(0)

    # closing all open windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
