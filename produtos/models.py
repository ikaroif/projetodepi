from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    senha = models.CharField(max_length=15)
    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome
    

    
class Carrinho(models.Model):
    cliente = models.OneToOneField(Cliente,on_delete=models.CASCADE)
    data_criacao = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()

    def __str__(self):
        return f"Carrinho de {self.cliente.nome}"

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.FloatField()
    imagem = models.ImageField(upload_to='produtos/')
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE, null=True)
    quantidade = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.nome