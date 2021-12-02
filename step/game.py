#-*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout, QLabel
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton

from judge import Judge
from screen import Screen
from word import Word
import random


class MarketGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.word = Word('words.txt')  # 컴퓨터가 외칠 단어의 데이터베이스
        self.difficulty = '' # 난이도 초기화
        self.timer = QTimer()  # 타이머 지정
        self.gameOver = True

        # 좌측 레이아웃 1
        difficultyLayout = QGridLayout()
        # 난이도 버튼
        difficulties = ['Easy', 'Normal', 'Hard']
        i = 0
        for d in difficulties:
            self.difficultyButton = QToolButton()
            self.difficultyButton.setText(d)
            self.difficultyButton.clicked.connect(self.difficultyClicked)
            difficultyLayout.addWidget(self.difficultyButton, 0, i)
            i += 1

        # 좌측 레이아웃 2
        settingLayout = QGridLayout()
        # 난이도 안내 문구
        self.difficultyLabel = QLabel('--Choose mode--')
        self.difficultyLabel.setAlignment(Qt.AlignCenter)
        settingLayout.addWidget(self.difficultyLabel, 0, 0)
        # 게임 시작 버튼
        self.gamestartButton = QToolButton()
        self.gamestartButton.setText('Game Start')
        self.gamestartButton.clicked.connect(self.startGame)
        settingLayout.addWidget(self.gamestartButton, 1, 0)
        # 안내 문구
        self.guideLabel = QLabel('Never mind ' + 'the last \' \'!')
        self.guideLabel.setAlignment(Qt.AlignRight)
        settingLayout.addWidget(self.guideLabel, 2, 0)

        # 좌측 레이아웃 완성
        leftLayout = QGridLayout()
        leftLayout.addLayout(difficultyLayout, 0, 0)
        leftLayout.addLayout(settingLayout, 1, 0)


        # 우측 레이아웃 1
        screenLayout = QGridLayout()
        # 게임 화면
        self.gameWindow = QTextEdit()
        self.gameWindow.setReadOnly(True)
        self.gameWindow.setAlignment(Qt.AlignCenter)
        screenLayout.addWidget(self.gameWindow, 0, 0)
        # 플레이어가 외치는 문장
        self.shoutLabel = QLabel('')
        self.shoutLabel.setAlignment(Qt.AlignRight)
        screenLayout.addWidget(self.shoutLabel, 1, 0)

        # 우측 레이아웃 2
        inputLayout = QGridLayout()
        # 입력 창
        self.stringInput = QLineEdit()
        inputLayout.addWidget(self.stringInput, 0, 0)
        # 엔터 버튼
        self.enterButton = QToolButton()
        self.enterButton.setText('Enter')
        self.enterButton.clicked.connect(self.enterClicked)
        inputLayout.addWidget(self.enterButton, 0, 1)

        # 우측 레이아웃 완성
        rightLayout = QGridLayout()
        rightLayout.addLayout(screenLayout, 0, 0)
        rightLayout.addLayout(inputLayout, 1, 0)


        # 메인 레이아웃 완성
        mainLayout = QGridLayout()
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(leftLayout, 0, 0)
        mainLayout.addLayout(rightLayout, 0, 1)

        self.setLayout(mainLayout)

        self.setWindowTitle('시장에 가면')

    def difficultyClicked(self):
        # 클릭된 버튼의 텍스트를 확인하여 난이도 설정: 게임이 진행 중이지 않을 때에만
        if self.gameOver == True:
            btn = self.sender()
            self.difficulty = btn.text()
            self.difficultyLabel.setText('--%s mode--' % self.difficulty)
        else:
            self.guideLabel.setText('You can\'t change difficulty now.')
            return 'You can\'t change difficulty now.'





    def startGame(self):

        # 난이도를 설정하지 않은 채 시작 버튼을 눌렀을 때
        if self.difficulty == '':
            self.guideLabel.setText('Choose mode!')
            return 'Choose mode!'

        # 플래그, 타이머 초기화
        self.myTurn = False
        self.newWord = False
        self.gameOver = False
        self.timer.start(0)
        self.guideLabel.clear()

        # 이번 게임에서 컴퓨터가 기억할 수 있는 단어 수
        self.limit = self.word.randFromMem(self.difficulty)

        # 컴퓨터부터 시작
        self.order = 0
        self.makeTurn()
        ranWord = self.word.randFromDB(self.difficulty)
        self.computer(ranWord)
        self.judge = Judge()
        self.judge.nowAppend(ranWord)
        self.makeTurn()
        self.myTurn = True

    # 컴퓨터 율동
    def computerMove(self):
        self.gameWindow.setPlaceholderText(Screen.text[0])
        loop = QEventLoop()
        QTimer.singleShot(800, loop.quit)
        loop.exec_()
        self.gameWindow.setPlaceholderText(Screen.text[1])
        QTimer.singleShot(800, loop.quit)
        loop.exec_()

    # 새로운 턴이 시작될 때
    def makeTurn(self):
        self.shoutLabel.setText('다같이 : 시장에 가면~')
        self.computerMove()

    # 컴퓨터가 제시어를 외칠 때
    def computer(self, currentWord):
        self.shoutLabel.setText('컴퓨터 : %s도 있고~' % currentWord)
        self.computerMove()



    def enterClicked(self):

        # 플레이어의 차례가 아닐 때에는 반응하지 않음
        if self.myTurn == False:
            self.guideLabel.setText('Not your turn!')
            return 'Not your turn!'
        # 게임이 종료된 후에는 반응하지 않음
        if self.gameOver == True:
            self.guideLabel.setText('Press \'Game start\' to play again.')
            return 'Press \'Game start\' to play again.'

        # 양쪽 공백을 자른 값이 입력값이 됨
        enteredString = self.stringInput.text().strip()

        # 아무것도 입력하지 않았을 경우
        if len(enteredString) < 1:
            self.guideLabel.setText('Enter the keyword.')
            return 'Enter the keyword.'

        try:
            # 새로운 단어를 입력해야 될 때라면
            if self.newWord == True:
                self.judge.nowAppend(enteredString)
                self.newWord = False
                self.myTurn = False
                self.shoutLabel.setText('플레이어 : (마지막) %s도 있고~' % enteredString)
                self.computerMove()
                # 컴퓨터의 차례
                self.makeTurn()
                if self.judge.enterLength() <= self.limit:
                    for num in range(0, self.judge.enterLength()):
                        self.computer(self.judge.enteredStringsIndex(num))
                    ranWord = self.word.randFromDB(self.difficulty)
                    self.computer(ranWord)
                    self.judge.nowAppend(ranWord)
                    self.makeTurn()
                    self.gameWindow.setPlaceholderText(Screen.text[0])
                    self.order = 0
                    self.myTurn = True
                else:  # 컴퓨터가 기억할 수 있는 단어 수 초과: 랜덤한 시점에서 게임 오버, 플레이어 승리
                    for num in range(0, random.randrange(0, self.judge.enterLength()-1)):
                        self.computer(self.judge.enteredStringsIndex(num))
                    loop = QEventLoop()
                    QTimer.singleShot(800, loop.quit)
                    loop.exec_()
                    self.gameWindow.setPlaceholderText(Screen.text[3])
                    self.gameOver = True
                    self.guideLabel.setText('WIN!!')
                    return 'WIN!!'

            # 기존의 단어를 맞춰야 될 때라면
            else:
                result = self.judge.judge(enteredString, self.order)
                self.guideLabel.setText(result)
                # 정답
                if result == 'Correct':
                    self.shoutLabel.setText('플레이어 : %s도 있고~' % enteredString)
                    self.order += 1
                    self.computerMove()
                    if self.order == self.judge.enterLength():
                        self.newWord = True
                # 오답: 플레이어 패배, 게임 오버
                else:
                    self.gameWindow.setPlaceholderText(Screen.text[2])
                    self.gameOver = True
        except:
            self.guideLabel.setText('Error!')  # 예외 처리: 엔터 버튼을 빠르게 클릭했을 경우
            return 'Error!'



if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    game = MarketGame()
    game.show()
    sys.exit(app.exec_())