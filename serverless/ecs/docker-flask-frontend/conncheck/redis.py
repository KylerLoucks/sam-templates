import redis
from redis.exceptions import ConnectionError
from config import REDIS_HOST, REDIS_PORT


def create_conn():
    conn = None

    kwargs = {"host": REDIS_HOST}
    if REDIS_PORT:
        kwargs["port"] = REDIS_PORT

    try:
        conn = redis.Redis(**kwargs)
        conn.ping()
        print("Connected to Redis")
    except ConnectionError as e:
        print(f"The error '{e}' occurred")
    return conn


def is_redis_accessible():
    conn = create_conn()
    if conn is not None:
        try:
            conn.ping()
            return True
        except ConnectionError:
            return False
    return False
