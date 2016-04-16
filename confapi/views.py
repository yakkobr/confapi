# coding=utf-8
import os
import sys
import json
import re
import requests
import collections
import ast

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from confapi.models import Confapi
from pprint import pformat
from django.conf import settings


path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../exec/")
sys.path.append(path)

from dizzy_zabbix import Zabbix


class IndexView(generic.DetailView):
    model = Confapi
    template_name = 'confapi/index.html'


class ConfigureView(generic.DetailView):
    # model =
    template_name = 'confapi/configure.html'


class ExtrasView(generic.DetailView):
    # model =
    template_name = 'confapi/extras.html'


class UseView(generic.DetailView):
    # model =
    template_name = 'confapi/use.html'


def healthcheck(request):
    return HttpResponse("WORKING")

def index(request):
    return render(request, 'confapi/index.html')


def help(request):
    return HttpResponseRedirect(settings.ENDPOINT_DOC)
    # return render(request, 'confapi/configure.html')


def configure(request):
    return render(request, 'confapi/configure.html')


def extras(request):
    return render(request, 'confapi/index.html')


def use(request):
    endpoint_options = settings.ENDPOINT_OPTIONS

    if request.POST:
        function_params = {}
        access_params = {}
        for k, v in request.POST.items():
            if re.match('^z_', k):
                access_params[k] = v
            elif k != 'csrfmiddlewaretoken':
                if v:
                    if v[0] == '{':
                        function_params[k] = ast.literal_eval(v)
                    else:
                        function_params[k] = v
        function = 'globo.' + function_params.pop('function') if not re.search('^.+\..+$', function_params[
            'function']) else function_params.pop('function')
        https = access_params.get('z_https', False)
        if not re.match('^http', access_params['z_endpoint']):
            access_params['z_endpoint'] = 'https://' + access_params['z_endpoint'] if https else 'http://' + \
                                                                                                 access_params[
                                                                                                     'z_endpoint']
        # print function_params

        try:
            z = Zabbix(access_params['z_endpoint'], access_params['z_username'], access_params['z_password'])
        except Exception:
            return render(request, 'confapi/use.html', {'post': True, 'error': True,
                                                        'endpoint_options': endpoint_options,
                                                        'response': "Não foi possível logar na API. Verifique os parâmetros de login.",
                                                        'z_endpoint': access_params['z_endpoint'],
                                                        'z_username': access_params['z_username'],
                                                        'z_password': access_params['z_password'],
                                                        'access_params': pformat(access_params, indent=4, width=40, ),
                                                        'function_params': pformat(function_params, indent=4, width=20),
                                                        'https': https})

        # z = Zabbix (access_params['z_endpoint'], access_params['z_username'], access_params['z_password'])

        api_response = z.x(function, function_params)
        api_response_json = json.dumps(api_response)
        return render(request, 'confapi/use.html',
                      {'post': True, 'response': api_response_json, 'endpoint_options': endpoint_options,
                       'z_endpoint': access_params['z_endpoint'],
                       'z_username': access_params['z_username'], 'z_password': access_params['z_password'],
                       'access_params': pformat(access_params, indent=4, width=40, ),
                       'function_params': pformat(function_params, indent=4, width=20), 'https': https})
    else:
        return render(request, 'confapi/use.html', {'post': False, 'endpoint_options': endpoint_options})


def api_functions(request):
    '''
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/confapi/data/api_functions.json")
    data = open(json_path)
    response = json.load(data)
    data.close()
    '''
    black_methods = ['userlogin']

    https = request.GET['z_https']
    gbix_endpoint = request.GET['endpoint'] + '/api/methods'

    if https == 1:
        protocol = 'https://'
    elif https == 0:
        protocol = 'http://'
    else:
        protocol = 'http://'

    if not re.match('^http', gbix_endpoint):
        gbix_endpoint = protocol + gbix_endpoint

    code = requests.get(gbix_endpoint)
    code_json = code.json()

    confapi_methods = {}

    for method in code_json:
        confapi_methods[method['name']] = {}
        # print method['name']

        for group_params in method['parameter']['fields']:
            for parameter in method['parameter']['fields'][group_params]:
                if not re.match('\w+\.\w+', parameter['field']):
                    confapi_methods[method['name']][parameter['field']] = {}
                    if parameter['optional'] is False:
                        confapi_methods[method['name']][parameter['field']]['optional'] = 0
                        confapi_methods[method['name']][parameter['field']]['values'] = list()
                        confapi_methods[method['name']][parameter['field']]['default'] = ""
                    else:
                        confapi_methods[method['name']][parameter['field']]['optional'] = 1
                        confapi_methods[method['name']][parameter['field']]['values'] = list()
                        if 'defaultValue' in parameter:
                            confapi_methods[method['name']][parameter['field']]['default'] = parameter['defaultValue']
                        else:
                            confapi_methods[method['name']][parameter['field']]['default'] = ""

                    if 'allowedValues' in parameter:
                        confapi_methods[method['name']][parameter['field']]['type'] = 2
                        for value in parameter['allowedValues']:
                            confapi_methods[method['name']][parameter['field']]['values'].append(value.replace("'", ''))
                    elif parameter['type'] == 'Object':
                        confapi_methods[method['name']][parameter['field']]['type'] = 1
                    else:
                        confapi_methods[method['name']][parameter['field']]['type'] = 0
        #Sort Alphabetically by Parameter of Method
        confapi_methods[method['name']] = collections.OrderedDict(sorted(confapi_methods[method['name']].items()))            
    
    for black_method in black_methods:
        if black_method in confapi_methods:
            confapi_methods.pop(black_method)

    confapi_methods = collections.OrderedDict(sorted(confapi_methods.items()))

    return HttpResponse(json.dumps(confapi_methods), content_type="application/json")
    '''return HttpResponse(json.dumps(response), content_type="application/json")'''
 
