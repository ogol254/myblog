from ...database_config import init_db
from datetime import datetime, timedelta
import jwt
import os


class BaseModel(object):
    """docstring for BaseModel"""

    @staticmethod
    def ecnode_token(user_id):
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(days=1),
                "iat": datetime.utcnow(),
                "user": user_id
            }
            token = jwt.encode(
                payload,
                os.getenv("SECRET_KEY"),
                algorithm="HS256"
            )
            resp = token
        except Exception as e:
            resp = e

        return resp

    def blacklisted(self, token):
        dbconn = init_db()
        curr = dbconn.cursor()
        query = """
                SELECT * FROM blacklist WHERE tokens = %s;
                """
        curr.execute(query, [token])
        if curr.fetchone():
            return True
        return False

    def decode_token(self, auth_token):
        """This function takes in an auth
        token and decodes it
        """
        if self.blacklisted(auth_token):
            return "Token has been blacklisted"
        secret = os.getenv("SECRET_KEY")
        try:
            payload = jwt.decode(auth_token, secret)
            return payload['user']  # user id
        except jwt.ExpiredSignatureError:
            return "The token has expired"
        except jwt.InvalidTokenError:
            return "The token is invalid"

    def check_exist(self, table_name, field_name, value):
        con = init_db()
        cur = con.cursor()
        query = "SELECT * FROM {} WHERE {}='{}';".format(table_name, field_name, value)
        cur.execute(query)
        resp = cur.fetchall()
        if resp:
            return True
        else:
            return False

    def delete_item(self, table_name, field_name, value):
        if self.check_exist(table_name, field_name, value) == False:
            return "No such item"

        con = init_db()
        cur = con.cursor()
        query = "DELETE FROM {} WHERE {}={};".format(table_name, field_name, value)
        cur.execute(query)
        con.commit()
        cur.close()
        return 200

    def update_item(self, table_name, field_name, data, item_p, item_id):
        """update the field of an item given the item_id"""
        if self.check_exist(table_name, item_p, item_id) == False:
            return "No such item"

        con = init_db()
        cur = con.cursor()
        cur.execute("UPDATE {} SET {}='{}' \
                     WHERE {} = {} ;".format(table_name, field_name, data, item_p, item_id))
        con.commit()
        return 200
