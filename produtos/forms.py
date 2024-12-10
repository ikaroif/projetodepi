from django import forms
from .models import Produto, Cliente

class FinalizarCompraForm(forms.Form):
    metodo_pagamento_choices = [
        ('cartao_credito', 'Cartão de Crédito'),
        ('boleto', 'Boleto'),
        ('pix', 'Pix'),
    ]
    
    metodo_pagamento = forms.ChoiceField(choices=metodo_pagamento_choices, widget=forms.RadioSelect)
    endereco_entrega = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite o endereço completo'}))
    nome_destinatario = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Nome da pessoa que receberá'}))

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'quantidade', 'imagem','carrinho', 'preco']

class LoginForm(forms.Form):
    usuario = forms.CharField(max_length=100, label='Usuário')
    senha = forms.CharField(max_length=15, widget=forms.PasswordInput, label='Senha')

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        senha = cleaned_data.get("senha")

        if usuario and senha:
            try:
                # Tenta encontrar o cliente com o usuário e a senha fornecidos
                cliente = Cliente.objects.get(usuario=usuario, senha=senha)
            except Cliente.DoesNotExist:
                raise forms.ValidationError("Usuário ou senha inválidos.")
        return cleaned_data