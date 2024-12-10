from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('cadastro_cliente/', views.cadastro_cliente, name='cadastro_cliente'),
    path('sobre/', views.sobre, name='sobre'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('login/', views.login, name='login'),
    path('adicionar-carrinho/<int:produto_id>', views.adicionar_ao_carrinho, name='adicionar_carrinho'),
    path('remover-do-carrinho/<int:produto_id>', views.remover_do_carrinho, name='remover_do_carrinho'),
    path('criar_produto', views.criar_produto, name='criar_produto'),
    path('editar_produto/<int:produto_id>', views.editar_produto, name='editar_produto'),
    path('remover_produto/<int:produto_id>', views.remover_produto, name='remover_produto'),
    path('Comptar/<int:produto_id>', views.Comprar, name='Comprar'),
    path('atualizar_quantidade_carrinho/<int:produto_id>', views.atualizar_quantidade_carrinho, name='atualizar_quantidade_carrinho'),
    path('finalizar_compra/', views.finalizar_compra, name='finalizar_compra'),
    path('pedido_concluido/<int:pedido_id>/',views.pedido_concluido, name='pedido_concluido'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

