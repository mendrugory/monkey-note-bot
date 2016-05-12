def find(db, user):
    """
    find the notelist
    :param db:
    :param user:
    :return:
    """
    document = db.notelist.find_one({"_id": user})
    return document


def find_all_lists(db, user):
    """
    It finds all lists
    :param db:
    :param user:
    :return:
    """
    document = db.notelist.find_one({"_id": user}, {"lists": 1})
    return document.get("lists", [])


def find_list(db, user, list_name):
    """
    It finds the list
    :param db:
    :param user:
    :param list_name:
    :return:
    """
    document = db.notelist.find_one({"_id": user}, {"lists.{}".format(list_name): 1})
    if not document:
        return []
    return document["lists"].get(list_name, [])


def find_all_lists_names(db, user):
    """
    It finds all the lists names
    :param db:
    :param user:
    :return:
    """
    document = db.notelist.find_one({"_id": user}, {"lists": 1})
    return [name for name in document["lists"].keys()]


def find_notes(db, user, list_name):
    """
    It returns all the notes of a list
    :param db:
    :param user:
    :param list_name:
    :return:
    """
    document = db.notelist.find_one({"_id": user}, {"lists": 1})
    return document["lists"][list_name]


def insert_new_notelist(db, user):
    """
    It inserts a new notelist
    :param db:
    :param user:
    :return:
    """
    db.notelist.insert({"_id": user, "lists": {}})


def add_new_list(db, user, list_name):
    """
    It adds a new list
    :param db:
    :param user:
    :param list_name:
    :return:
    """
    notelist = find(db, user)
    if not notelist:
        insert_new_notelist(db, user)
    db.notelist.update({"_id": user}, {"$set": {"lists.{}".format(list_name): []}})


def remove_list(db, user, list_name):
    """
    It removes the given list
    :param db:
    :param user:
    :param list_name:
    :return:
    """
    db.notelist.update({"_id": user}, {"$unset": {"lists.{}".format(list_name): 1}})


def add_note(db, user, list_name, note):
    """
    It adds a note
    :param db:
    :param user:
    :param list_name:
    :param note:
    :return:
    """
    the_list = find_list(db, user, list_name)
    if not the_list:
        add_new_list(db, user, list_name)
    db.notelist.update({"_id": user}, {"$addToSet": {"lists.{}".format(list_name): note}})
    return True


def remove_note(db, user, list_name, note):
    """
    It removes a note
    :param db:
    :param user:
    :param list_name:
    :param note:
    :return:
    """
    result = False
    the_list = find_list(db, user, list_name)
    if the_list:
        try:
            index = int(note) - 1
            db.notelist.update({"_id": user}, {"$unset": {"lists.{}.{}".format(list_name, index): 1}})
            db.notelist.update({"_id": user}, {"$pull": {"lists.{}".format(list_name): None}})
        except:
            db.notelist.update({"_id": user}, {"$pull": {"lists.{}".format(list_name): note}})
        result = True
    return result
