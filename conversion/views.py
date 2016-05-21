from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
from conversion.forms import QuestionForm
from conversion.pintparser import PintParser
from pint import DimensionalityError

# Create your views here.
def home(request):
    text = """<h1>Bienvenue!</h1>"""

    return HttpResponse(text)

def date_actuelle(request):
    return render(request,'conversion/date.html', {'date': datetime.now()})

def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            response = None
            source_measure = None
            target_unit = None

            raw_question = form.cleaned_data['raw_question']
            parser = PintParser(raw_question)


            if parser.error:
                messages.add_message(request,messages.ERROR, parser.error)

            else:
                source_measure = '{:P}'.format(parser.source_unit)
                target_unit = '{:P}'.format(parser.target_unit)
                response = '{:~P}'.format(parser.response)

    else:
        form = QuestionForm()

    return render(request, 'conversion/question.html', locals())