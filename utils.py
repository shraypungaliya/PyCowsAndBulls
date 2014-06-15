__author__ = 'shray'

def check_unique_letters(word):
    uniqueLetters = set()
    for letter in word:
        if letter in uniqueLetters:
            return False
        else:
            uniqueLetters.add(letter)
    return True

