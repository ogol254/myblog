from ...database_config import init_db
from basemodel import BaseModel


class UserModel(BaseModel):
    """docstring for UserModel"""

    def __init__(self, name="name", email="email", password="password", username="username"):
        self.name = name
        self.email = email
        self.password = password
        self.username = username

    # method to save  user data
    def save(self):
        user = {
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

        con = init_db()
        cur = con.cursor()

        if BaseModel().check_exist('users', 'email', self.email) == True:
            return "user already exists"

        query = """ INSERT INTO users (name, username, email, password) VALUES \
                    ( %(name)s, %(username)s, %(email)s, %(password)s) RETURNING user_id """
        cur.execute(query, user)
        user_id = cur.fetchone()[0]
        con.commit()
        con.close()
        return user_id

    def logout(self, token):
        con = init_db()
        cur = con.cursor()
        query = "INSERT INTO blacklist (tokens) VALUES ('{}');".format(token)
        cur.execute(query)
        con.commit()
        cur.close()

    def get_user_by_username(self, username):
        """return user from the db given a username"""
        database = init_db()
        curr = database.cursor()
        curr.execute(
            """SELECT user_id, password \
            FROM users WHERE username = '%s'""" % (username))
        data = curr.fetchone()
        curr.close()
        return data
