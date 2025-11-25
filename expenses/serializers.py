
from rest_framework import serializers
from .models import Expense, Category

class CategoryTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['title']

class ExpenseSerializer(serializers.ModelSerializer):
    category=CategoryTitleSerializer()
    class Meta:
        model = Expense
        fields = ['id','amount', 'date','notes', 'category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'featured_expenditure']

class CategorySummarySerializer(serializers.Serializer):
    category_title = serializers.CharField(max_length=255)
    category_total_spent = serializers.DecimalField(max_digits=10, decimal_places=2)

class MonthlySummarySerializer(serializers.Serializer):
    month = serializers.CharField(max_length =7)
    total_spent=serializers.DecimalField(max_digits=12, decimal_places=2)
    breakdown = CategorySummarySerializer(many=True)

class YearlySummarySerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    annual_total_spent = serializers.DecimalField(max_digits=12, decimal_places=2)
    breakdown = CategorySummarySerializer(many=True)