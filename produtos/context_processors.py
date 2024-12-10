from django.shortcuts import get_object_or_404
from produtos.models import Cliente, Carrinho
from django.http import Http404

def itens_carrinho(request):
    if request.user.is_authenticated:
        try:
            
            cliente = get_object_or_404(Cliente, id=request.user.id)
            carrinho = get_object_or_404(Carrinho, cliente=cliente)
            itens = carrinho.itens.all()  # Assuming you have a related name 'itens' in your Carrinho model
            itens_count = itens.count()
        except Http404:
            itens_count = 0
    else:
        itens_count = 0

    return {
        'numeros_de_itens': itens_count
    }