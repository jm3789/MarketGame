class Judge:

    def __init__(self):
        self.enteredStrings = []
        self.order = 0

    def enteredStringsIndex(self, num):
        return self.enteredStrings[num]

    def nowAppend(self, ranWord):
        self.enteredStrings.append(ranWord)

    def enterLength(self):
        return len(self.enteredStrings)

    def judge(self, enteredString, order):
        if enteredString == self.enteredStrings[order]:
            return 'Correct'
        else:
            return 'LOSE: incorrect!'

