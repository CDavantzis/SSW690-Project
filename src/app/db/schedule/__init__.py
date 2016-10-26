""" Schedule Database Functions """
import middleware
from app import flask_app, mongo_client
from itertools import combinations, product


def update_db():
    """ Replicate existing course scheduler database in MongoDB """
    db = mongo_client.schedule
    for term in middleware.terms():
        new_data = list(middleware.courses(term[0]))
        if len(new_data) != 0:
            if term[0] not in db.collection_names():
                db[term[0]].insert_many(new_data)
            else:
                db.temp.drop()
                db.temp.insert_many(new_data)
                db.temp.aggregate([{"$out": term[0]}])
                db.temp.drop()


def get_semesters():
    for name in mongo_client.schedule.collection_names():
        if not name.lower().startswith("system"):
            yield name


def get_all():
    """

    :return:
    """
    return mongo_client.schedule["2016F"].find({}, {'_id': False})


def get_tree():
    """

    :return:
    """
    cursor = mongo_client.schedule["2016F"].aggregate([
        {"$group": {"_id": {"prefix": "$section.prefix", "number": "$section.number", "activity": "$activity",
                            "title": "$title"},
                    "nodes": {"$push": {"text": {
                        "$concat": ["$section.prefix", "-", "$section.number", " ", "$activity", "-",
                                    "$section.code"]}}}}},
        {"$sort": {"_id.number": 1}},
        {"$sort": {"_id.prefix": 1}},
        {"$project": {"text": {"$concat": ["$_id.prefix", "-", "$_id.number", " ", "$_id.activity"]},
                      "children": "$nodes"}},
        {"$group": {"_id": {"prefix": "$_id.prefix", "number": "$_id.number", "title": "$_id.title"},
                    "nodes": {"$push": "$$ROOT"}}},
        {"$sort": {"_id.number": 1}},
        {"$sort": {"_id.prefix": 1}},
        {"$project": {"text": {"$concat": ["$_id.prefix", "-", "$_id.number", " ", "$_id.title"]},
                      "children": "$nodes"}},
    ])
    return list(cursor)


def has_conflict(combo):
    for c1, c2 in combinations(combo, 2):
        for m1 in c1.get("meetings", []):
            for m2 in c2.get("meetings", []):
                if (m1['day'] == 'TBA') or (m2['day'] == 'TBA'):
                    continue
                if True in [a == b for a in list(m1["day"]) for b in list(m2["day"])]:
                    if (m1["start_time"] <= m2["end_time"]) and (m2["start_time"] <= m1["end_time"]):
                        return True
                return False


def courses(semester, call_numbers):
    with flask_app.app_context():
        return mongo_client.schedule[semester].aggregate([{"$match": {"_id": {"$in": call_numbers}}},
                                                          {"$group": {"_id": {"prefix": "$section.prefix",
                                                                              "number": "$section.number",
                                                                              "activity": "$activity"},
                                                                      "offerings": {"$push": "$$ROOT"}}}])


def wip():
    for a in product(*(x.get("offerings") for x in courses("2016F", ["10281", "10282", "10283", "10298"]))):
        if not has_conflict(a):
            print a
