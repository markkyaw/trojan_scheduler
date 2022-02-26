# I think these work in principle, but I don't know how to loop through all the possible objects
# this only works if you call it on a specific object

from models import BasicClassInfo, BasicClassSection


class BasicClassInfoView:
    # Create a view that will return a list of basicclasssection objects based on class_code and class_section
    # Ex: If the query passes in "CSCI 102" expect to see all sections that contains CSCI 102
    #    If the query passes in "all" return all classes in basicclassinfo objects ordered alphabetically

    def class_section_search(object, query):
        if query == "all":
            return object
        code = query[: query.index(" ")]
        section = query[query.index(" ") + 1 :]
        if object.class_code == code and object.class_section == section:
            return object

    # Create another view that returns a list of basicclassinfo objects based on class code
    # If the query passes in is "CSCI" expect to see all basicclassinfo that contains "CSCI" so it'll have CSCI 102, CSCI 103, ...

    def class_code_search(object, code):
        if object.class_code.equals(code):
            return object.class_code + " " + object.class_section
