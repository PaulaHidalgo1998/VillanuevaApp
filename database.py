import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS personas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    dinero REAL NOT NULL,
                    tipo_aportacion TEXT NOT NULL
                )
            """)
            self.connection.commit()

    def add_persona(self, nombre, apellidos, dinero, tipo_aportacion):
        with self.connection:
            self.connection.execute("""
                INSERT INTO personas (nombre, apellidos, dinero, tipo_aportacion)
                VALUES (?, ?, ?, ?)
            """, (nombre, apellidos, dinero, tipo_aportacion))
            self.connection.commit()

    def delete_persona(self, persona_id):
        with self.connection:
            self.connection.execute("""
                DELETE FROM personas WHERE id = ?
            """, (persona_id,))
            self.connection.commit()

    def delete_all(self):
        with self.connection:
            self.connection.execute("DELETE FROM personas")
            self.connection.commit()

    def get_personas(self):
        with self.connection:
            return self.connection.execute("SELECT * FROM personas").fetchall()
        
    def count_personas(self):
        query = "SELECT COUNT(*) FROM personas"
        cursor = self.connection.execute(query)
        count = cursor.fetchone()[0]
        return count
