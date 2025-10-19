import mysql.connector
import json

class connectdb:
    def __init__(self):
        super().__init__()
        with open ("config.json") as f:
            config = json.load(f)
        
        self.conn = mysql.connector.connect(
            host = config["host"],
            user = config["user"],
            password = config["password"],
            database = config["database"]
        )
