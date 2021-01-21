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
from http import HTTPStatus
import re
import json
import secrets
import requests

def index(request):
    return render(request, 'index.html')

def deslogar(request):
    del request.session["token"]
    with open('static/btc/js/currencies.json', "r+") as cur:
        currencies = { "BRL": "5.400", "EUR": "0.920", "CAD": "1.440" }
        cur.seek(0)
        json.dump(currencies, cur, indent=5)
        cur.truncate()
        cur.close()
    return HttpResponse('Deslogado com sucesso!')

@csrf_exempt
def api(request, tool):
    if tool == 'login':
        if request.method == "POST":
            email = request.POST['email']
            senha = request.POST['password']

            try : senha = int(senha)
            except ValueError : pass

            if re.match('^[a-z0-9!#$%&\'*+-/=?^_`{|}~]+[\._]?[a-z0-9!#$%&\'*+-/=?^_`{|}~]+[@]\w+[.]\w+$', email) is not None and len(str(senha)) == 6 and isinstance(senha, int):
                data = {'token' : secrets.token_hex(16)}
                request.session['token'] = data['token']
                status = 200
            else:
                data = {'message': 'Campos inválidos'}
                status = 400

            return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'), status=status)
    elif tool == 'btc':
        if request.method == "GET":
            with open('static/btc/js/currencies.json') as cur : currencies = json.loads(cur.read())
            coindesk = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
            newcur = json.loads(coindesk.text)
            insertC = {"BRL": {"code": "BRL", "description": "Brazilian Real"}, "EUR": {"code": "EUR", "description": "Euro"}, "CAD": {"code": "CAD", "description": "Canadian Dollar"}}

            for c in currencies:
                rid = float(currencies[c]) * newcur['bpi']['USD']['rate_float']
                insertC[c]['rate'] = str(rid)
                insertC[c]['rate_float'] = float(rid)

            newcur['bpi'].update(insertC)

            try:
                auth = request.headers['Authorization']
            except KeyError:
                auth = False

            if auth == request.session['token']:
                data = newcur
                status = 200
            else:
                data = { "message": "Token inválido" }
                status = 401
        else:
            curAvailable = ["BRL", "EUR", "CAD"]
            currency = request.POST["currency"]
            val = request.POST["value"]

            try : val = int(val)
            except ValueError : val = -1

            if currency in curAvailable and val > 0:
                with open('static/btc/js/currencies.json', "r+") as cur:
                    currencies = json.loads(cur.read())
                    currencies[currency] = str(val)
                    cur.seek(0)
                    json.dump(currencies, cur, indent=5)
                    cur.truncate()
                    cur.close()
                status = 200
                data = { "message": "Valor alterado com sucesso!" }
            elif val < 0:
                 status = 400
                 data = { "message": "Valor inválido" }
            else:
                status = 400
                data = { "message": "Moeda inválida" }
        return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'), status = status)
    else:
        status = 404
        data = { "message": "Endpoint não encontrado" }
        return HttpResponse(json.dumps(data, ensure_ascii=False).encode('utf8'), status = status)
