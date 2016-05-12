def lists_view(lists):
    """
    View for lists
    :param lists:
    :return:
    """
    if lists:
        view = "*Your lists:*\n\n{}"
        modified_lists = ["*{}.* {}".format(index + 1, value) for index, value in enumerate(lists)]
        return view.format("\n\n".join(modified_lists), )
    else:
        return "No lists yet :("


def notes_view(notes, list_name):
    """
    View for notes
    :param notes:
    :param list_name:
    :return:
    """
    if notes:
        view = "*Your notes of {}*:\n\n{}"
        modified_notes = ["*{}.* {}".format(index + 1, value) for index, value in enumerate(notes)]
        return view.format(list_name, "\n\n".join(modified_notes))
    else:
        return "No notes yet :("


def wrong_message():
    """
    Message when anything was wrong
    :return:
    """
    return "I have no understood your message :("


def help_message():
    """
    Help message
    :return:
    """
    return """
        *MonkeyNoteBot* is a bot which will help you to manage your notes in lists


*COMMANDS:*

*Help*: Set of commands of the Bot

*Showlists*: Check the lists

*Shownotes <list name>* : Check the notes of the given list

*Newlist <list name>*: Add a new list

*Addnote <list name> <note>*: Add a new note to the given list. If the list does not exist, it will be created.

*Addnotes <list name> <notes separated by dots: "." or ". ">*: Add a set of notes to the given list. If the list does not exist, it will be created.

*Removelist <list name>*: Remove the list

*Removenote <list name> <note or note's index>*: Remove the note from the given list

*Removenotes <list name> <notes or note's indexes separated by dots: "." or ". ">*: Remove a set of notes from the given list.
"""
