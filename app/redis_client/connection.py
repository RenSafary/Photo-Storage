from redis import Redis


def connect():
    rd = Redis(host="localhost", port=6379, db=0)
    print(rd.ping)
    return rd