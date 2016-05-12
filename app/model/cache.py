def get_last_message_id(db):
    doc = db.cache.find_one({"_id": "last_message_id"})
    return doc['last_message_id'] if doc else 0


def set_last_message_id(db, last_message_id):
    db.cache.save({"_id": "last_message_id", "last_message_id": last_message_id})
