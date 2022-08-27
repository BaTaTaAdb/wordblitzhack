import numpy as np
import pickle as pkl
import psutil


def main():
    global next_free_elem
    global word_parsed
    next_free_elem = 3
    d2 = (800_000, 27)
    word_parsed = np.zeros(d2, dtype=np.int32)
    eng_dict = load_words()
    parse_words(eng_dict)
    print(word_parsed[:15])
    print(next_free_elem)
    save_array(word_parsed)


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


def word_processer(word):
    global next_free_elem
    cur_elem = 2
    len_word = len(word)
    index = 1
    # print("Processing word:", word)
    # converts letter to index using ascii convertion
    for letter in word:
        letter_index = ord(letter) - 97
        # !!!
        stored_value = word_parsed[cur_elem][letter_index]
        #print(f"index: {index}. len_word = {len_word}. letter: {letter}")
        if index < len_word:
            if stored_value == 0 or stored_value == -1:
                if stored_value == -1:
                    word_parsed[cur_elem][letter_index] = -next_free_elem
                else:
                    word_parsed[cur_elem][letter_index] = next_free_elem
                cur_elem = next_free_elem
                next_free_elem += 1
            else:
                if stored_value < 0:
                    cur_elem = -stored_value
                else:
                    cur_elem = stored_value
        else:
            if stored_value == 0:
                word_parsed[cur_elem][letter_index] = -1
            elif stored_value > 0:
                word_parsed[cur_elem][letter_index] = -stored_value
        index += 1


def load_words():
    with open('words_alpha.txt') as word_file:
        dict_words = set(word_file.read().split())
    return dict_words


def parse_words(set):
    word_limit = -1
    for i in set:
        if word_limit == 0:
            break
        word_limit -= 1
        word_processer(i)


def save_array(array):
    with open("parsed_words.pkl", "wb") as f:
        pkl.dump(array, f)


def generate_array():
    with open("parsed_words.pkl", "rb") as f:
        return pkl.load(f)


if __name__ == '__main__':
    main()
