from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
import re
import json
import secrets

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        senha = request.POST['password']

        try : senha = int(senha)
        except ValueError : pass

        if re.match('^[a-z0-9!#$%&\'*+-/=?^_`{|}~]+[\._]?[a-z0-9!#$%&\'*+-/=?^_`{|}~]+[@]\w+[.]\w+$', email) is not None and len(str(senha)) == 6 and isinstance(senha, int):
            data = {'token' : secrets.token_hex(16)}
        else:
            data = {'message': 'Campos inválidos'}

        return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'))
