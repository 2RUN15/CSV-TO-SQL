import mysql.connector
from logindb import connectdb
from convert import convert
import numpy as np
from logla import log_al
import dialogs
from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal

log = log_al("logal")

class create_table(QObject, connectdb):
    finished = pyqtSignal(int)

    def __init__(self,table_name,column,json_path,table_index,ui):
        super().__init__()

        self.login(json_path)
        self.cursor = self.conn.cursor()
        self.ui = ui
        self.table_name = table_name
        self.column = column
        self.table_index = table_index
        self.table_list = []
        self.column_list = []
        self.liste = []

        #Dialogs
        self.table_warning = dialogs.table_warning(self.table_name, self)
        self.table_error = dialogs.table_error(self.table_name, self)
        self.table_success = dialogs.table_success(self)        

        #Values
        self.int_value = "INT"
        self.varchar = "VARCHAR(255)"
        self.float_value = "FLOAT"
        self.bool_value = "BOOL"
    
    def exec(self):
        try:
            self.cursor.execute("SHOW TABLES")
            for i in self.cursor.fetchall():
                self.liste.append(i[0])

            if self.table_index !=0:
                if self.table_name not in self.liste:
                    self.add_column()
                    self.insert_user()
            else:
                self.insert_user()
            
            self.ui.log_text.append("Veriler Eklendi")
            self.finished.emit(int(1))
        except Exception as e:
            self.finished.emit(int(0))
            log.error(f"{e}",exc_info=True)
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def add_column(self):
        log.debug("add_column")
        self.cursor.execute(f"""
CREATE TABLE {self.table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY
)
""")
        try:
            for i in self.column.columns:
                self.ui.log_text.append(f"{i} -- column eklendi")
                self.column_type = type(self.column[i].iloc[0])
                if self.column_type == np.int64:
                    self.cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {i} {self.int_value}")
                elif self.column_type == str:
                    self.cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {i} {self.varchar}")
                elif self.column_type == np.float64:
                    self.cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {i} {self.float_value}")
                elif self.column_type == np.bool:
                    self.cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {i} {self.bool_value}")
        except Exception as e:
            self.ui.log_text.append("HATA (Detaylar için log.log dosyasını kontrol et)")
            log.error(f"add_column_function: {e}",exc_info=True)
    
    def insert_user(self):
        log.debug("insert_user")
        try:
            birlestir = ", ".join(self.column.columns)
            column_len = len(self.column.columns)
            yer_tutucu = ", ".join(['%s'] * column_len)

            sql_insert = f"INSERT INTO {self.table_name} ({birlestir}) VALUES ({yer_tutucu}) "
            self.ui.log_text.append("Veriler Ekleniyor...")
            for _,row in self.column.iterrows():
                values = tuple(row)
                self.cursor.execute(sql_insert,values)
        except Exception as e:
            log.error(f"insert_user: {e}",exc_info=True)
