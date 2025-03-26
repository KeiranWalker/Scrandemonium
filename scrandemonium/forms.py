from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from models import Recipe, Comment, Rating, User


class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'picture', 'video', 'steps', 'ingredients', 'tags', 'category', 'servings']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Dish Name', 
                'required': 'required'
            }),
            'picture': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add A Picture',
                'required': 'required'}),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add A Video'}),
            'steps': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Step 1... {Enter} Step 2... {Enter} Step 3...',
                'required': 'required'}),
            'ingredients': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingredient 1, {Enter} Ingredient 2, {Enter} Ingredient 3...',
                'required': 'required'}),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tags'}),
            'category': forms.Select(choices=Recipe.MEAL_TYPES, attrs={
                'class': 'form-control',
                'required': 'required'
                }),
            'servings': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Servings'}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'biography', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'required': 'required'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email',
                'required': 'required'}),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Password',
                'required': 'required'}),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Confirm Password',
                'required': 'required'}),
            'biography': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'About me...',}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Username',
        'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 
        'placeholder': 'Password',
        'required': 'required'}))


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    details = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a review'}), required=True)
    
    class Meta:
        model = Rating
        fields = ['rating']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Leave a comment'}), required=True)

    class Meta:
        model = Comment
        fields = ['comment']