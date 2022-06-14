from src.app.base.service_nosql_base import BaseService
from src.db.nosql_base import database


class NoteService(BaseService):
    collection = database.get_collection("notes")


note_s = NoteService()
