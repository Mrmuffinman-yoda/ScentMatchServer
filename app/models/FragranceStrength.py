from pydantic import BaseModel


class FragranceStrength(BaseModel):
    id: int
    strength_level: int
    strength_name: str
    description: str


if __name__ == "__main__":
    # Eau de Parfum
    fragrance_strength = FragranceStrength(
        id=1,
        strength_level=4,
        strength_name="Eau de Parfum",
        description="A strong and long-lasting fragrance with a high concentration of perfume oils.",
    )
