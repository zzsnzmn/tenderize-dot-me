"""
Module for voting for tenders
"""
import json
import redis



CONN = redis.StrictRedis(host="localhost", port=6379, db=0)
def vote(tender1, tender2):
    """
    Adds a vote for tender t1 against tender t2
    """
    CONN.incr("{t1}>{t2}".format(t1=tender1, t2=tender2))

def get_vote_count(tender1, tender2):
    """
    Returns a tuple of votes for t1>t2 and t2>t1
    """
    return (CONN.get("{t1}>{t2}".format(t1=tender1, t2=tender2)) or 0,
            CONN.get("{t2}>{t1}".format(t1=tender1, t2=tender2)) or 0)

def get_tender(tender):
    """
    Returns a tender as a dictionary
    """
    try:
        return json.loads(CONN.get(tender))
    except TypeError:
        return {}

def set_tender(key, tender):
    """
    Takes a key and a dictionary and creates a record of it in redis
    """
    CONN.set(key, json.dumps(tender))
