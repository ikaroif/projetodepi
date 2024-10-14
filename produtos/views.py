from django.shortcuts import render, redirect, get_object_or_404
from .models import Categoria, Produto
from .forms import ProdutoForm

def lista_produtos(request):
    categorias = Categoria.objects.all()
    
    if request.GET.get('categoria'):
        produtos = Produto.objects.filter(categoria=Categoria.objects.get(nome__iexact=request.GET['categoria']))
    else:
        produtos = Produto.objects.all()
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos, 'categorias': categorias})

def adicionar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/adicionar_produto.html', {'form': form})

def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar_produto.html', {'form': form})

def remover_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        produto.delete()
        return redirect('lista_produtos')
    return render(request, 'produtos/remover_produto.html', {'produto': produto})


def categoria(request, categoria_id):
    produtos = Produto.objects.filter(name=categoria_id)
    return render(request, 'produtos/categoria.html', {'produtos': produtos})

def sobre(request):
    return render(request, 'produtos/sobre.html')

def pesquisa(request):
    query = request.GET.get('q', '')
    produtos = Produto.objects.filter(nome__icontains=query)
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})
def carrinho(request):
    return render(request, 'produtos/carrinho.html')
def categoria_remedios(request):
    produtos = Produto.objects.filter(categoria='Remédios')
    return render(request, 'produtos/categoria_remedios.html', {'produtos': produtos})
def categoria_produtos_infantis(request):
    produtos = Produto.objects.filter(categoria='Produtos Infantis')
    return render(request, 'produtos/categoria_produtos_infantis.html', {'produtos': produtos})
def categoria_produtos_adultos(request):
    produtos = Produto.objects.filter(categoria='Produtos Adultos')
    return render(request, 'produtos/categoria_produtos_adultos.html', {'produtos': produtos})
def adicionar_ao_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return redirect('lista_produtos')  
