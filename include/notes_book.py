import re
from collections import UserDict
from note import Note

class NotesBook(UserDict):

  def find_note_by_id(self, note_id: str) -> Note | None:
    return self.data.get(note_id)
  
  def find_note_by_text(self, text: str) -> Note | None:
    for note in self.data.values():
      if note.note_text.value == text:
        return note
    return None

  def add_note(self, note: Note):
    if self.find_note_by_text(note.note_text.value):
      raise KeyError(f"Note with text '{note.note_text.value}' already exists.")
    self.data[note.id] = note

  def edit_note(self, note_id: str, new_text: str):
    note = self.find_note_by_id(note_id)
    if note is None:
      raise KeyError(f"Note with text '{note_id}' not found.")
    
    existing_note = self.find_note_by_text(new_text)
    if existing_note and existing_note.id != note_id:
      raise KeyError(f"Another note with text '{new_text}' already exists.")
    
    note.note_text.value = new_text
    return note

  def delete_note(self, note_id: str):
    if note_id not in self.data:
      raise KeyError(f"Note with id '{note_id}' not found.")
    
    del self.data[note_id]
 
  def search_notes_by_text(self, text: str) -> list[Note]:
    tokens = text.lower().split()

    result = []
    for note in self.data.values():
      note_text = note.note_text.value.lower()
      if all(re.search(re.escape(token), note_text) for token in tokens):
        result.append(note)
    return result