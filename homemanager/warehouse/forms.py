#Django imports
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

#Project imports
from .models import Home, Product, Category

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'new_quantity','unit']

    def __init__(self, *args, **kwargs):
        home_instance = kwargs.pop('home_instance', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(home=home_instance)


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name','home']

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['home'].queryset = Home.objects.filter(client=client)


class HomeForm(forms.ModelForm):
    
    class Meta:
        model = Home
        fields = ['name']



