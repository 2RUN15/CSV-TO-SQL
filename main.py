import sys , json
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import * # UI'yi import ettik
from frontend import Ui_MainWindow
import dialogs, button_action
from convert import convert
from logla import log_al
from behaviour import create_table
import threading

log = log_al("logla")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dialog = QWidget()

        #None Value
        self.localtext = ""
        self.csv_path = ""
        self.databasetext = ""
        self.usernametext = ""
        self.dbpasswordtext = ""
        self.tablenametext = ""
        self.tableindex = 0
        self.dbindex = 0
        
        #Dialogs
        self.filechos = dialogs.file_chos(self.dialog)
        self.csvchos = dialogs.json_chos(self.dialog)
        self.table_success = dialogs.table_success(self)

        #MessageBoxx
        self.warning_msg = dialogs.warning_run()
    
        #Button Actions Class
        self.save_csv = button_action.save_csv(self)
        self.chos_jsv = button_action.chos_jsv(self,self.ui)

        #Button Actions
        self.ui.file_push_2.clicked.connect(self.file_chos)
        self.ui.json_save.clicked.connect(self.save_csv.exec)
        self.ui.json_chose.clicked.connect(self.chos_jsv.exec)
        self.ui.run_buton.clicked.connect(self.run_button)

        #Line Actions
        self.ui.localhost.textChanged.connect(self.localhost_changed)
        self.ui.databasedb.textChanged.connect(self.databasedb_changed)
        self.ui.user_name.textChanged.connect(self.user_name_changed)
        self.ui.db_password.textChanged.connect(self.db_password_changed)
        self.ui.table_name.textChanged.connect(self.table_name_changed)

        #Check Box
        self.ui.crt_table.stateChanged.connect(self.table_index_changed)
        self.ui.crt_db.stateChanged.connect(self.db_index_changed)

        #QInstall
        qInstallMessageHandler(self.qt_messsage_handler)

    def run_button(self):
        self.ui.log_text.clear()
        self.threads = QThread()
        try:
            log.debug("Çalıştır butonuna basıldı")
            if self.csv_path and self.localtext and self.databasetext and self.usernametext and self.dbpasswordtext and self.tablenametext:
                self.result = convert(self.csv_path)
                self.result.exec()
                self.worker = create_table(self.tablenametext,self.result.df,self.chos_jsv.csv_path,self.tableindex,self.ui)
                self.worker.moveToThread(self.threads)

                self.threads.started.connect(self.worker.exec)
                self.worker.finished.connect(self.finished)

                self.worker.finished.connect(self.threads.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.threads.finished.connect(self.threads.deleteLater)

                self.threads.start()

                self.ui.run_buton.setEnabled(False)

            else:
                log.debug("Kullanıcı değerleri girmeden çalıştır butonuna bastı")
                self.warning_msg.exec()
        except Exception as e:
            log.error(f"run_buton: {e}",exc_info=True)

    def finished(self, code):
        if code == 1:
            self.table_success.exec()
            self.ui.run_buton.setEnabled(True)

    def file_chos(self):
        try:
            self.csv_path = self.filechos.exec()
            self.ui.file_line_2.setText(self.csv_path)
            log.debug(f"Bir dosya seçildi --> {self.csv_path}")
        except Exception as e:
            log.error(f"file_chos: {e}",exc_info=True)

    def localhost_changed(self, localtext):
        self.localtext = localtext
    
    def databasedb_changed(self, databasedbtext):
        self.databasetext = databasedbtext
    
    def user_name_changed(self, usernametext):
        self.usernametext = usernametext
    
    def db_password_changed(self, dbpasswordtext):
        self.dbpasswordtext = dbpasswordtext
    
    def table_name_changed(self, tablenametext):
        self.tablenametext = tablenametext
    
    def table_index_changed(self, i):
        self.tableindex = i
    
    def db_index_changed(self, i):
        self.dbindex = i
    
    def closeEvent(self, a0):
        log.debug("Programdan çıkış yapıldı\n")
        return super().closeEvent(a0)
    
    def qt_messsage_handler(self, mode, context, message):
        pass
if __name__ == "__main__":
    with open("style.css","r") as c:
        style = c.read()
    log.debug("Program başlatıldı")
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet(style)
    window.show()
    sys.exit(app.exec())