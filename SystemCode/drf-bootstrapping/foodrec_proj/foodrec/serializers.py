from rest_framework import serializers
from foodrec.models import Food

class FoodSerializer(serializers.HyperlinkedModelSerializer):
    selfLink = serializers.HyperlinkedIdentityField(view_name='food-detail', read_only=True)
    class Meta:
        model = Food
        fields = ['id', 'name', 'selfLink']

class FoodDetailSerializer(serializers.HyperlinkedModelSerializer):
    selfLink = serializers.HyperlinkedIdentityField(view_name='food-detail', read_only=True)
    class Meta:
        model = Food
        fields = ['id', 'name', 'group', 'nutrient_protein_amount', 'nutrient_protein_unit', 'nutrient_sugar_amount', 'nutrient_sugar_unit', 'selfLink']