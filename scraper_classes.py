from datetime import time

import requests
from bs4 import BeautifulSoup

from apps.classes.models import BasicClassInfo, BasicClassSection, Instructor


class Parser:
    soup = BeautifulSoup()

    def __init__(self, url_: str):
        page = requests.get(url_)
        self.soup = BeautifulSoup(page.content, "html.parser")

    def parseClasses(self):
        cl_code = self.soup.find("abbr").get_text().strip()
        href = self.soup.select_one("header > h2 > a").get("href")

        # Grab semester from header href: ex. 20221, 20222
        term = href[href.find("term-") + 5 : href.find("term-") + 10]
        year = int(term[0:4])
        sem = int(term[4:])

        for cl in self.soup.select("div[class~='course-info']"):
            # Course ID (i.e. CSCI 102L)
            course_id = cl.select_one(".course-id strong").get_text().strip()

            # Course number (i.e. 102L), remove the : at the end
            cl_num = course_id.split()[1].split(":")[0]

            # Units
            # Returns "(X.0-Y.0 units, max Z)"
            units_text = cl.find("span", class_="units").get_text().strip()
            # Grabs just the numerical units (i.e. "1.0-2.0" or "2.0")
            units = units_text[1:-1].split(" ", 1)[0]
            min_unit = 0
            max_unit = 0
            hyphen_loc = units.find("-")
            if hyphen_loc > 0:  # Case for range of units
                # Drops the ".0" so it can be cast to float
                min = units[: units.find(".")]
                min_unit = float(min)
                max = units[hyphen_loc + 1 : units.find(".", hyphen_loc)]
                max_unit = float(max)
            else:  # Case for no range of units
                min_unit = float(units[: units.find(".")])
                max_unit = float(units[: units.find(".")])

            # Class description
            descriptn = cl.find(class_="catalogue").get_text().strip()

            # Create database object
            c = BasicClassInfo.objects.create(
                class_code=cl_code,
                class_number=cl_num,
                year=year,
                semester=sem,
                min_units=min_unit,
                max_units=max_unit,
                description=descriptn,
            )

            # Parse Sections
            self.parseSections(cl, c)

        return None

    # REMOVE CLASS_ID AFTER TESTING
    def parseSections(self, class_info: BeautifulSoup, c: BasicClassInfo, class_id):
        # class_info = self.soup.find("div", id=class_code + "-" + class_id)
        s_table = class_info.select_one("table[class~=sections]")

        # FOR TESTING
        id_list = []
        ssn_list = []
        type_list = []
        st_times = []
        end_times = []
        days_list = []
        instr_list = []
        loc_bldgs = []
        loc_rooms = []

        # REMOVE ALL APPENDS AFTER TESTING
        for s in s_table.select("tr"):  # Get all the table rows
            if "headers" in s["class"]:  # Skip header row
                continue
            # Section ID
            id = s.select_one(".section").get_text().strip()
            id_list.append(id)

            # Session
            ssn = s.select_one(".session > a").get_text().strip()
            ssn_list.append(ssn)

            # Session type : 1=lect, 2=disc, 3=lab, 4=quiz
            type_name = s.select_one(".type").get_text().strip()
            type_int = None
            if type_name == "Lecture":
                type_int = 1
            elif type_name == "Discussion":
                type_int = 2
            elif type_name == "Lab":
                type_int = 3
            elif type_name == "Quiz":
                type_int = 4
            type_list.append(type_int)

            # Time
            timeTxt = s.select_one(".time").get_text().strip()
            startTime: time = None
            endTime: time = None
            hyphen = timeTxt.find("-")
            if hyphen != -1:  # assume TBA or incorrectly formatted
                am_pm = timeTxt[-2:]

                start = timeTxt[:hyphen]
                stColon = start.find(":")
                stHr = int(start[:stColon])
                stMin = int(start[stColon + 1 :])

                end = timeTxt[hyphen + 1 : -2]
                endColon = end.find(":")
                endHr = int(end[:endColon])
                endMin = int(end[endColon + 1 :])

                if am_pm == "pm":
                    stHr += 12
                    endHr += 12

                # convert to datetime obj format
                startTime = time(stHr, stMin)
                endTime = time(endHr, endMin)

            st_times.append(startTime)
            end_times.append(endTime)

            # Day(s)
            days_str = ""
            days_txt = s.select_one(".days").get_text().strip()
            if days_txt == "TBA":
                days_str = "0000000"
            else:
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                day_tracker = dict.fromkeys(days, "0")
                i = 0
                print(days_txt)
                while days_txt.find(",") != -1:
                    i += 2  # to account for the ', ' btwn days
                    septr = days_txt.find(",", i)
                    # get first 3 letters
                    temp_day = days_txt[i:septr][i : i + 3]
                    if temp_day in day_tracker:
                        print("in while loop: " + temp_day)
                        day_tracker[temp_day] = "1"
                    i = septr
                if days_txt[i : i + 3] in day_tracker:
                    print("outside while loop: " + days_txt[i : i + 3])
                    day_tracker[days_txt[i : i + 3]] = "1"
                # Append all to string
                for j in day_tracker:
                    days_str += day_tracker[j]
            days_list.append(days_str)

            # Instructor(s)
            instr_name = s.select_one(".instructor > a").get_text().strip()
            instr = Instructor.objects.create(name=instr_name)
            instr_list.append(instr_name)

            # Location
            location = s.select_one(".location").get_text().strip()
            loc_bldg = location
            loc_room = location
            for i, char in enumerate(location):
                if char.isdigit():
                    loc_bldg = location[:i]
                    loc_bldgs.append(loc_bldg)
                    loc_room = location[i:]
                    loc_rooms.append(loc_room)
                    break
            # REMOVE ELSE AFTER TESTING
            else:
                # assume TBA or otherwise not formatted
                loc_bldgs.append(location)
                loc_rooms.append(location)

            # Create database object
            sect: BasicClassSection = BasicClassSection.objects.create(
                c,
                section=id,
                session=ssn,
                section_type=type_int,
                start_time=startTime,
                end_time=endTime,
                days=days_str,
                location_building=loc_bldg,
                location_room=loc_room,
            )
            sect.instructor.add(instr)

        print("CSCI" + class_id)
        print("Section ID: ")
        print(id_list)
        print("Session: ")
        print(ssn_list)
        print("Type: ")
        print(type_list)
        print("Start: ")
        print(st_times)
        print("End: ")
        print(end_times)
        print("Days: ")
        print(days_list)
        print("Instructor: ")
        print(instr_list)
        print("Location: ")
        print(loc_bldgs)
        print(loc_rooms)

        return None


# Testing
c1 = Parser("https://classes.usc.edu/term-20221/classes/csci/")
c1.parseClasses()
