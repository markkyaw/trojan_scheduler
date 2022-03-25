import datetime

from apps.classes.models import *
from apps.users.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Populates 5 BasicClassInfos, 5 BasicClassSessions, 5 Instructors, 5 Users"

    def handle(self, *args, **kwargs):

        # Populating UserInfo.
        ui_list = ["user1", "user2", "user3", "user4", "user5"]

        for user in ui_list:
            # First see if it already exists. If it does, leave it; if it doesn't, create a new User.
            try:
                User.objects.get(username=user)
            except User.DoesNotExist:
                User.objects.create_user(user, user + "@gmail.com", user + "pw")

        # Populating Instructors.
        instructors_list = {
            "Sanjay Madhav": "",
            "David Matthias Kempe": "",
            "Margaret Moser": "",
            "Reuven Firestone": "",
            "Aaron Cote": "",
        }

        for key, value in instructors_list.items():
            obj, created = Instructor.objects.update_or_create(name=key)
            instructors_list[key] = obj

        # Populating BasicClassInfos with Spring 2022 classes.
        classinfo_list = {
            "itp_380": BasicClassInfo.objects.update_or_create(
                class_code="ITP",
                class_number="380",
                year=2022,
                semester=1,
                min_units=4.0,
                max_units=4.0,
            )[0],
            "csci_270": BasicClassInfo.objects.update_or_create(
                class_code="CSCI",
                class_number="270",
                year=2022,
                semester=1,
                min_units=4.0,
                max_units=4.0,
            )[0],
            "ctin_489": BasicClassInfo.objects.update_or_create(
                class_code="CTIN",
                class_number="489",
                year=2022,
                semester=1,
                min_units=2.0,
                max_units=2.0,
            )[0],
            "ctin_484": BasicClassInfo.objects.update_or_create(
                class_code="CTIN",
                class_number="484",
                year=2022,
                semester=1,
                min_units=2.0,
                max_units=2.0,
            )[0],
            "js_314": BasicClassInfo.objects.update_or_create(
                class_code="JS",
                class_number="314",
                year=2022,
                semester=1,
                min_units=4.0,
                max_units=4.0,
            )[0],
        }

        # Populating BasicClassSessions.
        # import pdb; pdb.set_trace()
        itp_380_lec = BasicClassSection.objects.update_or_create(
            class_info=classinfo_list.get("itp_380"),
            section="31908",
            session="001",
            section_type=1,
            start_time=datetime.time(17, 0, 0),
            end_time=datetime.time(18, 30, 0),
            days="0100000",
            location_building="KAP",
            location_room="160",
        )[0]
        itp_380_lec.instructor.set([instructors_list.get("Sanjay Madhav")])
        itp_380_lab = BasicClassSection.objects.update_or_create(
            class_info=classinfo_list.get("itp_380"),
            section="31908",
            session="001",
            section_type=3,
            start_time=datetime.time(17, 0, 0),
            end_time=datetime.time(18, 30, 0),
            days="0001000",
            location_building="KAP",
            location_room="160",
        )[0]
        itp_380_lab.instructor.set([instructors_list.get("Sanjay Madhav")])
        csci270_lec = BasicClassSection.objects.update_or_create(
            class_info=classinfo_list.get("csci_270"),
            section="29957",
            session="001",
            section_type=1,
            start_time=datetime.time(12, 30, 0),
            end_time=datetime.time(13, 50, 0),
            days="1010000",
            location_building="THH",
            location_room="202",
        )[0]
        csci270_lec.instructor.set([instructors_list.get("David Matthias Kempe")])
        csci270_quiz = BasicClassSection.objects.update_or_create(
            class_info=classinfo_list.get("csci_270"),
            section="30224",
            session="001",
            section_type=4,
            start_time=datetime.time(19, 00, 0),
            end_time=datetime.time(20, 50, 0),
            days="0000100",
            location_building="TBA",
        )[0]
        csci270_quiz.instructor.set([instructors_list.get("David Matthias Kempe")])
        csci270_disc = BasicClassSection.objects.update_or_create(
            class_info=classinfo_list.get("csci_270"),
            section="30269",
            session="001",
            section_type=2,
            start_time=datetime.time(14, 00, 0),
            end_time=datetime.time(15, 50, 0),
            days="0000100",
            location_building="THH",
            location_room="202",
        )[0]
        csci270_disc.instructor.set([instructors_list.get("David Matthias Kempe")])
