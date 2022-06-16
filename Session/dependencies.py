import uuid

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

from nameko.extensions import DependencyProvider

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def upload_file(self, file):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM data 
        WHERE file = %s;
        """, (file,))
        for row in cursor.fetchall():
            result.append({
                'file': row['file']
            })
        if result:
            cursor.close()
            return "File Sudah ada!"
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            cursor.execute("""
            INSERT INTO data (id, file)
            VALUES (%s, %s);
            """, (generateUUID, file))
            cursor.close()
            self.connection.commit()
            return "Upload File Success!"

    def download_file(self, id):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM data
        WHERE id = %s;
        """, (id, ))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'file': row['file']
            })
        if result:
            cursor.close()
            return result
        else:
            cursor.close()
            return "File tidak ada!"

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='soa_normal',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error while connecting to MySQL using Connection pool ", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())