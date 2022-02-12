import requests
from bs4 import BeautifulSoup


class Courses:
    # basic class info
    __class_code = None
    __year = None
    __semester = None
    class_id_list = []
    min_units_list = []
    max_units_list = []
    description_list = []
    URL = None

    def __init__(self, url_):
        self.URL = url_

    def parse(self):
        global __class_code
        global __year
        global __semester
        global URL
        page = requests.get(self.URL)
        soup = BeautifulSoup(page.content, "html.parser")

        # Data members below are the same for all classes on this page
        __class_code = soup.find("abbr").get_text().strip()
        href = soup.find("header", class_="term-banner").find("h2").a.get("href")
        term = href[
            href.find("term-") + 5 : href.find("term-") + 10
        ]  # Grab semester from header href: ex. 20221, 20222
        __year = int(term[0:4])
        __semester = int(term[4:])

        # Get Basic Class Info
        courseTable = soup.find("div", class_="course-table")
        course_info = courseTable.find_all(
            "div", recursive=False
        )  # Find the dividers for each class listed
        for cl in course_info:
            class_id = (
                cl.find(class_="course-id").find("strong").get_text().strip()
            )  # Get course ID (i.e. CSCI 102L)
            cl_num = class_id.split()[1].split(":")[
                0
            ]  # Get just the course number (i.e. 102L), remove the : at the end
            self.class_id_list.append(cl_num)

            units_text = (
                cl.find("span", class_="units").get_text().strip()
            )  # Returns "(X.0-Y.0 units, max Z)"
            units = units_text[1:-1].split(" ", 1)[
                0
            ]  # Grabs just the numerical units (i.e. "1.0-2.0" or "2.0")
            hyphen_loc = units.find("-")
            if hyphen_loc > 0:  # Case for range of units
                min = units[
                    : units.find(".")
                ]  # Drops the ".0" so it can be cast to float
                self.min_units_list.append(float(min))
                max = units[hyphen_loc + 1 : units.find(".", hyphen_loc)]
                self.max_units_list.append(float(max))
            else:  # Case for no range of units
                self.min_units_list.append(float(units[: units.find(".")]))
                self.max_units_list.append(float(units[: units.find(".")]))

            descriptn = (
                cl.find(class_="catalogue").get_text().strip()
            )  # Get class description
            self.description_list.append(descriptn)
            # store info?

            # Get Class Sections

        return None


# Testing
# c1 = Courses("https://classes.usc.edu/term-20221/classes/csci/")
# c1.parse()
# print("Class code: "+c1.get_class_code())
# print("Year: "+str(c1.get_year()))
# print("Semester: "+str(c1.get_semester()))
# for i in range( len(c1.get_class_ids()) ):
#     print(c1.get_class_code() + " " + c1.get_class_ids()[i] + ": " + str(c1.get_min_units_list[i]) + "-" + str(c1.get_max_units_list[i]) + " units" )
#     print(c1.get_descriptions[i])


# class section info
# Section: 41635R
#    - Session: 001
#    - Type: 1 (Lecture)
#           LECTURE = 1, _("Lecture")
#           DISCUSSION = 2, _("Discussion")
#           LAB = 3, _("Lab")
#           QUIZ = 4, _("Quiz")
#    - Time
#        - Start time: 1230PM
#        - End time: 150PM
#    - Days: 1010000 (Translates to: MW)
#    - Instructor: David Kempe
#    - Location
#        - Building: ONLINE
#        - Room #: NULL


class Section:
    section = None
    section_type = None
    start_time = None
    end_time = None
    days = None
    instructor = None
    location_building = None
    location_room = None

    def __init__(self, class_id):
        self.class_id = id
