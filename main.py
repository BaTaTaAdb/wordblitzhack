from process import generate_array
import numpy as np


def main():
    global FIRST_LETTER_INDEX
    FIRST_LETTER_INDEX = 2
    global word_parsed
    """    global processed_path
    processed_path = np.zeros((20, 4, 4), np.int8)"""
    """global found_letters
    found_letters = np.chararray((20, 20))"""
    # print(found_letters)
    word_parsed = generate_array()
    """board_raw = [["a", "e", "u", "d"], ["o", "b", "i", "l"],
                 ["u", "s", "a", "l"], ["t", "r", "c", "t"]]"""
    board_raw = [["a", "m", "a", "f"], ["b", "e", "a", "r"],
                 ["t", "a", "p", "u"], ["g", "n", "i", "s"]]
    """board_raw = [["a", "b", "c", "d"], ["e", "f", "g", "h"],
                 ["i", "j", "k", "l"], ["m", "n", "o", "p"]]"""
                 
    # Debug
    curr=2
    print("\n\nLevel 1 State:[", curr, ]:\n==================\n", word_parsed[abs(curr)],"\n")
    
    # Letters "b"
    curr = word_parsed[abs(curr), ord("b" - 97)]
    print("\n\nLevel 2 [b] State:[", curr, ]:\n==================\n", word_parsed[abs(curr)],"\n")

    
    # Letters "be"
    curr = word_parsed[abs(curr), ord("e" - 97)]
    print("\n\nLevel 3 [be]:\n==================\n", word_parsed[abs(curr)],"\n")
                 
     # Letters "bea"
    curr = word_parsed[abs(curr), ord("a" - 97)]
    print("\n\nLevel 4 [bea]:\n==================\n", word_parsed[abs(curr)],"\n")                
                
                 
    board = board_pre_process(board_raw)
    board_processer(board)
    print(words_found)


def check_letter_in_word(state, letter_index):
    stored_value = word_parsed[state][letter_index]
    
    print("stored_value=[", stored_value, "]")
    
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
    for y in range(board_size):
        for x in range(board_size):
            processed_path = np.zeros((board_size, board_size), np.int8)
            found_letters_start = []
            if y == 1 and x == 0:
                print(y, x)
            print("\n\n", "Main letter:[", chr(
                board[y][x] + 97), "]   Y=[", y, "] X=[", x, "]\n", processed_path)
            print("==================================================")
            find_words(board, processed_path, found_letters_start,
                       y, x, FIRST_LETTER_INDEX, 0)


def board_pre_process(board_raw):
    board = np.zeros((len(board_raw), len(board_raw)), dtype=np.int32)
    # print(board)
    for i in range(len(board)):
        for j in range(len(board)):
            board[i][j] = ord(board_raw[i][j]) - 97
    return board


def find_words(board, processed_path, letters, start_y, start_x, cur_state, level):
    cur_proc_path = processed_path
    found_letters = []
    found_letters = letters

    # Signal this letter position was processed
    # processed_path[start_y][start_x] = 1

    level += 1
    
    
    ## Debug
    if abs(cur_state)==1089:
        print(word_parsed[abs(cur_state)])
    
    if level == 4 and start_y == 1 and start_x == 3:
        print("Test [R]")
    
    
    print(processed_path)
    found_letters.append(chr(board[start_y][start_x] + 97))

    stop_process, end_word, next_state = check_letter_in_word( cur_state, board[start_y][start_x])

    # stop_process = (level == 4)
    # end_word = (level == 4)
    # next_state = 999

    print(stop_process, end_word)

    print("     [", chr(board[start_y][start_x] + 97), "]  ",
          stop_process, end_word, next_state, level, "Found=", found_letters, "\n")

    if end_word:
        current_word = ""
        for i in found_letters:
            current_word += i
        words_found.append(current_word)

    if stop_process:
        print("  --Return")
        return

    cur_proc_path[start_y][start_x] = 1

    for delta_y in (-1, 0, 1):
        for delta_x in (-1, 0, 1):
            current_y = start_y + delta_y
            current_x = start_x + delta_x

            if (current_y >= 0 and current_x >= 0 and current_y < len(board) and current_x < len(board)):
                print("Y=[", current_y, "] X=[", current_x,
                      "] Dy=[", delta_y, "] Dx=[", delta_x, "] Flag:", processed_path[current_y][current_x])
                if processed_path[current_y][current_x] == 0:
                    #print("\n\n+++++++++\nPRINT BEFORE", level, found_letters)
                    find_words(board, cur_proc_path, found_letters,
                               current_y, current_x, next_state, level)
                    found_letters.pop(-1)
    if level != 1:
        cur_proc_path[start_y][start_x] = 0

        #print("\nPRINT AFTER", level, found_letters)


if __name__ == "__main__":
    main()
