#Django imports
from django import forms
from bootstrap_modal_forms.forms import BSModalModelForm

#Project imports
from .models import Home, Product, Category

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'new_quantity','unit']

    def __init__(self, home_instance, *args, **kwargs):
        
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(home=home_instance)


class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['name','home']

    def __init__(self, user, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['home'].queryset = Home.objects.filter(client=user.client)
 


class HomeForm(forms.ModelForm):
    
    class Meta:
        model = Home
        fields = ['name']

