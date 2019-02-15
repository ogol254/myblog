from ...database_config import init_db
from basemodel import BaseModel


class PostModel(BaseModel):
    """docstring for UserModel"""

    def __init__(self, title="title", description="description", created_by="created_by"):
        self.title = title
        self.description = description
        self.created_by = created_by

    # method to save  user data
    def save(self):
        post = {
            "title": self.title,
            "description": self.description,
            "created_by": self.created_by
        }

        con = init_db()
        cur = con.cursor()

        if BaseModel().check_exist('posts', 'title', self.title) == True:
            return "post already exists"

        query = """ INSERT INTO posts (title, description, created_by) VALUES \
					( %(title)s, %(description)s, %(created_by)s) RETURNING post_id """
        cur.execute(query, post)
        post_id = cur.fetchone()[0]
        con.commit()
        cur.close()
        return post_id

    def get_posts(self):
        con = init_db()
        cur = con.cursor()
        query = "SELECT title, description, created_by, post_id, created_on FROM posts;"
        cur.execute(query)
        data = cur.fetchall()
        res = []

        for i, items in enumerate(data):
            title, description, created_by, post_id, created_on = items
            posts = dict(
                post_id=int(post_id),
                title=title,
                description=description,
                created_by=int(created_by),
                created_on=str(created_on)
            )
            res.append(posts)

        return res

    def get_single_post(self, post_id):
        con = init_db()
        cur = con.cursor()
        if BaseModel().check_exist('posts', 'post_id', post_id) == False:
            return 404

        query = "SELECT title, description, created_by, created_on FROM posts WHERE post_id={}".format(post_id)
        cur.execute(query)
        data = cur.fetchall()[0]
        res = []

        posts = dict(
            title=data[0],
            description=data[1],
            created_by=int(data[2]),
            created_on=str(data[3])
        )
        res.append(posts)
        return res
