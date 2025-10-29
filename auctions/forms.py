from django import forms
from django.forms import TextInput, Select, DateTimeInput, NumberInput
from .models import Product, Category, Auction, Bid, Comment

class MyProductForm(forms.ModelForm):
    category = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Category'})
    )

    class Meta:
        model = Product
        fields = ['name','category', 'description', 'long_description','image']
        widgets = {
            "name": TextInput(attrs={'placeholder': 'Name'}),
            "description": forms.Textarea(attrs={'placeholder': 'Short description...'}),
            "long_description": forms.Textarea(attrs={'placeholder': 'Full description...'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['list'] = 'category-list'

    def clean_category(self):
        category_input = self.cleaned_data['category'].strip()
        if not category_input:
            raise forms.ValidationError("Category cannot be empty.")

        category, _ = Category.objects.get_or_create(name=category_input)
        return category

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            category = self.cleaned_data['category']
            instance.categories.set([category])
        return instance
    
class MyAuctionForm(forms.ModelForm):
    class Meta: 
        model = Auction
        fields = ['starting_price', 'auction_status', 'end_time']
        widgets = {
            "starting_price": NumberInput(attrs={'placeholder': '$000.00', 'step':'0.01'}),
            "auction_status": Select(),
            "end_time": DateTimeInput(attrs={'type': 'datetime-local'})
        }
class MyAuctionStatusForm(MyAuctionForm):
    class Meta(MyAuctionForm.Meta):
        fields = ['auction_status']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']