from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Expense, Category
from .serializers import ExpenseSerializer, CategorySerializer, MonthlySummarySerializer, YearlySummarySerializer
from .filters import ExpenseFilter
import logging


class ExpenseViewSet(ModelViewSet):
    queryset=Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends =[DjangoFilterBackend]
    filterset_fields = ['category_id', 'amount', 'date']
    filterset_class = ExpenseFilter
    
    def get_serializer_context(self):
        return {'request': self.request}

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def destroy(self, request, *args, **kwargs):
        if Expense.objects.filter(expense_id=kwargs['id'].count()>0):
            return Response('This category cannot be deleted because it contains at least one expense', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class MonthlySummaryView(APIView):
    serializer_class = MonthlySummarySerializer

    def get(self, request, *args, **kwargs):
        user_month =request.query_params.get('month')
        if not user_month:
            return Response({'error': 'Please enter the month(YYYY-MM)'}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            year, month=user_month.split('-')
            year=int(year)
            month=int(month)
        except:
            return Response({'error': "Wrong format. Use YYYY-MM"}, status=status.HTTP_400_BAD_REQUEST)
        
        expenses = Expense.objects.annotate(expense_year = ExtractYear('date'),expense_month =ExtractMonth('date')).filter(
            expense_year = year,
            expense_month = month,
            user =request.user
        )
         
        total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
        category_breakdown = expenses.values('category__title').annotate(category_total =Sum('amount')).order_by('-category_total')
        breakdown = []
        for item in category_breakdown:
            breakdown.append({
                'category_title':item['category__title'],
                'category_total_spent': item['category_total']
            })

        data = {
            'month': user_month,
            'total_spent': total_spent,
            'breakdown': breakdown
        }
        serializer = self.serializer_class(data)
        return Response(serializer.data)
    
class YearlySummaryView(APIView):
    serializer_class = YearlySummarySerializer

    def get(self, request, *args, **kwargs):
        user_year =request.query_params.get('year')
        if not user_year:
            return Response({'error': 'Please enter the year(YYYY)'}, status=status.HTTP_400_BAD_REQUEST)
        
        try: 
            year =int(user_year)
        except:
            return Response({'error': "Wrong format. Use YYYY"}, status=status.HTTP_400_BAD_REQUEST)
        
        expenses = Expense.objects.filter(date__year = year,user=request.user)
         
        annual_total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0
        category_breakdown = expenses.values('category__title').annotate(category_total =Sum('amount')).order_by('-category_total')
        breakdown = []
        for item in category_breakdown:
            breakdown.append({
                'category_title':item['category__title'],
                'category_total_spent': item['category_total']
            })

        data = {
            'year': str(user_year),
            'annual_total_spent': annual_total_spent,
            'breakdown': breakdown
        }
        serializer = self.serializer_class(data)
        return Response(serializer.data)
    


logger = logging.getLogger('expensetracker')

def log(request):
    logger.info('This is an expense tracking application')
    logger.warning('This is a warning message')
    return HttpResponse("WHAT'S UP?????")