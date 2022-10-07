import sys
from PyQt5.QtWidgets import (QMainWindow, QLabel, QLineEdit, QPushButton ,\
    QTextEdit, QApplication, QMessageBox ,QDialog ,QHBoxLayout, QVBoxLayout,\
    QFileDialog ,QFontDialog ,QWidget ,QAction,QInputDialog)
from PyQt5.QtGui import QTextCursor
from codecs import open as fopen
from random import randint
class Text(QTextEdit):
    def __init__(self,parent,filename="Unititled"):
        super().__init__(parent)
        self.newfile = True
        self.filename = filename
        self.changed = False
        self.edit = parent
        self.edit.setWindowTitle(self.filename)
        self.label = self.edit.statusBar()
        self.showpos()
        self.setFocus()
        self.cursorPositionChanged.connect(self.showpos)
        self.textChanged.connect(self.setchanged)

    def open(self,filename):
        try:
            f = fopen(filename,"r","utf-8",buffering=True)
            text = f.read()
        except:
            QMessageBox.warning(self,'消息','打开文件错误',\
                                QMessageBox.Ok,QMessageBox.Ok)
            return
        with f:
            self.setText(text)
            self.filename = filename
            self.newfile = False
            self.changed = False
            self.edit.setWindowTitle(self.filename)

    def save(self,filename):
        with fopen(filename,"w","utf-8",buffering=True) as f:
            f.write(self.toPlainText())
        self.newfile = False
        self.changed = False
        self.filename = filename
        self.edit.setWindowTitle(self.filename)

    def setchanged(self,*args,**kwargs):
        if not self.changed:
            self.changed = True
            self.edit.setWindowTitle("*"+self.filename+"*")

    def showpos(self,*args,**kwargs):
        tc = self.textCursor()
        self.label.showMessage("Row:{},Col:{}".format(tc.blockNumber()+1,\
                                                   tc.columnNumber()))

class FindandReplace(QDialog):
    def __init__(self,parent,te):
        super().__init__(parent)
        self.master = parent
        self.textEdit = te
        self.initUI()
    
    def initUI(self):
        vb1 = QVBoxLayout()
        
        vb1.addWidget(QLabel("查找："))
        self.findEdit = QLineEdit()
        vb1.addWidget(self.findEdit)
        
        vb1.addWidget(QLabel("替换："))
        self.replaceEdit = QLineEdit()
        vb1.addWidget(self.replaceEdit)
        
        vb2 = QVBoxLayout()
        
        bt1 = QPushButton("查找")
        bt1.clicked.connect(self.find)
        vb2.addWidget(bt1)
        
        bt2 = QPushButton("替换")
        bt2.clicked.connect(self.replace)
        vb2.addWidget(bt2)
        
        bt3 = QPushButton("替换全部")
        bt3.clicked.connect(self.replaceall)
        vb2.addWidget(bt3)

        bt4 = QPushButton("关闭")
        bt4.clicked.connect(self.close)
        vb2.addWidget(bt4)

        hb = QHBoxLayout()
        hb.addLayout(vb1)
        hb.addLayout(vb2)

        self.setLayout(hb)

        self.setWindowTitle("查找与替换")
        self.move(self.master.x(),self.master.y())
        self.show()

    def returnfocus(self):
        self.clearFocus()
        self.master.activateWindow()
        self.textEdit.setFocus()

    def find(self,*args,**kwargs):
        tc = self.textEdit.textCursor()
        text = self.textEdit.toPlainText()
        find_str = self.findEdit.text()
        start = tc.position()
        index = text.find(find_str,start)
        if index == -1:
            index = text.find(find_str,0)
            if index == -1:
                QMessageBox.warning(self,'消息','找不到该字符串',\
                                QMessageBox.Ok,QMessageBox.Ok)
                return
        tc.setPosition(index,QTextCursor.MoveAnchor)
        tc.setPosition(index+len(find_str),QTextCursor.KeepAnchor)
        self.textEdit.setTextCursor(tc)
        self.returnfocus()

    def replace(self,*args,**kwargs):
        tc = self.textEdit.textCursor()
        if tc.hasSelection():
            tc.deleteChar()
            tc.insertText(self.replaceEdit.text())
            self.returnfocus()
        else:
            QMessageBox.warning(self,'消息','无选中',\
                                QMessageBox.Ok,QMessageBox.Ok)
            
    def replaceall(self,*args,**kwargs):
        self.textEdit.setText(self.textEdit.toPlainText().replace(\
            self.findEdit.text(),self.replaceEdit.text()))
        self.returnfocus()

class Edit(QMainWindow):
    def __init__(self,parent):
        super().__init__(parent)
        self.manager = parent
        self.manager.Edits.append(self)
        self.initUI()
    def initUI(self):
        self.textEdit = Text(self)
        self.setCentralWidget(self.textEdit)
        menubar = self.menuBar()

        filemenu = menubar.addMenu('&File')
        
        ac1 = QAction("新建(Ctrl+N)",self)
        ac1.setShortcut("Ctrl+N")
        ac1.triggered.connect(self.newedit)
        filemenu.addAction(ac1)

        ac2 = QAction("打开(Ctrl+O)",self)
        ac2.setShortcut("Ctrl+O")
        ac2.triggered.connect(self.openfile)
        filemenu.addAction(ac2)

        ac3 = QAction("保存(Ctrl+S)",self)
        ac3.setShortcut("Ctrl+S")
        ac3.triggered.connect(self.savefile)
        filemenu.addAction(ac3)

        ac4 = QAction("另存为(Ctrl+Shift+S)",self)
        ac4.setShortcut("Ctrl+Shift+S")
        ac4.triggered.connect(self.saveotherfile)
        filemenu.addAction(ac4)

        editmenu = menubar.addMenu("&Edit")

        ac5 = QAction("查找与替换(Ctrl+R)",self)
        ac5.setShortcut("Ctrl+R")
        ac5.triggered.connect(self.findandreplace)
        editmenu.addAction(ac5)
        '''
        ac_line = QAction("转至某行(Ctrl+L)",self)
        ac_line.setShortCut("Ctrl+L")
        ac_line.triggered.connect(self.gotoline)
        editmenu.addAction(ac_line)
        '''

        fontmenu = menubar.addMenu("&Font")

        ac6 = QAction("设置字体(Ctrl+F)",self)
        ac6.setShortcut("Ctrl+F")
        ac6.triggered.connect(self.changefont)
        fontmenu.addAction(ac6)

        self.setGeometry(randint(100,400),randint(100,400),500,600)
        self.show()

    def newedit(self,*args,**kwargs):
        self.newedit = Edit(self.manager)

    def openfile(self,*args,**kwargs):
        filename,tp = QFileDialog.getOpenFileName(self,"打开文件",\
            "C:/Users/Administrator/Documents","文本文件(*.txt);;全部文件(*)")
        if not filename:
            return
        self.textEdit.open(filename)

    def savefile(self,*args,**kwargs):
        if self.textEdit.newfile:
            filename,tp = QFileDialog.getSaveFileName(self,"保存文件",\
            "C:/Users/Administrator/Documents","文本文件(*.txt);;全部文件(*)")
            if not filename:
                return
            if "." not in filename:
                filename += ".txt"
        else:
            filename = self.textEdit.filename
        self.textEdit.save(filename)

    def saveotherfile(self,*args,**kwargs):
        filename,tp = QFileDialog.getSaveFileName(self,"另存为",\
            "C:/Users/Administrator/Documents","文本文件(*.txt);;全部文件(*)")
        if not filename:
            return
        if "." not in filename:
            filename += ".txt"
        self.textEdit.save(filename)

    def findandreplace(self,*args,**kwargs):
        self.dialog = FindandReplace(self,self.textEdit)

    def changefont(self,*args,**kwargs):
        font,ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setCurrentFont(font)

    def gotoline(self):
        line_no,ok = QInputDialog.getInt(self,"转至某行","请输入行号:")
        if ok:
            tc = self.textEdit.textCursor()
            

    def closeEvent(self,event):
        if self.textEdit.changed:
            result = QMessageBox.question(self,"提示","是否保存文件并退出",\
                    QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel,\
                    QMessageBox.Cancel)
        else:
            result = QMessageBox.No
        if result == QMessageBox.Cancel:
            event.ignore()
            return
        if result == QMessageBox.Yes:
            self.savefile()
        self.manager.Edits.remove(self)
        event.accept()
        if len(self.manager.Edits) == 0:
            self.manager.close()


    
        
