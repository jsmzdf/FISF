from behave import *
import requests

# -- Feature: Permisos Scenario: Reconocer Permisos
@given('un {name} para definir')
def step_impl(context, name):
    context.api_url = 'http://localhost:5000/user/' + name
    print('url :'+context.api_url)

@when('se obtiene el permiso')
def step_impl(context):
    response = requests.get(url=context.api_url, headers="")
    print(response.text)
    context.saludo = response.text

@then('el {greet} corresponde al nombre')
def step_impl(context, greet):
    assert (context.saludo == greet)


# -- Feature: Permisos Scenario: Crear Registro
@given('un {user} para crear')
def step_impl(context, user):
    datos = ["nom_usu", "ape_usu", "contra_usu", "email_usu", "proyecto_usu",
                "codigo_usu"]
    campos = [user, user, user+"144000", user+"@d.t", "I"]
    s = "?"
    for i in range(len(campos)): s += datos[i]+"="+campos[i]+"&"
    context.api_url = 'http://localhost:5000/crear' + s [:-1]
    print('url :'+context.api_url)

@when('se solicita insertarlo en la db')
def step_impl(context):
    response = requests.get(url=context.api_url, headers="")
    print(response.text)
    context.mensaje = response.text

@then('el {message} corresponde')
def step_impl(context, message):
    assert (context.mensaje == message)

# -- Feature: Permisos Scenario: Iniciar Sesion
@given('un {user} con su {key}')
def step_impl(context, user, key):
    context.api_url = 'http://localhost:5000/login?codigo_usu=' + user + '&contra_usu=' + key
    # example http://localhost:5000/login?codigo_usu=1&contra_usu=juan144000
    print('url :'+context.api_url)

@when('intenta validar su identidad')
def step_impl(context):
    response = requests.get(url=context.api_url, headers="")
    print(response.text)
    context.mensaje = response.text

@then('se le da un {uphold}')
def step_impl(context, uphold):
    assert (context.mensaje == uphold)