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

def get_random_tenders():
    """
    Returns 2 random tenders
    """
    left, right = CONN.srandmember('tenders', 2)
    return get_tender(left), get_tender(right)

def get_tender(tender):
    """
    Returns a tender as a dictionary
    """
    try:
        return json.loads(CONN.get(tender))
    except TypeError:
        return {}

def is_tender(tender):
    """
    Returns whether or not the tender has been added
    """
    CONN.sismember('tenders', tender)

def not_tendered(tender):
    """
    """
    return not (CONN.sismember('tenders', tender) or CONN.sismember('bad', tender))

def bad_tender(tender):
    CONN.srem('tenders', tender)
    CONN.sadd('bad', tender)

def add_tender(tender):
    """
    Takes a dictionary with a field id and creates a record of it in redis
    """
    # need to add the tender to a set of some sort
    CONN.sadd('tenders', tender['id'])
    CONN.set(tender['id'], json.dumps(tender))

def wipe_tenders():
    """
    Deletes everything in the database
    """
    for key in CONN.keys():
        CONN.delete(key)
