from conncheck import postgres, mysql, redis, mongodb


def test_postgres():
    assert postgres.is_postgres_accessible() == False


def test_mysql():
    assert mysql.is_mysql_accessible() == False


def test_redis():
    assert redis.is_redis_accessible() == False


def test_mongodb():
    assert mongodb.is_mongodb_accessible() == False
