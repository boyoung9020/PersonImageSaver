from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import QIcon

class Ui_crawling(object):
    def setupUi(self, crawling):
        
        defalutImage= 'icon/고라파덕.gif'
        icon = QIcon('icon/icon.png')
        
        crawling.setObjectName("crawling")
        crawling.setEnabled(True)
        crawling.resize(379, 566)
        
        crawling.setWindowIcon(icon)
      
        self.namelist = QtWidgets.QListWidget(crawling) 
        self.namelist.setGeometry(QtCore.QRect(20, 10, 101, 171))
        self.namelist.setObjectName("namelist")
        self.namelist.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.addButton = QtWidgets.QPushButton(crawling)
        self.addButton.setGeometry(QtCore.QRect(210, 19, 75, 23))
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.addTextAndScroll)
        self.deleteButton = QtWidgets.QPushButton(crawling)
        self.deleteButton.setGeometry(QtCore.QRect(130, 50, 75, 23))
        self.deleteButton.setObjectName("deleteButton")
        self.crawlingButton = QtWidgets.QPushButton(crawling)
        self.crawlingButton.setGeometry(QtCore.QRect(130, 150, 75, 23))
        self.crawlingButton.setObjectName("crawlingButton")
        self.loglist = QtWidgets.QListWidget(crawling)  
        self.loglist.setGeometry(QtCore.QRect(20, 220, 341, 171))
        self.loglist.setObjectName("loglist") 
        self.detected_image_label = QtWidgets.QLabel(crawling)
        self.detected_image_label.setGeometry(QtCore.QRect(120, 420, 141, 131))
        self.detected_image_label.setFrameShape(QtWidgets.QFrame.Panel)
        self.detected_image_label.setObjectName("detected_image_label")

        self.movie = QMovie(defalutImage)
        self.detected_image_label.setMovie(self.movie)
        self.movie.start()

        self.resetButton = QtWidgets.QPushButton(crawling)
        self.resetButton.setGeometry(QtCore.QRect(280, 470, 75, 23))
        self.resetButton.setObjectName("resetButton")

        self.ScheckBox = QtWidgets.QCheckBox(crawling)
        self.ScheckBox.setGeometry(QtCore.QRect(270, 110, 130, 16))
        font = QtGui.QFont()
        font.setFamily("한컴 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.ScheckBox.setFont(font)
        self.ScheckBox.setAutoRepeat(False)
        self.ScheckBox.setAutoExclusive(False)
        self.ScheckBox.setObjectName("ScheckBox")
        self.GcheckBox = QtWidgets.QCheckBox(crawling)
        self.GcheckBox.setGeometry(QtCore.QRect(270, 130, 130, 16))
        font = QtGui.QFont()
        font.setFamily("한컴 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.GcheckBox.setFont(font)
        self.GcheckBox.setObjectName("GcheckBox")
        
        self.cautionlabel = QtWidgets.QLabel(crawling)
        self.cautionlabel.setGeometry(QtCore.QRect(245, 150, 130, 32)) 
        self.cautionlabel.setObjectName("cautionlabel")
        self.cautionlabel.setWordWrap(True)
        self.cautionlabel.setAlignment(Qt.AlignCenter) 
        self.cautionlabel.setStyleSheet("color: red;")
        self.cautionlabel.setFont(font)
        self.cautionlabel.setVisible(False)
        
        self.buttonGroup = QtWidgets.QButtonGroup(crawling)
        self.buttonGroup.addButton(self.ScheckBox)
        self.buttonGroup.addButton(self.GcheckBox)

        self.buttonGroup.buttonClicked.connect(self.checkBoxClicked)

        self.progressBar = QtWidgets.QProgressBar(crawling)
        self.progressBar.setGeometry(QtCore.QRect(20, 190, 341, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setStyleSheet("""
        QProgressBar {
            border: 2px solid grey;
            border-radius: 5px;
            background-color: white;
        }

        QProgressBar::chunk {
            background-color: #FFD700; 
        }
        """)


        self.label = QtWidgets.QLabel(crawling)
        self.label.setGeometry(QtCore.QRect(130, 90, 200, 16))
        self.label.setObjectName("label")
        self.nameEdit = QtWidgets.QLineEdit(crawling)
        self.nameEdit.setGeometry(QtCore.QRect(130, 20, 81, 21))
        self.nameEdit.setObjectName("nameEdit")
        self.imagenumEdit = QtWidgets.QLineEdit(crawling)
        self.imagenumEdit.setGeometry(QtCore.QRect(130, 110, 51, 21))
        self.imagenumEdit.setObjectName("imagenumEdit")
        self.imagenumEdit.setText("20")  
        self.label_2 = QtWidgets.QLabel(crawling)
        self.label_2.setGeometry(QtCore.QRect(150, 400, 150, 16))
        font = QtGui.QFont()
        font.setFamily("한컴 고딕")
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.deleteallButton = QtWidgets.QPushButton(crawling)
        self.deleteallButton.setGeometry(QtCore.QRect(210, 50, 75, 23))
        self.deleteallButton.setObjectName("deleteallButton")

        self.retranslateUi(crawling)
        QtCore.QMetaObject.connectSlotsByName(crawling)

    def retranslateUi(self, crawling):
        version = 'v1.0'
        _translate = QtCore.QCoreApplication.translate
        crawling.setWindowTitle(_translate("crawling", f"Person Image Crawling {version}"))
        self.addButton.setText(_translate("crawling", "추가"))
        self.deleteButton.setText(_translate("crawling", "삭제"))
        self.resetButton.setText(_translate("crawling", "종료"))
        self.crawlingButton.setText(_translate("crawling", "실행"))
        self.label.setText(_translate("crawling", "저장할 이미지 갯수"))
        self.label_2.setText(_translate("crawling", "선택된 대표 얼굴"))
        self.cautionlabel.setText(_translate("crawling", "⚠️ googleCSE는 10개이하만 가능"))
        self.deleteallButton.setText(_translate("crawling", "전체 삭제"))
        self.ScheckBox.setText(_translate("crawling", "Selenium"))
        self.GcheckBox.setText(_translate("crawling", "googleCSE"))
        
    def checkBoxClicked(self, checkBox):
        if checkBox == self.ScheckBox:
            print('Selenium 선택됨')
            self.GcheckBox.setChecked(False)
            self.cautionlabel.setVisible(False)

        elif checkBox == self.GcheckBox:
            print('GoogleCSE 선택됨')
            self.cautionlabel.setVisible(False)

            if int(self.imagenumEdit.text()) <= 10:
                self.GcheckBox.setChecked(True)
                self.cautionlabel.setVisible(False)
  
            else:
                self.GcheckBox.setChecked(False)
                self.ScheckBox.setChecked(True)
                self.cautionlabel.setVisible(True)

    def addTextAndScroll(self):
        text = self.nameEdit.text()
        self.namelist.addItem(text)
        self.nameEdit.clear()
        self.namelist.scrollToBottom()
