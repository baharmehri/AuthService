import redis

redis_connection = None


def get_redis_connection():
    global redis_connection
    if redis_connection is None:
        redis_connection = redis.Redis(host='localhost', port=6379, db=0)
    return redis_connection
