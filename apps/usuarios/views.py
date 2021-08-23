from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):
    """Cadastra um novo usuário no sistema."""
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'O Campo Nome não pode ficar em branco')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'O Campo E-mail não pode ficar em branco')
            return redirect('cadastro')

        if not senha.strip():
            messages.error(request, 'O Campo Senha não pode ficar em branco')
            return redirect('cadastro')

        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais!')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, f'O Usuário com o email {email} já está cadastrado na base de dados!')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, f'O Usuário com o Username {nome} já está cadastrado na base de dados!')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Cadastro realizado com sucesso!')

        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    """Realiza o Login de um usuário no sistema."""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos de E-mail ou senha não podem estar vazios')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                print('Login realizado com sucesso')
                return redirect('dashboard')
        else:
            messages.error(request, 'Não foi possível efetuar o Login, verifique os dados e tente novamente.')
    return render(request, 'usuarios/login.html')


def logout(request):
    """Realiza o Logout do Usuário no sistema."""
    auth.logout(request)
    return redirect('index')


def dashboard(request):
    """Retorna uma dashboard do usuário autenticado com as receitas ordenadas por ordem de data invertida
    filtrando pelo ID do usuário para exibir apenas as receitas dele."""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def campo_vazio(campo):
    """Usada para processar um campo vazio nos formulários de autenticação."""
    return not campo.strip()


def senhas_nao_sao_iguais(senha, senha2):
    """Usada para processar se as senhas inseridas são equivalentes."""
    return senha != senha2



