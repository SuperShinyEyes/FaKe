from django.contrib.auth.models import User
from django import forms
from rango.models import *
from django.forms.extras.widgets import SelectDateWidget
# from django.contrib.admin.widgets import AdminDateWidget

class ProductForm(forms.ModelForm):

    # Multiselect: http://stackoverflow.com/a/11642620/3067013
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects, widget=forms.CheckboxSelectMultiple(), required=False)
    due_date = forms.DateField(widget=SelectDateWidget, initial=get_deadline())
    # due_date = forms.DateField(widget=AdminDateWidget)

    class Meta:
        model = Product
        # fields = ('seller', 'name', 'product_num', 'price', 'stock',)
        fields = ('name', 'product_num', 'price', 'stock', 'due_date', 'categories', 'picture',)
        exclude = ('seller',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    SELLER = '1'
    BUYER = '2'
    USER_CHOICES = (
        (SELLER, 'Seller'),
        (BUYER, 'Buyer'),
    )
    user_cls = forms.ChoiceField(widget=forms.RadioSelect, choices=USER_CHOICES)

    class Meta:
        model = UserProfile
        fields = ('user_cls',)


# class UserProfileForm(forms.ModelForm):
#   class Meta:
#     model = UserProfile
#     fields = ('website', 'picture')

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category
        fields = ('name',)

'''
class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('category',)
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')
'''
