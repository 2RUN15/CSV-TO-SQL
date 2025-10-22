from PyQt6.QtWidgets import *
import json
import dialogs
import os

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
