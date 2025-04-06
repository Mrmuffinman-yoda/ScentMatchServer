from pydantic import BaseModel, Field


class FragranceNotes(BaseModel):
    id: int = Field(..., description="Unique identifier for the fragrance note")
    note_name: str = Field(..., description="Name of the fragrance note")
    note_type: str = Field(
        ..., description="Type of the fragrance note (e.g., top, middle, base)"
    )


if __name__ == "__main__":
    # Example of creating a FragranceNotes instance
    fragrance_note = FragranceNotes(id=1, note_name="Rose", note_type="Middle")

    print(fragrance_note.json())
