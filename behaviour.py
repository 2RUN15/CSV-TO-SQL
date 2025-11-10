import mysql.connector
from logindb import connectdb
from convert import convert
import numpy as np
from logla import log_al
import dialogs
from PyQt6 import QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal
from package_values import behaviour_config, login_config

log = log_al("logal")

class create_table(QObject, connectdb):
    finished = pyqtSignal(int)
    add_column_sgn = pyqtSignal(str)
    log_text_sgn  = pyqtSignal(str)

    def __init__(self, config: behaviour_config):
        super().__init__()

        self.config = config
        self.login_conf = login_config(
            json_path=self.config.json_path,
            localtext=self.config.localtext,
            databasedbtext=self.config.databasedbtext,
            usernametext=self.config.usernametext,
            dbpasswordtext=self.config.dbpasswordtext
        )

        self.table_list = []
        self.column_list = []
        self.liste = []
        self.login(self.login_conf)
        self.cursor = self.conn.cursor()

        #Dialogs
        self.table_warning = dialogs.table_warning(self.config.table_name, self)
        self.table_error = dialogs.table_error(self.config.table_name, self)
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

            if self.config.table_index !=0:
                if self.config.table_name not in self.liste:
                    self.add_column()
                    self.insert_user()
            else:
                self.insert_user()
            
            self.log_text_sgn.emit(str("Veriler Eklendi"))
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
CREATE TABLE {self.config.table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY
)
""")
        try:
            for i in self.config.column.columns:
                self.add_column_sgn.emit(str(i))
                self.column_type = type(self.config.column[i].iloc[0])
                if self.column_type == np.int64:
                    self.cursor.execute(f"ALTER TABLE {self.config.table_name} ADD COLUMN {i} {self.int_value}")
                elif self.column_type == str:
                    self.cursor.execute(f"ALTER TABLE {self.config.table_name} ADD COLUMN {i} {self.varchar}")
                elif self.column_type == np.float64:
                    self.cursor.execute(f"ALTER TABLE {self.config.table_name} ADD COLUMN {i} {self.float_value}")
                elif self.column_type == np.bool:
                    self.cursor.execute(f"ALTER TABLE {self.config.table_name} ADD COLUMN {i} {self.bool_value}")
        except Exception as e:
            self.log_text_sgn.emit("HATA (Detaylar için log.log dosyasını kontrol et)")
            log.error(f"add_column_function: {e}",exc_info=True)
    
    def insert_user(self):
        log.debug("insert_user")
        try:
            birlestir = ", ".join(self.config.column.columns)
            column_len = len(self.config.column.columns)
            yer_tutucu = ", ".join(['%s'] * column_len)

            sql_insert = f"INSERT INTO {self.config.table_name} ({birlestir}) VALUES ({yer_tutucu}) "
            self.log_text_sgn.emit(str("Veriler Ekleniyor..."))
            for _,row in self.config.column.iterrows():
                values = tuple(row)
                self.cursor.execute(sql_insert,values)
        except Exception as e:
            log.error(f"insert_user: {e}",exc_info=True)
