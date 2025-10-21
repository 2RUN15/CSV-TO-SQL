import mysql.connector
from logindb import connectdb
from convert import convert
import numpy as np
from logla import log_al

log = log_al("logal")

class create_table(connectdb):
    def __init__(self,table_name,column,json_path):
        super().__init__()

        self.exec(json_path)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        self.column = column
        self.table_list = []
        self.column_list = []
        self.liste = []

        #Values
        self.int_value = "INT"
        self.varchar = "VARCHAR(255)"
        self.float_value = "FLOAT"
        self.bool_value = "BOOL"

        self.cursor.execute("SHOW TABLES")
        for table in self.cursor:
            self.table_list.append(table)
        
        if table_name  not in self.table_list:
            self.cursor.execute(f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY
)
""")

            self.add_column()
            self.insert_user()
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    def add_column(self):
        log.debug("add_column")
        try:
            for i in self.column.columns:
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
            log.error(f"add_column_function: {e}",exc_info=True)
    
    def insert_user(self):
        log.debug("insert_user")
        try:
            birlestir = ", ".join(self.column.columns)
            column_len = len(self.column.columns)
            yer_tutucu = ", ".join(['%s'] * column_len)

            sql_insert = f"INSERT INTO {self.table_name} ({birlestir}) VALUES ({yer_tutucu}) "

            for _,row in self.column.iterrows():
                values = tuple(row)
                self.cursor.execute(sql_insert,values)
        except Exception as e:
            log.error(f"insert_user: {e}",exc_info=True)
