from django import forms

class QuestionForm(forms.Form):
    raw_question = forms.CharField(max_length=200)
