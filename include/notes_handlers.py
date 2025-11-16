import re
from error import input_error
from notes_book import NotesBook
from note import Note

tag_regex = r"#\w+(?: \w+)*" # matches tags starting with '#' followed by word characters and spaces

@input_error
def add_note(notes: NotesBook, *args):
    # args: note text (may contain spaces) and optional tags starting with '#'
    if len(args) == 0:
        return "Invalid number of arguments. Usage: add-note [text] [#tag1 #tag2 ...]"

    raw_args = " ".join(args)
    tags = set(re.findall(tag_regex, raw_args))
    text = re.sub(tag_regex, "", raw_args).strip()

    try:
        new_note = Note(text)

        if tags:
            for tag in tags:
                if tag:
                    new_note.add_tag(tag)
            notes.add_note(new_note)
        return f"Note added. id: {new_note.id}"
    except Exception as e:
        return str(e)

@input_error
def edit_note(notes: NotesBook, *args):
    # Usage: edit-note [note_id] [new text ...] [#tag1 #tag2 ...]
    if len(args) < 2:
        return "Invalid number of arguments. Usage: edit-note [note_id] [new text] [#tag1 #tag2 ...]"

    note_id = args[0]
    rest = " ".join(args[1:])
    tags = set(re.findall(tag_regex, rest))
    new_text = re.sub(tag_regex, "", rest).strip()

    try:
        updated = notes.edit_note(note_id, new_text)

        if tags:
            updated.note_tags = []
            for tag in tags:
                if tag:
                    updated.add_tag(tag)
        return f"Note {note_id} updated."
    except Exception as e:
        return str(e)

@input_error
def delete_note(notes: NotesBook, *args):
    # Usage: delete-note [note_id]
    if len(args) != 1:
        return "Invalid number of arguments. Usage: delete-note [note_id]"
    note_id = args[0]

    try:
        notes.delete_note(note_id)
        return f"Note {note_id} deleted."
    except Exception as e:
        return str(e)

@input_error
def show_all_notes(notes: NotesBook):
  try:
    if len(notes) == 0:
      return "Notes book is empty."

    return "\n".join([str(note) for note in notes.values()])
  except Exception as e:
    return str(e)
  
@input_error
def find_note_by_id(notes: NotesBook, *args):
    # Usage: note-by-id [note_id]
    if len(args) != 1:
        return "Invalid number of arguments. Usage: note-by-id [note_id]"
    note_id = args[0]

    try:
        note = notes.find_note_by_id(note_id)
        if note is None:
            return f"Note with id '{note_id}' not found."
        return str(note)
    except Exception as e:
        return str(e)
    
@input_error
def remove_tag_from_note(notes: NotesBook, *args):
    # Usage: remove-tag [note_id] [tag]
    if len(args) < 2:
        return "Invalid number of arguments. Usage: remove-tag [note_id] [tag]"

    note_id = args[0]
    tags = re.findall(tag_regex, " ".join(args[1:])) # extract the first tag from args
    if not tags:
        return "Tag is missing or has invalid format. Usage: remove-tag [note_id] [#tag]"
    tag = tags[0]

    
    try:
        note = notes.find_note_by_id(note_id)
        if note is None:
            return f"Note with id '{note_id}' not found."
        note.remove_tag(tag)
        return f"Tag '{tag}' removed from note {note_id}."
    except Exception as e:
        return str(e)
    
@input_error
def edit_tag_in_note(notes: NotesBook, *args):
    #Usage: edit-tag [note_id] [old_tag] [new_tag]
    if len(args) < 3:
        return "Invalid number of arguments. Usage: edit-tag [note_id] [old_tag] [new_tag]"
    
    note_id = args[0]
    tags = re.findall(tag_regex, " ".join(args[1:]))

    if len(tags) < 2:
        return "Invalid number of arguments. Usage: edit-tag [note_id] [old_tag] [new_tag]"

    old_tag = tags[0] # extract the first tag from args
    new_tag = tags[1] # extract the second tag from args

    if old_tag == new_tag:
        return "Old tag and new tag cannot be the same."

    try:
        note = notes.find_note_by_id(note_id)
        if note is None:
            return f"Note with id {note_id} not found."
        
        note.edit_tag(old_tag, new_tag)
        return f"Tag '{old_tag}' updated to '{new_tag}' in note {note_id}."
    except Exception as e:
        return str(e)

@input_error   
def search_notes_by_tags(notes: NotesBook, *args):
    # Usage: search-notes-by-tags [#tag1 #tag2 ...]
    if len(args) == 0:
        return "Invalid number of arguments. Usage: search-notes-by-tags [#tag1 #tag2 ...]"

    tags = re.findall(tag_regex, " ".join(args))

    try:
        notes_found = notes.search_notes_by_tags(tags)
        if not notes_found:
            return "No notes found with the specified tags."
        return "\n".join([str(note) for note in notes_found])

    except Exception as e:
        return str(e)
    
@input_error   
def sort_notes_by_tags(notes: NotesBook):
    try:
        sorted_notes = notes.sort_notes_by_tags()
        if not sorted_notes:
            return "No notes available to sort."
        return "\n".join([str(note) for note in sorted_notes])
    except Exception as e:
        return str(e)

    

# “smart search”, знаходить нотатки навіть тоді, коли:
# слова введені у будь-якому порядку
# слова можуть бути частково введені
# регістр не має значення
# можна вводити кілька слів
# можна вводити частини слів
# знаходить збіги в будь-якій частині тексту

def search_notes_by_text(notes: NotesBook, *args):
    # Usage: search-notes [search_text]
    if len(args) == 0:
        return "Invalid number of arguments. Usage: search-notes [search_text]"
    
    search_text = " ".join(args)

    try:
        found_notes = notes.search_notes_by_text(search_text)
        if not found_notes:
            return f"No notes found containing '{search_text}'."
        return "\n".join([str(note) for note in found_notes])
    except Exception as e:
        return str(e)