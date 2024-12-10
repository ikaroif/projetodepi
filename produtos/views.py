from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from .forms import ProdutoForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import FinalizarCompraForm
from django.http import HttpResponse
from .models import *

def lista_produtos(request):
    categorias = Categoria.objects.all()
    
    if request.GET.get('categoria'):
        produtos = Produto.objects.filter(categoria=Categoria.objects.get(nome__iexact=request.GET['categoria']))
    else:
        produtos = Produto.objects.all()
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos, 'categorias': categorias})

def criar_produto(request):
    produtos=Produto.objects.all()
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return redirect('criar_produto')
        print(form.errors)
    else:
        form = ProdutoForm()
    print(form.errors)
    return render(request, 'produtos/criar_produto.html', {'form': form, 'produtos': produtos})

def editar_produto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('criar_produto')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/criar_produto.html', {'form': form})

def remover_produto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    produto.delete()
    return redirect('criar_produto')

def sobre(request):
    categorias = Categoria.objects.all()
    
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        if categoria_id:
            return redirect(f'/produtos/lista_produtos?categoria={categoria_id}')
    
    return render(request, 'produtos/sobre.html', {'categorias': categorias})
    
def pesquisa(request):
    categorias = Categoria.objects.all()
    query = request.GET.get('q', '')
    produtos = Produto.objects.filter(nome__icontains=query)
    
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        if categoria_id:
            return redirect(f'/produtos/lista_produtos?categoria={categoria_id}')
    
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos, 'categorias': categorias})

def carrinho(request):
    cliente = get_object_or_404(Cliente, id=request.user.id)
    carrinho = get_object_or_404(Carrinho, cliente=cliente)
    
    # Calcular o total do carrinho
    total = sum([item.preco * item.quantidade for item in carrinho.itens.all()])
    carrinho.total = total
    carrinho.save()

    return render(request, 'produtos/carrinho.html', {'carrinho': carrinho})

def remover_do_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    cliente = get_object_or_404(Cliente, username=request.user.username)
    carrinho = get_object_or_404(Carrinho, cliente=cliente)
    
    carrinho.itens.remove(produto)
    
    # Recalcular o total
    total = sum([item.preco * item.quantidade for item in carrinho.itens.all()])
    carrinho.total = total
    carrinho.save()

    return redirect('carrinho')

def adicionar_ao_carrinho(request, produto_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    produto = get_object_or_404(Produto, id=produto_id)
    cliente = get_object_or_404(Cliente, username=request.user.username)
    carrinho, created = Carrinho.objects.get_or_create(cliente=cliente)
    
    # Assuming you have a ManyToMany relationship with a through model for items in the cart
    carrinho.itens.add(produto)
    
    return redirect('lista_produtos')
    
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('lista_produtos')
            else:
                form.add_error(None, 'Senha ou usuário incorretos')
        else:
            form.add_error(None, 'Senha ou usuário incorretos')
    else:
        form = AuthenticationForm()
    return render(request, 'produtos/login.html', {'form': form})

def cadastro_cliente(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        endereco = request.POST.get('endereco')
        senha = request.POST.get('senha')
        
        cliente = Cliente.objects.create_user(username=usuario, email=email, telefone=telefone, endereco=endereco, password=senha)
        cliente.save()
        
        # Create a cart for the new client
        carrinho = Carrinho(cliente=cliente)
        carrinho.save()
        
        return redirect('login')
    
    return render(request, 'produtos/cadastro_cliente.html')

def Comprar(request, produto_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    produto = get_object_or_404(Produto, id=produto_id)
    cliente = get_object_or_404(Cliente, username=request.user.username)
    carrinho, created = Carrinho.objects.get_or_create(cliente=cliente)
    
    # Adiciona o produto ao carrinho
    carrinho.itens.add(produto)
    
    # Redireciona para a página do carrinho
    return redirect('carrinho')

def atualizar_quantidade_carrinho(request, produto_id):
    if request.method == 'POST':
        produto = get_object_or_404(Produto, id=produto_id)
        quantidade = int(request.POST['quantity'])
        cliente = get_object_or_404(Cliente, username=request.user.username)
        carrinho = get_object_or_404(Carrinho, cliente=cliente)
        
        # Atualizar a quantidade do item no carrinho
        produto.quantidade = quantidade
        produto.save()

        # Recalcular o total
        total = sum([item.preco * item.quantidade for item in carrinho.itens.all()])
        carrinho.total = total
        carrinho.save()

    return redirect('carrinho')

def finalizar_compra(request):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, username=request.user.username)
        carrinho = get_object_or_404(Carrinho, cliente=cliente)
        
        # Limpar o carrinho
        carrinho.itens.clear()
        carrinho.total = 0
        carrinho.save()

    return redirect('carrinho')

def finalizar_compra(request):
    cliente = request.user
    carrinho = cliente.get_carrinho()


    if request.method == 'POST':
        form = FinalizarCompraForm(request.POST)
        if form.is_valid():
            pedido = Pedido(
                cliente=cliente,
                carrinho=carrinho,
                metodo_pagamento=form.cleaned_data['metodo_pagamento'],
                endereco_entrega=form.cleaned_data['endereco_entrega'],
                nome_destinatario=form.cleaned_data['nome_destinatario'],
            )
            pedido.save()
            return redirect('pedido_concluido', pedido_id=pedido.id)
    else:
        form = FinalizarCompraForm()

    return render(request, 'produtos/finalizar_compra.html', {'form': form, 'carrinho': carrinho})

def pedido_concluido(request, pedido_id):
    try:
        pedido = Pedido.objects.get(id=pedido_id)
        print(pedido.data)  # Verifique se a data está sendo recuperada
    except Pedido.DoesNotExist:
        return HttpResponse("Pedido não encontrado.")
    return render(request, 'produtos/pedido_concluido.html', {'pedido': pedido})

