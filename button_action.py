from PyQt6.QtWidgets import *
import json
import dialogs
import os
from PyQt6.QtCore import QThread, pyqtSignal
from logla import log_al
from convert import convert
from package_values import behaviour_config
from behaviour import create_table

log = log_al("logla")

class save_csv:
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.csv_folder_path = dialogs.csv_chos_folder(self.parent)

    def exec(self):
        path_list = []
        file_dict = {
            "file_name": "config",
            "uzanti":".json",
            "value":1,
        }
        config_json = {
            "host": self.parent.localtext,
            "user": self.parent.usernametext,
            "password": self.parent.dbpasswordtext,
            "database": self.parent.databasetext       
        }
        self.save_csv_folder = self.csv_folder_path.exec()
        for i in os.listdir(self.save_csv_folder):
            if os.path.isfile(i) == True:
                path_list.append(i)
        while True:
            if file_dict["file_name"] + str(file_dict["value"]) + file_dict["uzanti"] in path_list:
                self.new_path = file_dict["file_name"] + str(file_dict["value"]) + file_dict["uzanti"]
                file_dict["value"]+= 1
            if self.new_path not in path_list:
                self.save_csv_folder = os.path.join(self.save_csv_folder, self.new_path)
                break

        with open (self.save_csv_folder,"w", encoding="utf-8") as f:
            json.dump(config_json,f,ensure_ascii=False, indent=4)

class chos_jsv:
    def __init__(self,parent,ui_parent):
        self.parent = parent
        self.ui = ui_parent

        self.json_error = dialogs.json_error()

    def exec(self):
        self.csv_path = self.parent.csvchos.exec()
        try:
            if self.csv_path:
                with open(self.csv_path) as f:
                    self.json_file = json.load(f)

                self.localtext = self.json_file["host"]
                self.databasetext = self.json_file["database"]
                self.usernametext = self.json_file["user"]
                self.dbpasswordtext = self.json_file["password"]

                self.ui.localhost.setText(self.localtext)
                self.ui.databasedb.setText(self.databasetext)
                self.ui.user_name.setText(self.usernametext)
                self.ui.db_password.setText(self.dbpasswordtext)
        except:
            self.json_error.exec()

class run_buton:
    def __init__(self, conf: behaviour_config):
        self.conf = conf
        self.ui = self.conf.ui

        #Dialogs
        self.table_success = dialogs.table_success(self)        

    def run_button(self):
        self.ui.log_text.clear()
        self.threads = QThread()
        try:
                self.worker = create_table(self.conf)
                self.worker.moveToThread(self.threads)

                self.threads.started.connect(self.worker.exec)
                self.worker.finished.connect(self.finished)
                self.worker.add_column_sgn.connect(lambda sgn: self.ui.log_text.append(f"{sgn} -- column eklendi"))
                self.worker.log_text_sgn.connect(lambda text: self.ui.log_text.append(text))

                self.worker.finished.connect(self.threads.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.threads.finished.connect(self.threads.deleteLater)

                self.threads.start()

                self.ui.run_buton.setEnabled(False)

        except Exception as e:
            log.error(f"run_buton: {e}",exc_info=True)
    
    def finished(self, code):
        if code == 1:
            self.table_success.exec()
            self.ui.run_buton.setEnabled(True)