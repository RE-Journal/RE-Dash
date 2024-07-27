import mysql.connector
from mysql.connector import pooling
import pandas as pd

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.connection_pool = None
        return cls._instance

    def initialize_pool(self, pool_name="mypool", pool_size=5):
        if self.connection_pool is None:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                host='193.203.184.1',
                user='u661384233_dbuser',
                password='Rejournal@123',
                database='u661384233_rejournal'
            )

    def get_connection(self):
        if self.connection_pool is None:
            self.initialize_pool()
        return self.connection_pool.get_connection()

    def execute_query(self, query, params=None):
        connection = self.get_connection()
        try:
            with connection.cursor(dictionary=True) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
            return result
        finally:
            connection.close()

    def execute_query_pandas(self, query, params=None):
        connection = self.get_connection()
        try:
            if params:
                df = pd.read_sql(query, connection, params=params)
            else:
                df = pd.read_sql(query, connection)
            return df
        finally:
            connection.close()

db_manager = DatabaseManager()
db_manager.initialize_pool()