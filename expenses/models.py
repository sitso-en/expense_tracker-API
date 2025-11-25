from django.db import models
from config import settings

class Expense(models.Model):
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    date = models.DateField(null=True, blank=True)
    notes = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name= 'expense')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='expenses')

    def __str__(self):
        return self.notes
    

class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_expenditure = models.ForeignKey(Expense, on_delete=models.SET_NULL, related_name='+', null=True)

    def __str__(self):
        return self.title
    

class AccountUser(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
