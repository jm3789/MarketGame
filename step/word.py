import random

class Word:

    def __init__(self, filename):
        self.words = []  # words.txt 의 내용을 리스트 words 에 저장
        f = open(filename, 'r')
        lines = f.readlines()
        f.close()

        self.count = 0
        for line in lines:
            word = line.rstrip()
            self.words.append(word)
            self.count += 1

        print('%d words in DB' % self.count)

    # 난이도에 따른 단어 선택
    def randFromDB(self, d):
        if d == 'Easy':
            r = random.randrange(41, 80)
            return self.words[r]
        elif d == 'Normal':
            r = random.randrange(41, 160)
            return self.words[r]
        else:
            q = random.randrange(1, 40)
            r = random.randrange(41, 160)
            return self.words[q] + ' ' + self.words[r]

    # 난이도에 따른 컴퓨터가 기억할 수 있는 단어의 개수
    def randFromMem(self, d):
        if d == 'Easy':
            m = random.randrange(3, 7)
            return m
        elif d == 'Normal':
            m = random.randrange(5, 9)
            return m
        else:
            m = random.randrange(7, 11)
            return m

