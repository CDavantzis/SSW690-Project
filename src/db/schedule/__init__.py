""" Code for interfacing with the existing stevens course scheduler. """
from pymongo import MongoClient
from datetime import datetime
import re
import urllib2
from xml.dom import minidom

__author__ = "Constantine Davantzis"
__status__ = "Prototype"

# Compile regular expression to find terms in XML response.
re_terms = re.compile(r'<Term Code="(.*)" Name="(.*)"/>')
# Compile regular expression to match parts of course section
re_section = re.compile(r'(?P<prefix>[a-zA-Z]+)\s?(?P<number>\d+)(?P<code>\S+)')


def terms():
    """ Get Term Information
    :returns: A list of term codes and names
    :rtype: list
    """
    f = urllib2.urlopen("https://web.stevens.edu/scheduler/core/core.php?cmd=terms")
    return re_terms.findall(f.read())


def courses(term):
    """ Get Course Information
    :param term: The selected school term.
    :returns: A generator yielding course information for selected term
    :rtype: generator
    """
    f = urllib2.urlopen('https://web.stevens.edu/scheduler/core/core.php?cmd=getxml&term={0}'.format(term))
    for course in minidom.parse(f).getElementsByTagName("Course"):

        # Basic Course Information
        c = {"_id": course.getAttribute('CallNumber'),
             "title": course.getAttribute('Title'),
             "status": course.getAttribute('Status'),
             "section": re_section.match(course.getAttribute('Section')).groupdict(),
             'max_enrollment': int(course.getAttribute('MaxEnrollment')),
             'current_enrollment': int(course.getAttribute('CurrentEnrollment')),
             'instructor_1': course.getAttribute('Instructor1'),
             'instructor_2': course.getAttribute('Instructor2'),
             "meetings": [],
             'requirements': []}

        # Course Meeting Information
        for meeting in course.getElementsByTagName("Meeting"):
            m = {'day': meeting.getAttribute('Day'),
                 'site': meeting.getAttribute('Site'),
                 'building': meeting.getAttribute('Building'),
                 'room': meeting.getAttribute('Room'),
                 'activity': meeting.getAttribute('Activity')}
            if meeting.hasAttribute('StartTime') and meeting.hasAttribute('EndTime'):
                m.update({
                    "start_time": datetime.strptime(meeting.getAttribute('StartTime')[:-4], "%H:%M"),
                    "end_time": datetime.strptime(meeting.getAttribute('EndTime')[:-4], "%H:%M")
                })
            c["meetings"].append(m)

        # Course Requirement Information
        for requirement in course.getElementsByTagName("Requirement"):
            c["requirements"].append({"control": requirement.getAttribute('Control'),
                                      "argument": requirement.getAttribute('Argument'),
                                      "value_1": requirement.getAttribute('Value1'),
                                      "operator": requirement.getAttribute('Operator'),
                                      "value_2": requirement.getAttribute('Value2')})

        # Course Activity Information - To be used to group specific types of classes
        c["activity"] = c["section"]["code"] if len(c["meetings"]) == 0 else c["meetings"][0]['activity']

        yield c


def clone_database(client):
    """ Replicate existing course scheduler database in MongoDB
    """
    db = client.schedule
    for term in terms():
        term_data = list(courses(term[0]))
        if len(term_data) != 0:
            if term[0] not in db.collection_names():
                db[term[0]].insert_many(term_data)
            else:
                db.temp.drop()
                db.temp.insert_many(term_data)
                db.temp.aggregate([{"$out": term[0]}])
                db.temp.drop()


if __name__ == "__main__":
    client = MongoClient()
    clone_database(client)

