import uuid
from note_tag import NoteTag
from note_text import NoteText


class Note:
    def __init__(self, text):
        self.__id = uuid.uuid4().hex[:8]
        self.note_text: NoteText = NoteText(text)
        self.note_tags: list[NoteTag] = []


    @property
    def id(self):
        return self.__id

    def add_tag(self, tag):
        self.note_tags.append(NoteTag(tag))

    def remove_tag(self, tag):
        self.note_tags = list(filter(lambda p: p.value != tag, self.note_tags))
    
    def edit_tag(self, old_tag, new_tag):
        self.note_tags = list(map(lambda tag: NoteTag(new_tag) if tag.value == old_tag else tag, self.note_tags))

    def find_tag(self, target_tag):
        for tag in self.note_tags:
            if tag.value == target_tag:
                return tag
        return None

    def __str__(self):
        return f"Note id: {self.id} text: {self.note_text.value}, tags: {'; '.join(t.value for t in self.note_tags)}"