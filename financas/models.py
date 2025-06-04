from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Conta(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Conta de {self.user.username} - Saldo: R$ {self.saldo}"

# Cria automaticamente a conta quando um usuário é criado
@receiver(post_save, sender=User)
def criar_conta_usuario(sender, instance, created, **kwargs):
    if created:
        Conta.objects.create(user=instance)


class Lucro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # só se for criação (não atualização)
            super().save(*args, **kwargs)
            conta = Conta.objects.get(user=self.user)
            conta.saldo += self.valor
            conta.save()
        else:
            super().save(*args, **kwargs)

class Despesa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # só se for criação (não atualização)
            super().save(*args, **kwargs)
            conta = Conta.objects.get(user=self.user)
            conta.saldo -= self.valor
            conta.save()
        else:
            super().save(*args, **kwargs)

class Objetivo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    valor_meta = models.DecimalField(max_digits=10, decimal_places=2)
    valor_atual = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.nome} - R$ {self.valor_atual} / {self.valor_meta}"

