from pydantic import BaseModel, Field
from server.app.models.FragranceStrength import FragranceStrength


class Fragrance(BaseModel):
    id: int
    name: str
    brand: str
    notes: list[str]
    image_url: str
    scent_profile: str
    strength: FragranceStrength


if __name__ == "__main__":
    # Example usage
    fragrance = Fragrance(
        id=1,
        name="Eau de Toilette",
        brand="Brand Name",
        notes=["Citrus", "Floral", "Woody"],
        image_url="http://example.com/image.jpg",
        scent_profile="Fresh and floral",
    )
    print(fragrance.json())
