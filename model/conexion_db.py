import sqlite3

class ConexionDb:
    def __init__(self):
        self.base_datos = "database/base.db"
        #conexion a base de datos
        self.conexion = sqlite3.connect(self.base_datos)
        #cursor para ejecutar alguna modificacion a la base
        self.cursor = self.conexion.cursor()
        
    def cerrar(self):
        self.conexion.commit()
        self.conexion.close()