from pydantic import BaseModel, Field
from fragrance_strength import FragranceStrength

class Fragrance(BaseModel):
    id: int = Field(..., description="Unique identifier for the fragrance")
    name: str = Field(..., description="Name of the fragrance")
    brand: str = Field(..., description="Brand of the fragrance")
    notes: list[str] = Field(..., description="List of notes in the fragrance")
    image_url: str = Field(..., description="URL of the fragrance image")
    scent_profile: str = Field(..., description="Scent profile of the fragrance")
    strength: FragranceStrength = Field(..., description="Fragrance strength details")



if __name__ == "__main__":
    # Example usage
    fragrance = Fragrance(
        id=1,
        name="Eau de Toilette",
        brand="Brand Name",
        notes=["Citrus", "Floral", "Woody"],
        image_url="http://example.com/image.jpg",
        scent_profile="Fresh and floral"
    )
    print(fragrance.json())