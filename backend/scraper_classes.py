from datetime import time

import requests
from apps.classes.models import BasicClassInfo, BasicClassSection, Instructor
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        return None

    # Takes in a url for a particular term (i.e. Spring 2022, Summer 2022)
    def parse(self, url_: str):
        page = requests.get(url_)
        dptSoup = BeautifulSoup(page.content, "html.parser")
        urls = self.__getDepartmentURLs(dptSoup)
        for i in urls:
            print("Scraping: " + i)
            self.parseClasses(i)
        print("scraping completed.")
        return None

    def __getDepartmentURLs(self, soup: BeautifulSoup):
        hrefs = []  # list of string urls to dept class listings
        dpts = soup.select("li[data-type='department'] > a")
        for i in dpts:
            href = i.get("href")
            hrefs.append(href)
        return hrefs

    def parseClasses(self, url_: str):
        page = requests.get(url_)
        soup = BeautifulSoup(page.content, "html.parser")
        cl_code = soup.find("abbr").get_text().strip()
        href = soup.select_one("header > h2 > a").get("href")

        # Grab semester from header href: ex. 20221, 20222
        term = href[href.find("term-") + 5 : href.find("term-") + 10]
        year = int(term[0:4])
        sem = int(term[4:])

        for cl in soup.select("div[class~='course-info']"):
            # Course ID (i.e. CSCI 102L)
            course_id = cl.select_one(".course-id strong").get_text().strip()

            # Course number (i.e. 102L), remove the : at the end
            cl_num = course_id.split()[1].split(":")[0]

            # Units
            # Returns "(X.0-Y.0 units, max Z)"
            units_text = cl.find("span", class_="units").get_text().strip()
            # Grabs just the numerical units (i.e. "1.0-2.0" or "2.0")
            units = units_text[1:-1].split(" ", 1)[0]
            min_unit = 0.0
            max_unit = 0.0
            hyphen_loc = units.find("-")
            dot_loc = units.find(".")
            min = units[:dot_loc]
            min_unit = float(min)
            if hyphen_loc > 0:  # Case for range of units
                # Drops the ".0" so it can be cast to float
                max = units[hyphen_loc + 1 : units.find(".", hyphen_loc)]
                max_unit = float(max)
            else:  # Case for no range of units
                max_unit = min_unit

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
            self.__parseSections(cl, c)

        return None

    def __parseSections(self, class_info: BeautifulSoup, c: BasicClassInfo):
        s_table = class_info.select_one("table[class~=sections]")

        for s in s_table.select("tr"):  # Get all the table rows
            if "headers" in s["class"]:  # Skip header row
                continue
            if s.select_one(".section") == None:
                continue
            # temporary fix for the chem labs (332, 423) that meet multiple times a day
            if "secondLine" in s["class"]:
                continue

            # Section ID
            scraped_id = s.select_one(".section")
            id = ""
            if scraped_id != None:
                id = scraped_id.get_text().strip()

            # Session
            scraped_ssn = s.select_one(".session > a")
            ssn = ""
            if scraped_ssn != None:
                ssn = scraped_ssn.get_text().strip()

            # Session type : 1=lect, 2=disc, 3=lab, 4=quiz, 5=lecture-lab
            scraped_type = s.select_one(".type")
            type_int = None
            if scraped_type != None:
                type_name = scraped_type.get_text().strip()
                if type_name == "Lecture":
                    type_int = 1
                elif type_name == "Discussion":
                    type_int = 2
                elif type_name == "Lab":
                    type_int = 3
                elif type_name == "Quiz":
                    type_int = 4
                elif type_name == "Lecture-Lab":
                    type_int = 5

            # Time
            scraped_time = s.select_one(".time")
            timeTxt = ""
            if scraped_time != None:
                timeTxt = scraped_time.get_text().strip()
            startTime: time = None
            endTime: time = None
            hyphen = timeTxt.find("-")
            if hyphen != -1:  # assume TBA or incorrectly formatted
                am_pm = timeTxt[-2:]

                start = timeTxt[:hyphen]
                stColon = start.find(":")
                stHr = int(start[:stColon])
                stMin = int(start[stColon + 1 :])

                end = timeTxt[hyphen + 1 : timeTxt.find("m") - 1]
                endColon = end.find(":")
                endHr = int(end[:endColon])
                endMin = int(end[endColon + 1 :])

                if am_pm == "pm":
                    # for classes that start in am, end in pm (after 12:59)
                    if endHr < stHr:
                        endHr += 12
                    # catches classes with start, end times around ~12 pm
                    elif stHr < 12 and endHr < 12:
                        stHr += 12
                        endHr += 12

                # convert to datetime obj format
                startTime = time(stHr, stMin)
                endTime = time(endHr, endMin)

            # Day(s)
            days_temp = list("0000000")
            # In case of TBA, defaults to model default "0000000"
            days_txt = ""
            scraped_days = s.select_one(".days")
            if scraped_days != None:
                days_txt = scraped_days.get_text().strip()
            days = ["M", "Tu", "W", "Th", "F", "Sa", "Su"]
            for i, day in enumerate(days):
                idx = days_txt.find(day)
                if idx != -1:
                    days_temp[i] = "1"
            days_str = "".join(days_temp)

            # Instructor(s)
            scraped_instr = s.select_one(".instructor")
            instr_name = ""
            if scraped_instr != None:
                instr_name = scraped_instr.get_text().strip()

            # Location
            scraped_loc = s.select_one(".location")
            location = ""
            if scraped_loc != None:
                location = scraped_loc.get_text().strip()
            loc_bldg = location
            loc_room = location
            for i, char in enumerate(location):
                if char.isdigit():
                    loc_bldg = location[:i]
                    loc_room = location[i:]
                    break

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
            instr = Instructor.objects.create(name=instr_name)
            sect.instructor.add(instr)

        return None


# Example Util
# p = Parser()
# p.parse("https://classes.usc.edu/term-20221/") #full schedule
# p.parseClasses("https://classes.usc.edu/term-20221/classes/chem/") #by department
