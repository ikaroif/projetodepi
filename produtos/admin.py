from django.contrib import admin
from .models import Produto, Cliente, Categoria, Carrinho

admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Carrinho)
