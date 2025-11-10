from dataclasses import dataclass

@dataclass
class behaviour_config:
    table_name : str
    column: str
    json_path: str
    table_index: int
    ui: str
    localtext: str
    databasedbtext: str
    usernametext: str
    dbpasswordtext: str

@dataclass
class login_config:
    json_path: str
    localtext: str
    databasedbtext: str
    usernametext: str
    dbpasswordtext: str