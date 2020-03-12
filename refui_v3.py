# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 11:10:47 2020

@author: lavka
"""

import sys
import datetime
import sqlite3
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QSizePolicy
from PyQt5.QtWidgets import QLabel, QTextEdit, QMessageBox, QGridLayout, QGroupBox
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

class myReflections(QWidget):
    def __init__(self):
        super(myReflections, self).__init__()
        self.setGeometry(300,500,420,200)
        self.title = "My Reflections"
        
        self.initUI()
        
   
    def initUI(self):
        
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('reflections.png'))
        
        self.layout = QVBoxLayout()
        #self.layout.addStretch(1)
        self.setLayout(self.layout)

        
        self.txt = QTextEdit()
        self.layout.addWidget(self.txt)
        self.txt.setFixedSize(400,100) 
        self.txt.wordWrapMode
        
        self.lbl = QLabel(self)
        self.layout.addWidget(self.lbl)
        self.lbl.setText("Char: ")
        self.lbl.setFixedSize(100,10)
        
        self.hbox = QHBoxLayout()
        #self.hbox.addWidget(QLabel(""))
        self.enterbtn = QPushButton('Enter')
        self.enterbtn.setFixedSize(70,20)
        self.hbox.addWidget(self.enterbtn)
        self.enterbtn.animateClick()
        self.layout.addLayout(self.hbox)
        
        self.downbtn = QPushButton('v')
        self.layout.addWidget(self.downbtn)
        self.downbtn.resize(10,10)
        self.downbtn.setFixedHeight(30)
        self.downbtn.setFixedWidth(30)
        self.downbtn.animateClick()
        self.downbtn.minimumSize()
        
        self.txt20 = QTextEdit()   
        self.txt20.setReadOnly(True)
        
        self.txt.textChanged.connect(self.text_count)
        self.enterbtn.clicked.connect(self.enter_works)
        self.downbtn.clicked.connect(self.show20)
        
        
        self.show()
    
        
    def text_count(self):
        wordcount = len(self.txt.toPlainText())
        if wordcount <= 200:
            self.lbl.setText("Chars: " + str(wordcount))
        else:
            self.txt.setPlainText(self.txt.toPlainText()[0:200])
            self.txt.moveCursor(QTextCursor.End)
            QMessageBox.information(self, 'Warning', 'Warning: no more than 200 characters',QMessageBox.Ok)
            
    def enter_works(self):
         reflections = self.txt.toPlainText()
         datestamp = str(datetime.datetime.now())
         if len(reflections) > 0:
             conn = sqlite3.connect("myreflections.db")
             c = conn.cursor()
             c.execute("INSERT into reflections (datestamp, reflection) VALUES (?,?)", (datestamp,reflections))
             conn.commit()
             c.close()
             conn.close()
             self.txt.setPlainText("")
             self.show20()
             
    def show20(self):
        if self.downbtn.text() == 'v':
            self.downbtn.setText('^')
            self.setFixedSize(420,500)
            conn = sqlite3.connect("myreflections.db")
            c = conn.cursor()
            c.execute("SELECT datestamp, reflection FROM reflections")
            data = c.fetchall()
            self.layout.addWidget(self.txt20)
            for row in data:
                self.txt20.setText(self.txt20.toPlainText() + str(row) + '\n')
                
        elif self.downbtn.text() == '^':
            self.txt20.setParent(None)
            #self.resize(500,300)
            self.setFixedSize(420,300)
            self.downbtn.setText('v')
            
    
        
        
if __name__=='__main__':
    app = QApplication(sys.argv)
    myThings = myReflections()
    sys.exit(app.exec_())