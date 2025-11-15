from field import Field


class NoteText(Field):
  def __init__(self, value):
    if len(value.strip()) == 0:
      raise ValueError("Note text cannot be empty.")
    super().__init__(value)