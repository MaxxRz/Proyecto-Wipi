from .conexion_db import ConexionDb


class TablaDB(ConexionDb):
    def __init__(self, nombreTabla, nombreColumnas):
        self.nombreTabla = nombreTabla
        self.nombreColumnas = nombreColumnas
            
        
    def __str__(self):
        return f'el nombre es: {self.nombreTabla} y las columnas: {self.nombreColumnas}'
    
    
    def test(self, **kwargs):
        keys = ', '.join(self.nombreColumnas)
        placeholders = ', '.join(['?'] * len(self.nombreColumnas))
        valores = tuple(col for col in self.nombreColumnas)
        print(f"1. {keys}")
        print(f"2. {placeholders}") 
        print(f"3. {valores}")
    
            
        
    #Existe La tabla
    def isExist(self):        
        ## Creacion de las columnas 
        columnas = []
        
        for inx, columna in enumerate(self.nombreColumnas):
            if inx == 0:
                columnas.append(f"id_{columna} INTEGER PRIMARY KEY AUTOINCREMENT")   
            columnas.append(f'{columna} VARCHAR(50)')
        
        
        ## creamos los sql antes de solicitarlos
        sql = f'''
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='{self.nombreTabla}';
            '''
        sql2 = f'''
                CREATE TABLE {self.nombreTabla}(
                {','.join(columnas)}
            )'''
            
        ## se crea la conexion e intentamos realizar la solicitud para conocer su existencia
        conexion = ConexionDb()
        try:
            conexion.cursor.execute(sql)
            resultado = conexion.cursor.fetchone()
        except Exception as e:
            print(f"❌ Error en en: {str(e)}")
            return False
        
        # si retorna False significa que no existe y procederemos a crearla
        if not resultado:
            conexion.cursor.execute(sql2)            
        
        conexion.cerrar()


    # > methodo para insertar un valor nuevo,
    # para guardar hay que nombrar la columna Ej: insertar(pantalla="xx.xx.xx.xx",)
    def insertar(self, **kwargs):
        keys = ', '.join(kwargs) #Ej: antalla, fk_campana
        placeholders = ', '.join(['?'] * len(kwargs)) #Ej: ?, ?
        valores = tuple(kwargs[col] for col in kwargs) #Ej: ('10.152.150.129', 'Heylo')
        
        sql = f'''
            INSERT INTO {self.nombreTabla} ({keys}) VALUES ({placeholders})
            '''       
            
        conexion = ConexionDb()
        #intenta mandar el resultado al db por conexion
        try:
            conexion.cursor.execute(sql, valores)
            conexion.cerrar()
            return True
        except Exception as e:
            print(f"❌ Error en en: {str(e)}")
            return False
         
                 
    # > methodo para obtener el listado solicitado
    def obtenerTodo(self):       
        # Realiza peticion de todas las columnas 
        sql = f''' SELECT * FROM {self.nombreTabla} '''        
        
        conexion = ConexionDb()
        conexion.cursor.execute(sql)
        
        resultados = conexion.cursor.fetchall()
        conexion.cerrar()
        
        return resultados
        
    
    # > methodo para obtener una columna en especial
    def obtenerColumna(self, columna):
        # Realiza peticion de una columna
        sql = f''' SELECT {columna} FROM {self.nombreTabla} '''        
        
        conexion = ConexionDb()
        conexion.cursor.execute(sql)
        
        resultados = conexion.cursor.fetchall()
        conexion.cerrar()
        
        listado = [lista[0] for lista in resultados]


        return listado
    
    
    # > methodo para obtener una columna en especial
    # este methodo solo es para las pantallas
    def obtenerColumnaRestriccion(self, campana):
        # Realiza peticion de una columna
        sql = f'''SELECT pantalla FROM {self.nombreTabla} WHERE fk_campana IN ('{campana}')'''        
        
        conexion = ConexionDb()
        conexion.cursor.execute(sql)
        
        
        resultados = conexion.cursor.fetchall()
        conexion.cerrar()
        
        listado = [lista[0] for lista in resultados]


        return listado
        
        
    # > methodo para eliminar uno o mas valores a traves de un array
    # si se elimina pantallas hay que declarar la campaña a la cual pertenecen esas pantallas
    def eliminar(self, listaParaBorrar, campana = None):
        conexion = ConexionDb()
    
        #placeholders = ', '.join(['?'] * len(listaParaBorrar))
                    
        try:    
            # Ejecutar DELETE
            if campana:
                sql = f'''
                    DELETE FROM {self.nombreTabla} 
                    WHERE {self.nombreColumnas[0]} IN ({','.join(['?'] * len(listaParaBorrar))})
                    AND {self.nombreColumnas[1]} = "{campana}"
                    '''
            else:
                sql = f'''
                    DELETE FROM {self.nombreTabla} WHERE {self.nombreColumnas[0]} IN ({','.join(['?'] * len(listaParaBorrar))})
                    '''
                
            conexion.cursor.execute(sql, listaParaBorrar)
            conexion.cerrar()
            
            return True
        except Exception as error:
            return False
    