import re
from app.settings import mongodb
from app.telegram.api import send_message
from app.model import notelist as notelistmodel
from app.monkeynote import monkeyview

HELP_PATTERN = "help|Help|HELP"
ADD_LIST_PATTERN = "newlist|NewList|Newlist\W(.*)"
ADD_NOTE_PATTERN = "addnote|AddNote|addNote|Addnote\W(\w+)\W(.*)"
ADD_NOTES_PATTERN = "addnotes|AddNotes|addNotes|Addnotes\W(\w+)\W(.*)"
REMOVE_LIST_PATTERN = "removeList|removelist|RemoveList|Removelist\W(.*)"
REMOVE_NOTE_PATTERN = "removeNote|removenote|RemoveNote|Removenote\W(\w+)\W(.*)"
REMOVE_NOTES_PATTERN = "removeNotes|removenotes|RemoveNotes|Removenotes\W(\w+)\W(.*)"
SHOW_LISTS_PATTERN = "showlists|ShowLists|showLists|Showlists"
SHOW_NOTES_PATTERN = "ShowNotes|showNotes|shownotes|Shownotes\W(.*)"


def execute(message, chat_id):
    """
    Execute the actions depending to the message
    :param chat_id:
    :param message:
    :return:
    """
    if __analyze_message(message, HELP_PATTERN):
        result = __help()
    elif __analyze_message(message, ADD_LIST_PATTERN):
        result = add_list(chat_id, message)
    elif __analyze_message(message, ADD_NOTE_PATTERN):
        result = add_note(chat_id, message)
    elif __analyze_message(message, ADD_NOTES_PATTERN):
        result = add_notes(chat_id, message)
    elif __analyze_message(message, REMOVE_LIST_PATTERN):
        result = remove_list(chat_id, message)
    elif __analyze_message(message, REMOVE_NOTE_PATTERN):
        result = remove_note(chat_id, message)
    elif __analyze_message(message, REMOVE_NOTES_PATTERN):
        result = remove_notes(chat_id, message)
    elif __analyze_message(message, SHOW_LISTS_PATTERN):
        result = show_lists(chat_id)
    elif __analyze_message(message, SHOW_NOTES_PATTERN):
        result = show_notes(chat_id, message)
    else:
        result = __help()
        result["text"] = "I have no idea what you want :P !!\nI will send you a description ;)\n\n{}" \
            .format(result["text"])
        print(result)
    result.update({"chat_id": chat_id})
    send_message(result)


def __analyze_message(message, pattern):
    """
    It detects if it matches the pattern
    :param message:
    :param pattern:
    :return:
    """
    return re.search(pattern, message)


def __help():
    """
    Help message
    :return:
    """
    return {"text": monkeyview.help_message(), "parse_mode": "Markdown"}


def add_note(chat_id, message):
    """
    It adds a note
    :param chat_id:
    :param message:
    :return:
    """
    result = re.search(ADD_NOTE_PATTERN, message)
    list_name = result.groups()[0]
    note = result.groups()[1]
    if list_name and note:
        notelistmodel.add_note(mongodb, chat_id, list_name, note)
        text = "The note was added to the list: {}. :D".format(list_name)
    else:
        text = monkeyview.wrong_message()
    return {"text": text, "parse_mode": "Markdown"}


def add_notes(chat_id, message):
    """
    It adds a note
    :param chat_id:
    :param message:
    :return:
    """
    result = re.search(ADD_NOTES_PATTERN, message)
    list_name = result.groups()[0]
    notes = __split(result.groups()[1])
    if list_name and notes:
        for note in notes:
            notelistmodel.add_note(mongodb, chat_id, list_name, note)
        text = "The notes were added to the list: {}. :D".format(list_name)
    else:
        text = monkeyview.wrong_message()
    return {"text": text, "parse_mode": "Markdown"}


def add_list(chat_id, message):
    """
    It adds a list
    :param chat_id:
    :param message:
    :return:
    """
    result = re.search(ADD_LIST_PATTERN, message)
    list_name = result.groups()[0]
    if list_name:
        notelistmodel.add_new_list(mongodb, chat_id, list_name)
        text = "The list {} has been created :D".format(list_name)
    else:
        text = monkeyview.wrong_message()
    return {"text": text, "parse_mode": "Markdown"}


def show_lists(chat_id):
    """
    It shows all the lists of the given user
    :param chat_id:
    :return:
    """
    lists = notelistmodel.find_all_lists(mongodb, chat_id)
    return {"text": monkeyview.lists_view(lists), "parse_mode": "Markdown"}


def show_notes(chat_id, message):
    """
    It shows all the notes of the given user/list
    :param chat_id:
    :param message:
    :return:
    """
    result = re.search(SHOW_NOTES_PATTERN, message)
    list_name = result.groups()[0]
    notes = notelistmodel.find_notes(mongodb, chat_id, list_name)
    return {"text": monkeyview.notes_view(notes, list_name), "parse_mode": "Markdown"}


def remove_list(chat_id, message):
    """
    It removes a list
    :param chat_id:
    :param message:
    :return:
    """
    result = re.search(REMOVE_LIST_PATTERN, message)
    list_name = result.groups()[0]
    if list_name:
        notelistmodel.remove_list(mongodb, chat_id, list_name)
        text = "The list {} has been removed :D".format(list_name)
    else:
        text = monkeyview.wrong_message()
    return {"text": text, "parse_mode": "Markdown"}


def remove_note(chat_id, message):
    """
    It removes a note
    :param chat_id:
    :param message:
    :return:
    """
    result = re.search(REMOVE_NOTE_PATTERN, message)
    list_name = result.groups()[0]
    note = result.groups()[1]
    if list_name and note:
        notelistmodel.remove_note(mongodb, chat_id, list_name, note)
        text = "The note has been removed from the list {} :D".format(list_name)
    else:
        text = monkeyview.wrong_message()
    return {"text": text, "parse_mode": "Markdown"}


def remove_notes(chat_id, message):
    """
    It removes notes
    :param chat_id:
    :param message:
    :return:
    """
    result = re.search(REMOVE_NOTES_PATTERN, message)
    list_name = result.groups()[0]
    notes = __split(result.groups()[1])
    if list_name and notes:
        try:
            modified_notes = [int(note) for note in notes]
        except:
            modified_notes = notes
        for note in sorted(modified_notes, reverse=True):
            notelistmodel.remove_note(mongodb, chat_id, list_name, note)
        text = "The notes were removed from the list: {}. :D".format(list_name)
    else:
        text = monkeyview.wrong_message()
    return {"text": text, "parse_mode": "Markdown"}


def __split(str, separator="."):
    """
    Custom split
    :param str:
    :param separator:
    :return:
    """
    parts = [note.strip() for note in str.split(separator)]
    return filter(lambda x: x != '', parts)
