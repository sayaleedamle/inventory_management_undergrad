
from django import forms

from .models import Stock,StockHistory

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product_id', 'product_category', 'product_name', 'product_quantity']

    """ def clean_product_id(self):
        product_id = self.cleaned_data.get('product_id')
        if not product_id:
            raise forms.ValidationError("THIS FIELD IS REQUIRED")
            

        for instance in Stock.objects.all():
            if instance.product_id == product_id:
                raise forms.ValidationError(product_id + "is already created")

        return product_id """

    def clean_product_category(self):
        product_category = self.cleaned_data.get('product_category')
        if not product_category:
            raise forms.ValidationError("THIS FIELD IS REQUIRED")
            

        """ for instance in Stock.objects.all():
            if instance.product_category == product_category:
                raise forms.ValidationError(product_category + "is already created")
 """
        return product_category

        


    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if not product_name:
            raise forms.ValidationError("THIS FIELD IS REQUIRED")

        for instance in Stock.objects.all():
            if instance.product_name == product_name:
                raise forms.ValidationError(product_name + " is already created")
        return product_name

class StockSearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required = False)
    class Meta:
        model = Stock
        fields = ['product_category', 'product_name']



class StockHistorySearchForm(forms.ModelForm):
    export_to_CSV = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(required = False)
    end_date = forms.DateTimeField(required = False)
    class Meta:
        model = StockHistory
        fields = ['product_category', 'product_name', 'start_date', 'end_date']



class StockUpdateForm(forms.ModelForm):
    class Meta:
        model= Stock
        fields = ['product_id', 'product_category', 'product_name', 'product_quantity']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["product_issue_quantity", "product_issue_to"]

class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["product_receive_quantity"]

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['product_reorder_level']