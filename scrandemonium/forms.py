from django import forms 
from django.contrib.auth.models import User
from rango.models import Recipe, User, Review

class AddRecipe(forms.ModelForm):
    dishName = forms.CharField(max_length=128,
                           help_text="Recipe name") #required
    picture = forms.IntegerField(widget=forms.HiddenInput(), initial=0) #TODO required
    video = forms.IntegerField(default=0) #TODO optional
    steps = forms.SlugField(unique=True) #TODO required
    ingredients = forms.SlugField(unique=True) #TODO required
    tags = forms.SlugField(unique=True) #TODO optional
    category = forms.SlugField(unique=True) #TODO required, use choices
    servings = forms.IntegerField(default=0) #optional
    class Meta:
        model = Recipe
        fields = ('name',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta: 
        model = User
        fields = ('username', 'email', 'password',)

class LoginForm(forms.ModelForm):
    title = forms.CharField(max_length=128,
                            help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data 
        url = cleaned_data.get('url')
        
        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data

class ReviewForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta: 
        model = Review
        fields = ('Rating', 'Details',)

class UserProfileForm(forms.ModelForm): 
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)