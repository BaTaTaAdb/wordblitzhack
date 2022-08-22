from process import generate_array
import numpy as np
import sys


def get_all_words(board_raw):
    global trace_word_processed
    trace_word_processed = False
    global FIRST_LETTER_INDEX
    FIRST_LETTER_INDEX = 2
    global word_parsed

    word_parsed = generate_array()

    """board_raw = [["a", "e", "u", "d"], ["o", "b", "i", "l"],
                 ["u", "s", "a", "l"], ["t", "r", "c", "t"]]"""
    """board_raw = [["a", "m", "a", "f"], ["b", "e", "a", "r"],
                 ["t", "a", "p", "u"], ["g", "n", "i", "s"]]"""
    # board_raw = [["a", "b", "c", "d"], ["e", "f", "g", "h"],
    #             ["i", "j", "k", "l"], ["m", "n", "o", "p"]]
    """board_raw = [["p", "s", "m", "i"], ["a", "d", "o", "d"],
                 ["s", "i", "r", "t"], ["a", "s", "a", "s"]]"""

    if len(sys.argv) > 1:
        if sys.argv[-1] == "debug":
            trace_word_processed = True
            process_args()
            exit(0)
        board_raw = process_args()
    else:
        if trace_word_processed:
            debug_word()
            exit(0)

    board = board_pre_process(board_raw)
    print()
    board_processer(board)
    words, only_words = words_found, []
    # print(words_found, "\n\n\n")
    for i in range(len(words)):
        only_words.append(words[i][0])
    # print(only_words)
    words_processed = [x for x in only_words if any(
        ("a" in x, "e" in x, "i" in x, "o" in x, "u" in x)) and len(x) > 1]
    print("\n", sorted(
        list(dict.fromkeys(sorted(words_processed))), key=len, reverse=True))
    return words_found, words_processed


def check_letter_in_word(state, letter_index):
    stored_value = word_parsed[state][letter_index]

    # print("stored_value=[", stored_value, "]")

    # stop_process = stored_value in (-1, 0)
    stop_process = (stored_value == -1 or stored_value == 0)
    end_word = stored_value < 0
    next_state = abs(stored_value)
    return stop_process, end_word, next_state


def board_processer(board):
    global words_found
    words_found = []
    found_letters_start = []
    board_size = len(board)
    print("Loading.", end="")

    for y in range(board_size):
        for x in range(board_size):
            print(".", end="")
            processed_path = np.zeros((board_size, board_size), np.int8)
            coords_start = []
            found_letters_start = []
            # if y == 1 and x == 0:
            #     print(y, x)
            # print("\n\n", "Main letter:[", chr(
            #     board[y][x] + 97), "]   Y=[", y, "] X=[", x, "]\n", processed_path)
            # print("==================================================")
            find_words(board, processed_path, found_letters_start, coords_start,
                       y, x, FIRST_LETTER_INDEX, 0)


def board_pre_process(board_raw):
    board = np.zeros((len(board_raw), len(board_raw)), dtype=np.int32)
    # print(board)
    for i in range(len(board)):
        for j in range(len(board)):
            board[i][j] = ord(board_raw[i][j]) - 97
    return board


def find_words(board, processed_path, letters, coords, start_y, start_x, cur_state, level):
    cur_proc_path = processed_path
    # found_letters = []
    found_letters = letters
    found_coords = coords

    # Signal this letter position was processed
    # processed_path[start_y][start_x] = 1

    level += 1

    # Debug
    # if abs(cur_state) == 1089:
    #     print(word_parsed[abs(cur_state)])
    #
    # if level == 4 and start_y == 1 and start_x == 3:
    #     print("Test [R]")

    # print(processed_path)
    found_letters.append(chr(board[start_y][start_x] + 97))
    found_coords.append((start_y, start_x))
    # print(found_coords)

    stop_process, end_word, next_state = check_letter_in_word(
        cur_state, board[start_y][start_x])

    # stop_process = (level == 4)
    # end_word = (level == 4)
    # next_state = 999

    # print(stop_process, end_word)

    # print("     [", chr(board[start_y][start_x] + 97), "]  ",
    #       stop_process, end_word, next_state, level, "Found=", found_letters, "\n")

    if end_word:
        current_word = ""
        for i in found_letters:
            current_word += i
        # print(found_coords)
        words_found.append((current_word, list(found_coords)))
        # print(words_found)

    if stop_process:
        # print("  --Return")
        return

    cur_proc_path[start_y][start_x] = 1

    for delta_y in (-1, 0, 1):
        for delta_x in (-1, 0, 1):
            current_y = start_y + delta_y
            current_x = start_x + delta_x

            if (current_y >= 0 and current_x >= 0 and current_y < len(board) and current_x < len(board)):
                # print("Y=[", current_y, "] X=[", current_x,
                #       "] Dy=[", delta_y, "] Dx=[", delta_x, "] Flag:", processed_path[current_y][current_x])
                if processed_path[current_y][current_x] == 0:
                    #print("\n\n+++++++++\nPRINT BEFORE", level, found_letters)
                    find_words(board, cur_proc_path, found_letters, found_coords,
                               current_y, current_x, next_state, level)
                    found_letters.pop(-1)
                    found_coords.pop(-1)
    if level != 1:
        cur_proc_path[start_y][start_x] = 0

        #print("\nPRINT AFTER", level, found_letters)


def trace_word(word):
    curr = 2
    for i in range(len(word)):
        print(f"\nWord: {word[0:i+1]}\nLevel {i} State:[", curr, "]:\n==================\n",
              word_parsed[abs(curr)], "\n")
        curr = word_parsed[abs(curr), ord(word[i]) - 97]


def process_args():
    if sys.argv[1] == "debug":
        if len(sys.argv) == 3:
            debug_word(sys.argv[-1])
        else:
            debug_word()
    elif sys.argv[1] == "input":
        if len(sys.argv) == 6:
            board_raw = []
            for row in sys.argv[2::]:
                if len(row) == 4:
                    board_raw.append(row)
                else:
                    print("[ERROR] INPUT INVALID.")
                    exit(-1)
            return board_raw


def debug_word(word=""):
    if word == "":
        word_to_debug = input("Enter word to debug: ")
        trace_word(word_to_debug)
    else:
        trace_word(word)


if __name__ == "__main__":
    get_all_words([["a", "e", "u", "d"], ["o", "b", "i", "l"],
                   ["u", "s", "a", "l"], ["t", "r", "c", "t"]])
