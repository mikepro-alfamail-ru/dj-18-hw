from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ('product', 'quantity', 'price')


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, **position)
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        positions_to_remove = {position.id: position for position in stock.positions.all()}
        for position in positions:
            position_, created_ = StockProduct.objects.get_or_create(stock=stock, **position)
            if not created_:
                positions_to_remove.pop(position_.id)
        for position_ in positions_to_remove.values():
            position_.delete()

        return stock
