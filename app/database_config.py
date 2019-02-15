import os
import psycopg2

# host = 'localhost'
# user = 'Mcogol'
# port = 5432
# password = 'root'
# dbname = 'myblog'

uri = "dbname='myblog_test' host='127.0.0.1' port='5432' user='Mcogol' password='root'"
test_uri = "dbname='myblog_test' host='127.0.0.1' port='5432' user='Mcogol' password='root'"
# url for databse connection
#uri = os.getenv(['DATABASE_URL'])

# url for test databse connection
#test_uri = os.getenv(['DATABASE_TEST_URL'])


# return connection
def connection(url):
    con = psycopg2.connect(url)
    return con


# return connection and creates tables
def init_db():
    con = connection(uri)
    cur = con.cursor()
    queries = tables()

    for query in queries:
        cur.execute(query)
    con.commit()
    return con


# return connection and creates tables (TDD)
def init_test_db():
    con = connection(test_uri)
    cur = con.cursor()
    queries = tables()

    for query in queries:
        cur.execute(query)
    con.commit()
    return con

# Deletes all tables after tests have been run


def destroydb():
    con = connection(test_uri)
    cur = con.cursor()

    posts = """ DROP TABLE IF EXISTS posts CASCADE; """
    users = """ DROP TABLE IF EXISTS users CASCADE;  """
    blacklist = """ DROP TABLE IF EXISTS blacklist CASCADE;  """

    queries = [posts, users, blacklist]

    for query in queries:
        cur.execute(query)
    con.commit()

# contain all table creation queries


def tables():
    users = """ CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY NOT NULL,
    name character varying(50) NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(50),
    date_created timestamp with time zone DEFAULT ('now'::text)::date NOT NULL,
    password character varying(500) NOT NULL );"""

    posts = """CREATE TABLE IF NOT EXISTS posts (
    post_id serial PRIMARY KEY NOT NULL,
    created_by character varying(20) NOT NULL,
    description character varying(200) NOT NULL,
    title character varying(50),
    created_on timestamp with time zone DEFAULT ('now'::text)::date NOT NULL
    ); """

    blacklist = """CREATE TABLE IF NOT EXISTS blacklist (
    tokens character varying(200) NOT NULL
    );"""

    queries = [posts, users, blacklist]
    return queries
