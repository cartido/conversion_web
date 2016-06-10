from django import forms

class QuestionForm(forms.Form):
    raw_question = forms.CharField(label = '', widget=forms.TextInput(attrs={'autocomplete':'off'}), max_length=200)
