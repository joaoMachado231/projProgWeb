from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Conta, Lucro, Despesa, Objetivo, Conta
from .forms import LucroForm, DespesaForm, ObjetivoForm, MovimentoObjetivoForm, CadastroForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirecione para a página desejada após o login
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home_view(request):
    conta, _ = Conta.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'adicionar_lucro' in request.POST:
            lucro_form = LucroForm(request.POST)
            despesa_form = DespesaForm()
            if lucro_form.is_valid():
                lucro = lucro_form.save(commit=False)
                lucro.user = request.user
                lucro.save()
                return redirect('home')  # nome da url da home
        elif 'adicionar_despesa' in request.POST:
            despesa_form = DespesaForm(request.POST)
            lucro_form = LucroForm()
            if despesa_form.is_valid():
                despesa = despesa_form.save(commit=False)
                despesa.user = request.user
                despesa.save()
                return redirect('home')
    else:
        lucro_form = LucroForm()
        despesa_form = DespesaForm()

    total_lucro = Lucro.objects.filter(user=request.user).aggregate(total=Sum('valor'))['total'] or 0
    total_despesa = Despesa.objects.filter(user=request.user).aggregate(total=Sum('valor'))['total'] or 0

    context = {
        'total_lucro': total_lucro,
        'total_despesa': total_despesa,
        'saldo': conta.saldo,
        'lucro_form': lucro_form,
        'despesa_form': despesa_form,
    }

    return render(request, 'home.html', context)

@login_required
def objetivos_view(request):
    conta = Conta.objects.get(user=request.user)
    objetivos = Objetivo.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'adicionar_objetivo' in request.POST:
            form = ObjetivoForm(request.POST)
            if form.is_valid():
                objetivo = form.save(commit=False)
                objetivo.user = request.user
                objetivo.save()
                return redirect('objetivos')

        elif 'adicionar_valor' in request.POST:
            objetivo_id = request.POST.get('objetivo_id')
            objetivo = get_object_or_404(Objetivo, id=objetivo_id, user=request.user)
            form = MovimentoObjetivoForm(request.POST)
            if form.is_valid():
                valor = form.cleaned_data['valor']
                if valor <= conta.saldo:
                    objetivo.valor_atual += valor
                    conta.saldo -= valor
                    objetivo.save()
                    conta.save()
                return redirect('objetivos')

        elif 'remover_valor' in request.POST:
            objetivo_id = request.POST.get('objetivo_id')
            objetivo = get_object_or_404(Objetivo, id=objetivo_id, user=request.user)
            form = MovimentoObjetivoForm(request.POST)
            if form.is_valid():
                valor = form.cleaned_data['valor']
                if valor <= objetivo.valor_atual:
                    objetivo.valor_atual -= valor
                    conta.saldo += valor
                    objetivo.save()
                    conta.save()
                return redirect('objetivos')

        elif 'excluir_objetivo' in request.POST:
            objetivo_id = request.POST.get('objetivo_id')
            objetivo = get_object_or_404(Objetivo, id=objetivo_id, user=request.user)
            conta.saldo += objetivo.valor_atual  # devolve o valor à conta
            conta.save()
            objetivo.delete()
            return redirect('objetivos')
    else:
        form = ObjetivoForm()

    return render(request, 'objetivos.html', {
        'objetivos': objetivos,
        'form': form,
        'movimento_form': MovimentoObjetivoForm(),
        'saldo': conta.saldo
    })

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Criar a conta associada com saldo zero
            Conta.objects.create(user=user, saldo=0)
            login(request, user)  # opcional: já loga o usuário após cadastro
            return redirect('home')  # redireciona para a home ou outra página
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})
