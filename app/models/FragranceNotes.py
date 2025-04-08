from pydantic import BaseModel, Field


class FragranceNotes(BaseModel):
    id: int
    note_name: str
    note_type: str


if __name__ == "__main__":
    # Example of creating a FragranceNotes instance
    fragrance_note = FragranceNotes(id=1, note_name="Rose", note_type="Middle")

    print(fragrance_note.json())
