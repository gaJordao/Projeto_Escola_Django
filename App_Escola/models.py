from django.db import models

class Professor(models.Model):
    nome = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    senha = models.CharField(max_length=64)

    def __str__(self):
        return self.nome
    
class Turma(models.Model):
    nome_turma = models.CharField(max_length=120)
    id_professor = models.ForeignKey(Professor, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_turma
    
class Atividade(models.Model):
    nome_atividade = models.CharField(max_length=120)
    id_turma = models.ForeignKey(Turma, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_atividade