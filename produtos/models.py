from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import random
import string
from django.db import models
from django.utils import timezone


class CustomManager(UserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        if not username:
            raise ValueError('O nome de usuário é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Cliente(AbstractUser):
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomManager()

    def __str__(self):
        return self.username
    
    def get_carrinho(self):
        return Carrinho.objects.get(cliente=self)



class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    
  
class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    def __str__(self):
        return f"Carrinho de {self.cliente.username}"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.FloatField()
    imagem = models.ImageField(upload_to='produtos/')
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, null=True, related_name='itens')
    quantidade = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome

class Login(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    ultimo_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Login de {self.cliente.nome} em {self.ultimo_login}"

    def get_carrinho(self):
        return Carrinho.objects.get(cliente=self.cliente)
        
def gerar_chave_aleatoria(tamanho=8):
    """Gera uma chave aleatória de tamanho especificado"""
    caracteres = string.ascii_letters + string.digits
    chave = ''.join(random.choice(caracteres) for _ in range(tamanho))
    return chave

class Pedido(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    carrinho = models.ForeignKey('Carrinho', on_delete=models.CASCADE)
    metodo_pagamento = models.CharField(max_length=255)
    endereco_entrega = models.CharField(max_length=255)
    nome_destinatario = models.CharField(max_length=255)
    chave_pacote = models.CharField(max_length=8, blank=True, null=True)
    data = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.chave_pacote:
            self.chave_pacote = gerar_chave_aleatoria()
        super().save(*args, **kwargs)

