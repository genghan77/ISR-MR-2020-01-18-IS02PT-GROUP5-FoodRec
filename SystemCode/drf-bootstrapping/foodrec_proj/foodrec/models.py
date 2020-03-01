from django.db import models

FOOD_GROUPS = sorted(
                    [
                        ("BEVERAGES", "BEVERAGES"), 
                        ("CEREAL AND CEREAL PRODUCTS", "CEREAL AND CEREAL PRODUCTS"),
                        ("EGG AND EGG PRODUCTS", "EGG AND EGG PRODUCTS"),
                        ("FAST FOODS", "FAST FOODS"),
                        ("FISH AND FISH PRODUCTS", "FISH AND FISH PRODUCTS"),
                        ("FRUIT AND FRUIT PRODUCTS", "FRUIT AND FRUIT PRODUCTS"),
                        ("HEALTHIER CHOICE SYMBOL (HCS) PRODUCTS", "HEALTHIER CHOICE SYMBOL (HCS) PRODUCTS"),
                        ("MEAT AND MEAT PRODUCTS", "MEAT AND MEAT PRODUCTS"),
                        ("MILK AND MILK PRODUCTS", "MILK AND MILK PRODUCTS"),
                        ("MISCELLANEOUS", "MISCELLANEOUS"),
                        ("MIXED ETHNIC DISHES, ANALYZED IN SINGAPORE", "MIXED ETHNIC DISHES, ANALYZED IN SINGAPORE"),
                        ("NUTS AND SEEDS, PULSES AND PRODUCTS", "NUTS AND SEEDS, PULSES AND PRODUCTS"),
                        ("OILS AND FATS", "OILS AND FATS"),
                        ("OTHER MIXED ETHNIC DISHES", "OTHER MIXED ETHNIC DISHES"),
                        ("SUGARS, SWEETS AND CONFECTIONERY", "SUGARS, SWEETS AND CONFECTIONERY"),
                        ("VEGETABLE AND VEGETABLE PRODUCTS", "VEGETABLE AND VEGETABLE PRODUCTS"),
                    ])


class Food(models.Model):
    name = models.CharField(max_length=100, blank=False)
    group = models.CharField(max_length=100, choices=FOOD_GROUPS, default='MISCELLANEOUS')
    nutrient_protein_amount = models.FloatField()
    nutrient_protein_unit = models.CharField(max_length=10)
    nutrient_sugar_amount = models.FloatField()
    nutrient_sugar_unit = models.CharField(max_length=10)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return self.name