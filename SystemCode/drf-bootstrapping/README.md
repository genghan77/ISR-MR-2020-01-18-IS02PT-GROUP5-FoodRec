pip install django
pip install djangorestframework
pip install pygments



python manage.py shell

from foodrec.models import Food
food = Food(name='6-inch Oven Roasted Chicken Breast Sandwich, Subway',group='FAST FOODS',nutrient_sugar_amount=5.98,nutrient_sugar_unit='g',nutrient_protein_amount=23,nutrient_protein_unit='g')
food.save()

food = Food(name='Chicken, breast, fried, skinless',group='MEAT AND MEAT PRODUCTS',nutrient_sugar_amount=0,nutrient_sugar_unit='g',nutrient_protein_amount=40.13,nutrient_protein_unit='g')
food.save()

from foodrec.serializers import FoodSerializer
serializer=FoodSerializer(food)
serializer.data


from rest_framework.renderers import JSONRenderer
content = JSONRenderer().render(serializer.data)
content


import io
from rest_framework.parsers import JSONParser
stream = io.BytesIO(content)
data = JSONParser().parse(stream)

serializer = FoodSerializer(data=data)
serializer.is_valid()
serializer.validated_data




serializer = FoodSerializer(Food.objects.all(), many=True)
serializer.data



python manage.py runserver