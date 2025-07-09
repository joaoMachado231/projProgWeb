import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LucroForm, DespesaForm, ObjetivoForm, MovimentoObjetivoForm, CadastroForm

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        response = requests.post('http://localhost:3333/login', json={
            'email': email,
            'password': password
        })

        if response.status_code == 200:
            data = response.json()
            request.session['user'] = data['user']
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')

def logout_view(request):
    return redirect('login')

def home_view(request):
    user = request.session.get('user')

    if request.method == 'POST':
        print('POST data:', request.POST)
        if 'adicionar_lucro' in request.POST:
            lucro_form = LucroForm(request.POST)
            despesa_form = DespesaForm()
            if lucro_form.is_valid():
                valor = lucro_form.cleaned_data['valor']
                print(valor)
                requests.post('http://localhost:3333/profit', json={
                    'user_id': user.get('id'),
                    'valor': float(valor)
                })
                return redirect('home')  # nome da url da home
        elif 'adicionar_despesa' in request.POST:
            despesa_form = DespesaForm(request.POST)
            lucro_form = LucroForm()
            if despesa_form.is_valid():
                valor = despesa_form.cleaned_data['valor']
                print(valor)
                requests.post('http://localhost:3333/expense', json={
                    'user_id': user.get('id'),
                    'valor': float(valor)
                })
                return redirect('home')
    else:
        response = requests.get(f'http://localhost:3333/info?user_id={user.get('id')}')
        infoConta = response.json()
        request.session['conta'] = infoConta
        lucro_form = LucroForm()
        despesa_form = DespesaForm()

    context = {
        'total_lucro': infoConta.get('lucro'),
        'total_despesa': infoConta.get('despesa'),
        'saldo': infoConta.get('conta').get('saldo'),
        'lucro_form': lucro_form,
        'despesa_form': despesa_form,
    }

    return render(request, 'home.html', context)

def objetivos_view(request):
    user = request.session.get('user')
    objetivos = {}

    if request.method == 'POST':
        if 'adicionar_objetivo' in request.POST:
            form = ObjetivoForm(request.POST)
            if form.is_valid():
                nomeObjetivo = form.cleaned_data['nome']
                valorMeta = form.cleaned_data['valor_meta']
                requests.post('http://localhost:3333/objetivos/create', json={
                    'user_id': user.get('id'),
                    'nome': nomeObjetivo,
                    'valor_meta': float(valorMeta)
                })
                return redirect('objetivos')

        elif 'adicionar_valor' in request.POST:
            objetivo_id = request.POST.get('objetivo_id')
            form = MovimentoObjetivoForm(request.POST)

            if form.is_valid():
                valor = form.cleaned_data['valor']
                requests.post('http://localhost:3333/objetivos/adicionar-saldo', json={
                    "objetivo_id": objetivo_id,
                    "valor": float(valor)
                })
                return redirect('objetivos')

        elif 'remover_valor' in request.POST:
            objetivo_id = request.POST.get('objetivo_id')
            form = MovimentoObjetivoForm(request.POST)
            if form.is_valid():
                valor = form.cleaned_data['valor']
                requests.post('http://localhost:3333/objetivos/remover-saldo', json={
                    "objetivo_id": objetivo_id,
                    "valor": float(valor)
                })
                return redirect('objetivos')

        elif 'excluir_objetivo' in request.POST:
            objetivo_id = request.POST.get('objetivo_id')
            requests.delete(f'http://localhost:3333/objetivos/{objetivo_id}')
            return redirect('objetivos')
    else:
        responseObjetivos = requests.get(f'http://localhost:3333/objetivos?user_id={user.get('id')}')
        objetivosJson = responseObjetivos.json()
        objetivos = objetivosJson.get('objetivos')
        response = requests.get(f'http://localhost:3333/info?user_id={user.get('id')}')
        infoConta = response.json()
        print(objetivos)
        form = ObjetivoForm()

    return render(request, 'objetivos.html', {
        'objetivos': objetivos,
        'form': form,
        'movimento_form': MovimentoObjetivoForm(),
        'saldo': infoConta.get('conta').get('saldo')
    })

def cadastro_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        userName = request.POST.get('userName')

        response = requests.post('http://localhost:3333/users/create', json={
            'email': email,
            'password': password,
            'username': userName
        })
        return redirect('login')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})
