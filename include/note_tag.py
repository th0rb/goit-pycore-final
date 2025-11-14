from field import Field


class NoteTag(Field):
  def __init__(self, value):
    if len(value) > 20:
      raise ValueError("The tag is too long. Maximum length is 20 characters.")
    super().__init__(value)