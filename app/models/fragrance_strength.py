from pydantic import BaseModel, Field


class FragranceStrength(BaseModel):
    id: int = Field(..., description="Unique identifier for the fragrance strength")
    strength_level: int = Field(..., description="Strength level of the fragrance")
    strength_name: str = Field(..., description="Name of the fragrance strength")
    description: str = Field(..., description="Description of the fragrance strength")


if __name__ == "__main__":
    # Eau de Parfum
    fragrance_strength = FragranceStrength(
        id=1,
        strength_level=4,
        strength_name="Eau de Parfum",
        description="A strong and long-lasting fragrance with a high concentration of perfume oils.",
    )
