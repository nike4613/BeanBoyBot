from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5 import uic
import sys
import os
import quotes
import configparser
import threading as threads
import util

form_class, qtbase = uic.loadUiType("gui.ui")

config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),"cfg.ini")
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())

class GuiClosed(Exception):
    pass

class MainGUI(QMainWindow, form_class):
    def __init__(self, bot):
        QMainWindow.__init__(self, None)
        self.setupUi(self)
        
        self.timed = QTimer(self, timeout=self.clear_status)
        
        self.bot = bot
        
        self.load_cfg()
        
        self.editUserFile.setText(self.last_valid_users)
        if not os.path.isfile(self.last_valid_users):
            open(self.last_valid_users,"w").close()
        else:
            self.forceLoadUsers()
        self.editQuotesFile.setText(self.last_valid_quotes)
        if not os.path.isfile(self.last_valid_quotes):
            open(self.last_valid_quotes,"w").close()
        else:
            self.forceLoadQuotes()

    def clear_status(self):
        self.statusBar.showMessage("")
            
    def show_status(self, stat):
        self.statusBar.showMessage(stat)
        self.timed.start(2000)
            
    def pickUsersFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
            "Choose Users file", self.editUserFile.text(),"All Files (*)", options=options)
        if fileName:
            if not os.path.isfile(fileName):
                open(fileName,"w").close()
            self.editUserFile.setText(fileName)
            self.setUsersFileFinish()
    def pickQuotesFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
            "Choose Quotes file", self.editQuotesFile.text(),"All Files (*)", options=options)
        if fileName:
            if not os.path.isfile(fileName):
                open(fileName,"w").close()
            self.editQuotesFile.setText(fileName)
            self.setQuotesFileFinish()
            
    def saveOldFormat(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,
            "Save old users", "","All Files (*)", options=options)
        if fileName:
            self.bot.player_handler.save_to_java_format(fileName)
            self.show_status("Users saved (Java)")
    def loadOldFormat(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,
            "Load old users", "","All Files (*)", options=options)
        if fileName:
            self.bot.player_handler.load_from_java_format(fileName)
            self.show_status("Users loaded (Java)")
            
    def forceSaveUsers(self):
        self.bot.player_handler.save_to_file(self.last_valid_users)
        self.show_status("Users saved")
    def forceLoadUsers(self):
        self.bot.player_handler.load_from_file(self.last_valid_users)
        self.show_status("Users loaded")
    def forceSaveQuotes(self):
        quotes.save(self.last_valid_quotes)
        self.show_status("Quotes saved")
    def forceLoadQuotes(self):
        quotes.load(self.last_valid_quotes)
        self.show_status("Quotes loaded")
        
    def setUsersFileFinish(self):
        # validate
        if os.path.isfile(self.editUserFile.text()):
            self.last_valid_users = self.editUserFile.text()
            self.show_status("Users file set to " + self.last_valid_users)
        else:
            self.editUserFile.setText(self.last_valid_users)
            self.setUsersFileFinish()
    def setQuotesFileFinish(self):
        # validate
        if os.path.isfile(self.editQuotesFile.text()):
            self.last_valid_quotes = self.editQuotesFile.text()
            self.show_status("Quotes file set to " + self.last_valid_quotes)
        else:
            self.editQuotesFile.setText(self.last_valid_quotes)
            self.setQuotesFileFinish()

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to close the program?"
        reply = QMessageBox.question(self, 'Closing...', 
                         quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.forceSaveQuotes()
            self.forceSaveUsers()
            self.save_cfg()
            util.async_raise(threads.main_thread(), GuiClosed)
            event.accept()
        else:
            event.ignore()

    def save_cfg(self):
        config.clear()
        config['files'] = {}
        user = os.path.abspath(self.last_valid_users)
        quote = os.path.abspath(self.last_valid_quotes)
        common = os.path.commonpath([user,quote])
        config['files']['base dir'] = common
        config['files']['users'] = user.replace(common,'${files:base dir}')
        config['files']['quotes'] = quote.replace(common,'${files:base dir}')
        
        
        
        with open(config_file, 'w') as configfile:
            config.write(configfile)
            
    def load_cfg(self):
        config.clear()
        if os.path.isfile(config_file):
            config.read(config_file)
        
        self.last_valid_users = config.get('files','users',fallback=os.path.abspath("users.pin"))
        self.last_valid_quotes = config.get('files','quotes',fallback=os.path.abspath("quotes.txt"))
        
def start_gui(bot):
    evt = threads.Event()
    thr = threads.Thread(target=run,args=(bot,evt),daemon=True)
    thr.start()
    evt.wait()
    return thr
        
def run(bot,evt):
    app = QApplication(sys.argv)

    #print(form_class,qtbase)

    myWindow = MainGUI(bot)
    myWindow.show()
    evt.set()
    app.exec_()
if __name__=="__main__":
    run(None)