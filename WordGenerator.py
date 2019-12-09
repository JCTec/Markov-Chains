import random
import re

class WordGenerator:

    brain = ""
    chain = {}
    lastResult = ""

    secondOrder = True

    brainPath = ""

    def __init__(self, brainPath, secondOrder=True):
        self.brainPath = brainPath
        self.secondOrder = secondOrder
        self.__loadWith__(brainPath)

    def load(self, brainPath):
        self.brainPath = brainPath
        self.__loadWith__(brainPath)

    def setSecondOrder(self):
        self.secondOrder = True
        self.__loadWith__(self.brainPath)

    def setFirstOrder(self):
        self.secondOrder = False
        self.__loadWith__(self.brainPath)

    def __loadWith__(self, brainPath):
        self.brain = ""
        self.chain = {}
        self.lastResult = ""

        file_string = ""
        file_string = open(brainPath, 'r').read()

        file_string = self.__clean__(file_string)

        self.brain = file_string.split()
        self.chain['.'] = ' '

        if(self.secondOrder):
            self.__loadSecondOrder__()
        else:
            self.__loadFirstOrder__()

    def __clean__(self, file_string):
        file_string = re.sub(r'^https?:\/\/.*[\r\n]*', '', file_string, flags=re.MULTILINE)
        file_string = re.sub(r'https\S+', '', file_string)
        file_string = re.sub(r'http\S+', '', file_string)
        file_string = re.sub(r'^co/?:\/\/.*[\r\n]*', '', file_string, flags=re.MULTILINE)

        file_string = file_string.lower()
        file_string = file_string.replace("!", " ")
        file_string = file_string.replace(".", " ")
        file_string = file_string.replace(",", " ")
        file_string = file_string.replace("@", " ")
        file_string = file_string.replace("&amp;", " ")
        file_string = file_string.replace("?", " ")
        file_string = file_string.replace("-", " ")
        file_string = file_string.replace("https://t", " ")

        return file_string

    def __loadFirstOrder__(self):

        #O(n)

        for i in range(0, len(self.brain)):
            key = self.brain[i]
            if key not in self.chain:
                self.chain[key] = []
                if (i + 1 < len(self.brain)):
                    self.chain[key].append(self.brain[i + 1])
                else:
                    self.chain[key].append('.')
            else:
                # already exists in chain
                if (i + 1 < len(self.brain)):
                    self.chain[key].append(self.brain[i + 1])
                else:
                    self.chain[key].append('.')


    def __loadSecondOrder__(self):

        #O(n)

        for i in range(0, len(self.brain)):
            if (i + 1 < len(self.brain)):
                key = (self.brain[i], self.brain[i + 1])
                if key not in self.chain:
                    self.chain[key] = []
                    if (i + 2 < len(self.brain)):
                        self.chain[key].append(self.brain[i + 2])
                    else:
                        self.chain[key].append('.')
                else:
                    # already exists in chain
                    if (i + 2 < len(self.brain)):
                        self.chain[key].append(self.brain[i + 2])
                    else:
                        self.chain[key].append('.')

    def predict(self, n):
        if(self.secondOrder):

            start_word = random.choice(tuple(self.chain.keys()))
            final_word_list = []
            current_tuple = start_word

            for i in range(n):
                current_word = current_tuple
                next_word = random.choice(self.chain[current_word])
                current_tuple = (current_word[1], next_word)
                final_word_list.append(next_word)

        else:
            start_word = random.choice(list(self.chain.keys()))

            final_word_list = []
            final_word_list.append(start_word)

            for i in range(n):
                current_word = final_word_list[i]
                next_word = random.choice(self.chain[current_word])
                final_word_list.append(next_word)

        result = ""

        for word in final_word_list:
            result += str(word) + " "

        print(result)

        self.lastResult = result
