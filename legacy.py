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


def get_terms():
    """ Get list of terms
    :returns: A list of term codes and names
    :rtype: list
    """
    f = urllib2.urlopen("https://web.stevens.edu/scheduler/core/core.php?cmd=terms")
    return find_terms(f.read())


def get_courses(term):
    """ Get course data
    :param term: The selected school term.
    """
    f = urllib2.urlopen('https://web.stevens.edu/scheduler/core/core.php?cmd=getxml&term={0}'.format(term))
    for course in minidom.parse(f).getElementsByTagName("Course"):
        course_entry = {"call_number": course.getAttribute('CallNumber'),
                        "title": course.getAttribute('Title'),
                        "status": course.getAttribute('Status'),
                        "section": match_section(course.getAttribute('Section')).groupdict(),
                        'max_enrollment': int(course.getAttribute('MaxEnrollment')),
                        'current_enrollment': int(course.getAttribute('CurrentEnrollment')),
                        'instructor': course.getAttribute('Instructor1'),
                        "meetings": []}

        for meeting in course.getElementsByTagName("Meeting"):
            meeting_entry = {'day': meeting.getAttribute('Day'),
                             'site': meeting.getAttribute('Site'),
                             'building': meeting.getAttribute('Building'),
                             'room': meeting.getAttribute('Room'),
                             'activity': meeting.getAttribute('Activity')}

            if meeting.hasAttribute('StartTime') and meeting.hasAttribute('EndTime'):
                meeting_entry.update({
                    "start_time": datetime.strptime(meeting.getAttribute('StartTime')[:-4], "%H:%M").time(),
                    "end_time": datetime.strptime(meeting.getAttribute('EndTime')[:-4], "%H:%M").time()
                })

            course_entry["meetings"].append(meeting_entry)

        # Todo: Include Requirement Elements
        print course_entry

if __name__ == "__main__":
    print get_terms()
    get_courses(get_terms()[-1][0])
