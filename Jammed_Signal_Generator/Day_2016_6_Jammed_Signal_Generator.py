import random
import os
from collections import Counter

def ecm_generator(unmodified_word: str, modified_word: str, how_many_repetitions: int = 572, 
                  seed: int = None) -> list:
    """This generates a list of random strings, with letters having different weight of occurance,
    based on the letters on the same index in unmodified_word (character is more common) or 
    modified_word (character is less common)."""
    if len(modified_word) != len(unmodified_word) or how_many_repetitions < 3:
        return []
    if seed:
        random.seed(seed)
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    weights = [4, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    scrambled_repetition = [ '' for _ in range(how_many_repetitions) ]
    for i in range(len(unmodified_word)):
        most_common = unmodified_word[i]
        least_common = modified_word[i]
        alphabet_list = [most_common, least_common] + \
            [ char for char in alphabet if char != most_common and char != least_common]
        while True:
            jammed_letter = ''.join(random.choices(alphabet_list, weights=weights, 
                                                    k=how_many_repetitions))
            letter_distributions = Counter(jammed_letter).most_common()
            least_in_scramble = min(letter_distributions, key= lambda x: x[1])
            most_in_scramble = max(letter_distributions, key= lambda x: x[1])
            occurance = [ v for k, v in letter_distributions ]
            most_unique = occurance.count(most_in_scramble[1]) == 1
            least_unique = occurance.count(least_in_scramble[1]) == 1
            if most_common == most_in_scramble[0] and least_common == least_in_scramble[0] \
                and most_unique and least_unique:
                break
        for j in range(how_many_repetitions):
            scrambled_repetition[j] += jammed_letter[j]
    return scrambled_repetition

def words_suitable(unmodified_word: str, modified_word: str) -> int:
    """Makes sure that two words are suitable to be hidden in same scramble,
    returns -1 if the words contain other characters, than alphabets, and
    -2 if the words are different length, and index if there is same letter 
    in same place in both words, as the letter can't be most common and
    uncommon at the same time. Returns -3 if there are no issues."""
    if not modified_word.isalpha() or not unmodified_word.isalpha():
        return -1
    if len(modified_word) != len(unmodified_word):
        return -2
    for i in range(len(unmodified_word)):
        if modified_word[i] == unmodified_word[i]:
            return i
    return -3
    
def file_writer(file_name: str, data: list) -> int:
    """Saves data in given file. Returns 1 if succesful.
    Returns -1 if file with that name exist, or 0 if fails to write."""
    if len(file_name.split('.')) == 1:
        file_name += '.txt'
    cur_path = os.path.dirname(__file__)
    file_path = os.path.join(cur_path, file_name)
    try:
        file = open(file_path, "r")
    except:
        try:
            file = open(file_path, "w")
        except:
            return 0
    else:
        file.close()
        return -1
    file.write( '\n'.join(data) )
    file.close()
    return 1

def main():
    suitable_words = False
    while not suitable_words:
        unmodified = input("Give word that is unmodified: ").lower()
        modified = input("Give word that is modified: ").lower()
        repetitions = input("Give the amount of repetitions: ")
        if not unmodified or not modified:
            continue
        if repetitions:
            try:
                repetitions = int(repetitions)
            except:
                print("Repetitions need to be given as numbers.")
                continue
            else:
                if repetitions < 3:
                    print("Repetitions need to be 3 or more.")
                    continue
        s = words_suitable(unmodified, modified)
        if s == -3:
            break
        elif s == -1:
            print("Word can only contain letters.")
        elif s == -2:
            print("Words are different length.")
        else:
            print("Words have same letter on same location: ")
            print(unmodified[:s], ' ', unmodified[s], ' ', unmodified[s + 1:])
            print(modified[:s], ' ', modified[s], ' ', modified[s + 1:])
    if repetitions:
        scramble = ecm_generator(unmodified, modified, repetitions)
    else:
        scramble = ecm_generator(unmodified, modified)
    file = ''
    while not file:
        file = input("File name: ")
    f = file_writer(file, scramble)
    if f == 1:
        print("Writing file successful.")
    elif f == -1:
        print("File name already in use.")
    else:
        print("File creation failed.")

if __name__ == "__main__":
    main()