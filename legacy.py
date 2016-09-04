""" Code for interfacing with the existing stevens course scheduler. """
from datetime import datetime
import re
import urllib2
from xml.dom import minidom

__author__ = "Constantine Davantzis"
__status__ = "Prototype"

# Compile regular expression to find terms in XML response.
find_terms = re.compile(r'<Term Code="(.*)" Name="(.*)"/>').findall
# Compile regular expression to match parts of course section
match_section = re.compile(r'(?P<prefix>[a-zA-Z]+)\s?(?P<number>\d+)(?P<code>\S+)').match


def terms():
    """ Get Term Information
    :returns: A list of term codes and names
    :rtype: list
    """
    f = urllib2.urlopen("https://web.stevens.edu/scheduler/core/core.php?cmd=terms")
    return find_terms(f.read())


def courses(term):
    """ Get Course Information
    :param term: The selected school term.
    :returns: A generator yielding course information for selected term
    :rtype: generator
    """
    f = urllib2.urlopen('https://web.stevens.edu/scheduler/core/core.php?cmd=getxml&term={0}'.format(term))
    for course in minidom.parse(f).getElementsByTagName("Course"):

        # Basic Course Information
        c = {"call_number": course.getAttribute('CallNumber'),
             "title": course.getAttribute('Title'),
             "status": course.getAttribute('Status'),
             "section": match_section(course.getAttribute('Section')).groupdict(),
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
                    "start_time": datetime.strptime(meeting.getAttribute('StartTime')[:-4], "%H:%M").time(),
                    "end_time": datetime.strptime(meeting.getAttribute('EndTime')[:-4], "%H:%M").time()
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
        c["activity"] = c["section"] if len(c["meetings"]) == 0 else c["meetings"][0]['activity']

        yield c

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(terms())
    most_recent_term = terms()[-1][0]
    pp.pprint(list(courses(most_recent_term)))
