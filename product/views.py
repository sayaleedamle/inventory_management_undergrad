from email import message
from django.contrib import messages as m1
from logging import warning
from turtle import title
from django.shortcuts import render, redirect

from product.forms import *
from .models import *

from django.http import HttpResponse
import csv

from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    title = "Welcome: This Is The Home Page"
    context = {
        "title" : title,
         #variable link to html page
    }

    return render(request, "home.html", context)

@login_required
def list_items(request):
    title = "LIST OF ITEMS"
    form = StockSearchForm(request.POST or None)

    queryset = Stock.objects.all()      #take list of all items from stock table created in models
    context = {
        "header": title,
        "queryset":queryset,
        "form":form,

    }

    if request.method == 'POST':
        category = form['product_category'].value()
        queryset = Stock.objects.filter(#product_category__icontains = form['product_category'].value(),
         product_name__icontains = form['product_name'].value(),
        )

        if (category != ''):
            queryset = queryset.filter(product_category = category)

        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type = 'text/csv')
            response['Content-Disposition'] = 'attachment; filename = "List of Products.csv"'
            writer = csv.writer(response)
            writer.writerow(['PRODUCT ID', 'CATEGORY', 'PRODUCT NAME', 'QUANTITY'])
            instance = queryset
            for stock in instance:
                writer.writerow([stock.product_id, stock.product_category, stock.product_name, stock.product_quantity])
            return response
        context = {
            "form":form,
            "header": title,
            "queryset":queryset
        }

    
    return render(request, "list_items.html", context)

@login_required
def add_items(request):
    form = StockCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'SUCCESSFULLY SAVED')
        return redirect('/list_items')
    context = {
        "form": form,
        "title" : "Add Item",
    }

    return render(request, "add_items.html", context)

    

def update_items(request, pk):
    queryset = Stock.objects.get(product_id = pk)
    form = StockUpdateForm(instance = queryset)
    if request.method == "POST":
        form = StockUpdateForm(request.POST, instance = queryset) #new information will be updated to the dataset
        if form.is_valid():
            form.save()
            messages.success(request, 'SUCCESSFULLY SAVED')
            return redirect('/list_items')
    context = {
        "form": form,
        
    }

    return render(request, "add_items.html", context)


def delete_items(request, pk):
    queryset = Stock.objects.get(product_id = pk)
    if request.method == "POST":
        queryset.delete()
        messages.success(request, 'SUCCESSFULLY DELETED')
        return redirect('/list_items')
    return render(request, "delete_items.html")


def stock_detail(request, pk):
    queryset = Stock.objects.get(product_id = pk)
    context = {
        
        "queryset" : queryset,
    }

    return render(request, "stock_detail.html", context)


def issue_items(request, pk):
    queryset = Stock.objects.get(product_id = pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.product_receive_quantity = 0
        if instance.product_quantity>instance.product_issue_quantity:
            instance.product_quantity -= instance.product_issue_quantity
            instance.product_issue_by = str(request.user)
            messages.success(request, "ISSUED SUCCESSFULLY " + str(instance.product_quantity) + " " + str(instance.product_name) + "s now left in store")
            instance.save()
        else:
            m1.error(request, "QUANTITY MORE THAN STOCK")
            return redirect('/stock_detail/' + str(instance.product_id))

        return redirect('/stock_detail/' + str(instance.product_id))

    context = {
        "title" : "ISSUE " + str(queryset.product_name),
        "queryset" : queryset,
        "form" : form,
        "username" : "ISSUE BY: " + str(request.user)
    }

    return render(request, "add_items.html", context)


def receive_items(request, pk):
    queryset = Stock.objects.get(product_id = pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.product_issue_quantity = 0
        instance.product_quantity += instance.product_receive_quantity
        instance.product_issue_by = str(request.user)
        messages.success(request, "RECEIVED SUCCESSFULLY " + str(instance.product_quantity) + " " + str(instance.product_name) + "s now in store")
        instance.save()

        return redirect('/stock_detail/' + str(instance.product_id))

    context = {
        "title" : "RECEIVE " + str(queryset.product_name),
        "queryset" : queryset,
        "form" : form,
        "username" : "RECEIVE BY: " + str(request.user)
    }

    return render(request, "add_items.html", context)


def reorder_level(request, pk):
    queryset = Stock.objects.get(product_id = pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit = False)

        #instance.product_quantity += instance.product_receive_quantity
        #instance.product_issue_by = str(request.user)
        messages.success(request, "REORDER LEVEL FOR " + str(instance.product_name) +  " IS UPDATED TO " + str(instance.product_reorder_level))
        instance.save()

        return redirect('/list_items/')

    context = {
        
        "instance" : queryset,
        "form" : form,
        
    }

    return render(request, "add_items.html", context)

@login_required
def list_history(request):
    header = 'HISTORY OF ITEMS'
    queryset = StockHistory.objects.all()
    form = StockHistorySearchForm(request.POST or None)
    context = {
        "header" : header,
        "queryset" : queryset,
        "form" : form
    }


    if request.method == 'POST':
        category = form['product_category'].value()
        
        """ queryset = StockHistory.objects.filter(
                                product_name__icontains=form['product_name'].value()
                                ) """
        queryset = queryset.filter(
                            product_name__icontains=form['product_name'].value(),
                            )
        print('start_date: ' + form['start_date'].value())
        print(len(form['start_date'].value()))
        print(len(form['end_date'].value()))
        #if(form['start_date'].value() != ' ' or form['end_date'].value() != ' '):
        if(len(form['start_date'].value()) > 0 and len(form['end_date'].value()) > 0):
            print(form['start_date'].value()) 
            queryset = queryset.filter(product_last_updated__range=[form['start_date'].value(), form['end_date'].value()]
                )

        if (category != ''):
            queryset = queryset.filter(product_category = category)
            
        


        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="Stock History.csv"'
            writer = csv.writer(response)
            writer.writerow(
                ['CATEGORY', 
                'ITEM NAME',
                'QUANTITY', 
                'ISSUE QUANTITY', 
                'RECEIVE QUANTITY', 
                'RECEIVE BY', 
                'ISSUE BY', 
                'LAST UPDATED'])
            instance = queryset
            for stock in instance:
                writer.writerow(
                [stock.product_category, 
                stock.product_name, 
                stock.product_quantity, 
                stock.product_issue_quantity, 
                stock.product_receive_quantity, 
                stock.product_receive_by, 
                stock.product_issue_by, 
                stock.product_last_updated])
            return response


        context = {
        "form": form,
        "header": header,
        "queryset": queryset,
    }
    return render(request, "list_history.html", context)