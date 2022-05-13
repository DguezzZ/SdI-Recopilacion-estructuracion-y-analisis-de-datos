from .entities.User import User
import sqlite3

class ModelUser():

    @classmethod
    def login(self, database, user):
        try:
            con = sqlite3.connect('database.db')
            controlador = con.cursor()

            sql = """SELECT id, contrasena FROM usuarios
                    WHERE id = '{}'""".format(user.id)
            controlador.execute(sql)
            row = controlador.fetchone()
            if row != None:
                user = User(row[0],User.check_password(row[1], user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id FROM usuarios WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)