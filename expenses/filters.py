from django_filters.rest_framework import FilterSet, DateFilter
from .models import Expense

class ExpenseFilter(FilterSet):
    date = DateFilter(
        field_name= 'date',
        lookup_expr= 'lte',
        label ='To Date(YYYY-MM-DD)'
    )
    class Meta:
        model = Expense
        fields = {
            'category_id': ['exact'],
            'amount': ['range'],
        }