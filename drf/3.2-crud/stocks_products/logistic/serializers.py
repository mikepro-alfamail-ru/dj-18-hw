from rest_framework import serializers
from .models import Product, Stock, StockProduct

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=True,
    )
    stock = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        required=True,
    )
    quantity = serializers.IntegerField(min_value=1, default=1)
    price = serializers.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0,
    )

    def create(self, validated_data):
        print('_______0')
        super.create(self, validated_data)

    def validate(self, attrs):
        print('______1')
        super.validate(self, attrs)

    class Meta:
        model = StockProduct
        fields = ('id', 'stock', 'product', 'quantity', 'price')


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def validate(self, attrs):
        print('______1')
        super.validate(self, attrs)

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # создаем склад по его параметрам
        stock = super().create(**validated_data)

        for position in positions:
            print(stock, position)
            StockProduct.objects.update_or_create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)

        positions_to_remove = {position.id: position for position in stock.positions.all()}
        for position in positions:
            position_, created_ = StockProduct.objects.get_or_create(**position)
            position_.stock = stock
            position_.save()
            positions_to_remove.pop(position_.id)

        for position_ in positions_to_remove.values():
            position_.delete()

        return stock
