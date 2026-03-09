
from tkinter import CASCADE
from django.db import models


product_category_choice = {
    ('FURNITURE', 'FURNITURE'),
    ('COMPUTER APPLICATION', 'COMPUTER APPLICATION'),
    ('ELECTRONIC DEVICES', 'ELECTRONIC DEVICES'),

}

class Category (models.Model):
    category_id = models.CharField(max_length=10, primary_key=True)
    category_name = models.CharField(max_length = 50, blank = True, null = True)

    def __str__(self):
        return self.category_name 


    
class Stock(models.Model):
    product_id = models.CharField(max_length=10, primary_key=True)
    product_category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True)  #fields will be taken from category table
    product_name = models.CharField(max_length=255, blank = True, null = True)
    product_quantity = models.IntegerField(null = True, blank = True, default = '0')
    product_receive_by = models.CharField(max_length=255, blank = True, null = True)
    product_receive_quantity = models.IntegerField(null = True, blank = True, default = '0')
    product_issue_quantity = models.IntegerField(null = True, blank = True, default = '0')
    product_issue_by = models.CharField(max_length=255, blank = True, null = True)
    product_issue_to = models.CharField(max_length=255, blank = True, null = True)
    product_created_by = models.CharField(max_length=255, blank = True, null = True)
    product_reorder_level = models.IntegerField(null = True, blank = True, default = '0')
    product_last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    product_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    #product_date = models.DateTimeField(auto_now_add=False, auto_now=False, blank = True)     #used for user defined date
    

    def __str__(self):
        return self.product_name + "  " + str(self.product_quantity)



class StockHistory(models.Model):
    product_id = models.CharField(max_length=10, primary_key=True)
    product_category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True)  #fields will be taken from category table
    product_name = models.CharField(max_length=255, blank = True, null = True)
    product_quantity = models.IntegerField(null = True, blank = True, default = '0')
    product_receive_by = models.CharField(max_length=255, blank = True, null = True)
    product_receive_quantity = models.IntegerField(null = True, blank = True, default = '0')
    product_issue_quantity = models.IntegerField(null = True, blank = True, default = '0')
    product_issue_by = models.CharField(max_length=255, blank = True, null = True)
    product_issue_to = models.CharField(max_length=255, blank = True, null = True)
    product_created_by = models.CharField(max_length=255, blank = True, null = True)
    product_reorder_level = models.IntegerField(null = True, blank = True, default = '0')
    product_last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, null = True)
    product_timestamp = models.DateTimeField(auto_now_add=True, auto_now=False, null = True)
