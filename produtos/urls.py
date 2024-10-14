from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('adicionar/', views.adicionar_produto, name='adicionar_produto'),
    path('editar/<int:id>/', views.editar_produto, name='editar_produto'),
    path('remover/<int:id>/', views.remover_produto, name='remover_produto'),
    path('categoria/', views.categoria, name='categoria'),
    path('sobre/', views.sobre, name='sobre'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('remedios/', views.categoria_remedios, name='categoria_remedios'),
    path('produtos-infantis/', views.categoria_produtos_infantis, name='categoria_produtos_infantis'),
    path('produtos-adultos/', views.categoria_produtos_adultos, name='categoria_produtos_adultos'),
    path('categoria/remedios/', views.categoria_remedios, name='categoria_remedios'),
    path('categoria/produtos-infantis/', views.categoria_produtos_infantis, name='categoria_produtos_infantis'),
    path('categoria/produtos-adultos/', views.categoria_produtos_adultos, name='categoria_produtos_adultos'),
    path('adicionar-ao-carrinho/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
]

