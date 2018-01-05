from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic
import sys
import os

form_class, qtbase = uic.loadUiType("gui.ui")

class MainGUI(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # TODO: load these defaults from configuration
        
        self.last_valid_users = "users.pin"
        self.last_valid_quotes = "quotes.txt"
        
        self.editUserFile.setText(self.last_valid_users)
        if not os.path.isfile(self.last_valid_users):
            open(self.last_valid_users,"w").close()
        self.editQuotesFile.setText(self.last_valid_quotes)
        if not os.path.isfile(self.last_valid_quotes):
            open(self.last_valid_quotes,"w").close()

    def pickUsersFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,
            "Choose Users file (if already existant, will not actually overwrite)", self.editUserFile.text(),"All Files (*)", options=options)
        if fileName:
            if not os.path.isfile(fileName):
                open(fileName,"w").close()
            self.editUserFile.setText(fileName)
            self.setUsersFileFinish()
    def pickQuotesFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,
            "Choose Quotes file (if already existant, will not actually overwrite)", self.editQuotesFile.text(),"All Files (*)", options=options)
        if fileName:
            if not os.path.isfile(fileName):
                open(fileName,"w").close()
            self.editQuotesFile.setText(fileName)
            self.setQuotesFileFinish()
    def saveOldFormat(self):
        print(self)
        pass # show picker and change things
    def loadOldFormat(self):
        print(self)
        pass # show picker and change things
        
    def setUsersFileFinish(self):
        print(self.editUserFile.text())
        # validate
        if os.path.isfile(self.editUserFile.text()):
            self.last_valid_users = self.editUserFile.text()
        else:
            self.editUserFile.setText(self.last_valid_users)
            self.setUsersFileFinish()
    def setQuotesFileFinish(self):
        print(self.editQuotesFile.text())
        # validate
        if os.path.isfile(self.editQuotesFile.text()):
            self.last_valid_quotes = self.editQuotesFile.text()
        else:
            self.editQuotesFile.setText(self.last_valid_quotes)
            self.setQuotesFileFinish()

def run():
    app = QApplication(sys.argv)

    #print(form_class,qtbase)

    myWindow = MainGUI(None)
    myWindow.show()
    app.exec_()
if __name__=="__main__":
    run()