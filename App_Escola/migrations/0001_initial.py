# Generated by Django 5.0.3 on 2024-03-20 13:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=120)),
                ('email', models.CharField(max_length=120)),
                ('senha', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_turma', models.CharField(max_length=120)),
                ('id_professor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='App_Escola.professor')),
            ],
        ),
    ]
