#-*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLayout, QGridLayout, QLabel
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QToolButton

#from word import Word

class MarketGame(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        #self.word = Word('words.txt')  # 컴퓨터가 외칠 단어의 데이터베이스


        # 좌측 레이아웃 1
        difficultyLayout = QGridLayout()
        # 난이도 버튼
        difficulties = ['Easy', 'Normal', 'Hard']
        i = 0
        for difficulty in difficulties:
            self.difficultyButton = QToolButton()
            self.difficultyButton.setText(difficulty)
            # self.difficultyButton.clicked.connect(self.difficultyClicked)
            difficultyLayout.addWidget(self.difficultyButton, 0, i)
            i += 1

        # 좌측 레이아웃 2
        settingLayout = QGridLayout()
        # 난이도 안내 문구
        self.difficultyLabel = QLabel('--Easy mode--')
        self.difficultyLabel.setAlignment(Qt.AlignCenter)
        settingLayout.addWidget(self.difficultyLabel, 0, 0)
        # 게임 시작 버튼
        self.gamestartButton = QToolButton()
        self.gamestartButton.setText('Game Start')
        # self.gamestartButton.clicked.connect(self.startGame)
        settingLayout.addWidget(self.gamestartButton, 1, 0)
        # 안내 문구
        self.guideLabel = QLabel('----')
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

        # 우측 레이아웃 2
        inputLayout = QGridLayout()
        # 입력 창
        self.stringInput = QLineEdit()
        inputLayout.addWidget(self.stringInput, 0, 0)
        # 엔터 버튼
        self.enterButton = QToolButton()
        self.enterButton.setText('Enter')
        # self.enterButton.clicked.connect(self.enterClicked)
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

        # 게임 시작
        self.startGame()


    def startGame(self):
        pass

    def difficultyClicked(self):
        pass


if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    game = MarketGame()
    game.show()
    sys.exit(app.exec_())