import mysql.connector
import json
from package_values import login_config

class connectdb:
    def __init__(self):
        super().__init__()

    def login(self, conf: login_config):
        self.conf = conf
        
        if self.conf.json_path:
            with open (self.conf.json_path) as f:
                config = json.load(f)

            self.conn = mysql.connector.connect(
                host = config["host"],
                user = config["user"],
                password = config["password"],
                database = config["database"]
        )
        
        else:
            self.conn = mysql.connector.connect(
                host = self.conf.localtext,
                user = self.conf.usernametext,
                password = self.conf.dbpasswordtext,
                database = self.conf.databasedbtext
        )