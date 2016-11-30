""" Schedule Database Functions """
import middleware
from app import flask_app, mongo_client
from itertools import combinations, product


def update_db(newest_terms=0):
    """ Replicate existing course scheduler database in MongoDB """
    db = mongo_client.schedule
    for term in middleware.terms()[-newest_terms:]:
        print "Updating db {0}".format(term)
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


def get_tree(semester="2016F"):
    """
    :return:
    """
    c = mongo_client.schedule[semester].aggregate([
        {"$group": {"_id": {"prefix": "$section.prefix",
                            "number": "$section.number",
                            "activity": "$activity",
                            "title": "$title"},
                    "nodes": {"$push": {"a_attr": {"call-number": "$_id"},
                                        "text": {
                                            "$concat": ["$section.prefix", "-", "$section.number", " ", "$activity",
                                                        "-", "$section.code"]}}}}},
        {"$sort": {"_id.number": 1}}, {"$sort": {"_id.prefix": 1}},
        {"$project": {"text": {"$concat": ["$_id.prefix", "-", "$_id.number", " ", "$_id.activity"]},
                      "children": "$nodes"}},
        {"$group": {"_id": {"prefix": "$_id.prefix", "number": "$_id.number", "title": "$_id.title"},
                    "nodes": {"$push": "$$ROOT"}}},
        {"$sort": {"_id.number": 1}}, {"$sort": {"_id.prefix": 1}},
        {"$project": {"text": {"$concat": ["$_id.prefix", "-", "$_id.number", " ", "$_id.title"]},
                      "children": "$nodes"}},
    ])
    return list(c)


def has_conflict(combo):
    for c1, c2 in combinations(combo, 2):
        for m1 in c1.get("meetings", []):
            for m2 in c2.get("meetings", []):
                if (m1['day'] == 'TBA') or (m2['day'] == 'TBA'):
                    continue
                # Check if classes are on the same day
                for a in list(m1["day"]):
                    for b in list(m2["day"]):
                        if a == b:
                            # Check if class times overlap
                            if (m1["start_time"] <= m2["end_time"]) and (m2["start_time"] <= m1["end_time"]):
                                return True
    return False


def group_courses(semester="2016F", call_numbers=[]):
    with flask_app.app_context():
        return mongo_client.schedule[semester].aggregate([{"$match": {"_id": {"$in": call_numbers}}},
                                                          {"$group": {"_id": {"prefix": "$section.prefix",
                                                                              "number": "$section.number",
                                                                              "activity": "$activity"},
                                                                      "offerings": {"$push": "$$ROOT"}}}])


def working_class_combinations(semester="2016F", call_numbers=None):
    for class_combination in product(*(x.get("offerings") for x in group_courses(semester, call_numbers))):
        if not has_conflict(class_combination):
            yield class_combination


dow_hash = {"M": 1, "T": 2, "W": 3, "R": 4, "F": 5, "S": 6}


def working_class_combinations_calendar(semester="2016F", call_numbers=None):
    # TODO, PREVENT/warning on MORE THAN 3 ONLINE CLASSES
    for working_class_combination in working_class_combinations(semester, call_numbers):
        combo_option = []
        for db_entry in working_class_combination:
            for meeting in db_entry["meetings"]:
                if meeting["day"] != "TBA":
                    combo_option.append({
                        "title": db_entry["title"],
                        "start": meeting["start_time"].strftime("%H:%M"),
                        "end": meeting["end_time"].strftime("%H:%M"),
                        "dow": map(lambda x: dow_hash.get(x), list(meeting["day"])),
                    })
                else:
                    # Currently assume its an online course
                    combo_option.append({
                        "title": db_entry["title"],
                        "allDay": True,
                        "start": '2000-01-01',
                        "end": '3000-01-01'
                    })
        yield combo_option