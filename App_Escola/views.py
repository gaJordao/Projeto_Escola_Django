from django.shortcuts import redirect, render
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect

def initial_population():
    print("Vou Popular")

    cursor = connection.cursor()

    senha = '123456'
    senha_armazenar = sha256(senha.encode()).hexdigest()
    insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES "
    insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '"+senha_armazenar+"'),"
    insert_sql_professor = insert_sql_professor + "('Profa. Angela Merkel', 'angela.merkel@gmail.com', '"+senha_armazenar+"'),"
    insert_sql_professor = insert_sql_professor + "('Prof Xi Jiping', 'xi.jiping@gmail.com','"+senha_armazenar+"')"

    cursor.execute(insert_sql_professor)
    transaction.atomic()

    insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES "
    insert_sql_turma = insert_sql_turma + "('1o Semestre - Desenvolvimento de Sistemas', 1),"
    insert_sql_turma  = insert_sql_turma + "('2o Semestre - Desenvolvimento de Sistemas', 2),"
    insert_sql_turma = insert_sql_turma + "('3o Semestre - Desenvolvimento de Sistemas', 3)"

    cursor.execute(insert_sql_turma)


    insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos de Programação', 1),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar FrameWork Django', 2),"
    insert_sql_atividade = insert_sql_atividade + "('Apresentar conceitos de Gerenciamento de Projeto', 3)"

    cursor.execute(insert_sql_atividade)
    transaction.atomic()

    print("Populei")

def abre_index(request):
    # return render(request, 'login.html')
    dados_pesquisa = "Obama"

    verifica_populado = Professor.objects.filter(nome__icontains=dados_pesquisa)

    if len(verifica_populado) == 0:
        print("Não está Populado")
        initial_population()
    else:
        print("Achei Obama ", verifica_populado)
    
    return render(request, "login.html")

def enviar_login(request):
    
    if (request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome", "senha", "id")
        print("Dados do Professor ", dados_professor)

        if dados_professor:
            senha = dados_professor[0]
            senha = senha['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            if (senha == senha_criptografada):
                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
                print("Turma do professor ", turmas_do_professor)
                return render(request, "Cons_Turma_Lista.html", {
                    "usuario_logado": usuario_logado, 
                    "turmas_do_professor": turmas_do_professor,
                    "id_logado": id_logado,
                })
            
            else:
                messages.info(request, 'Usuário ou senha incorretos. Tente Novamente.')
                return render(request, 'login.html')

        messages.info(request, "Olá "+email+" seja bem-vindo! Percebemos que você é novo por aqui. Complete o seu cadastro.")
        return render(request, 'cadastro.html', {'login': email})


def abre_cadastro(request):
    if (request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('login')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()

        gravar_professor = Professor(
            nome=nome,
            email=email,
            senha=senha_criptografada
        )

        gravar_professor.save()

        mensagem = "OLÁ PROFESSOR "+ nome + ", SEJA BEM VINDO!"
        return render(request, "Cons_Turma_Lista.html")
    
def cad_turma(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome", "id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']

    return render(request, 'Cad_Turma.html', {
        'usuario_logado': usuario_logado, 
        "id_logado": id_professor
    })

def salvar_turma_nova(request):
    if (request.method =='POST'):
        nome_turma = request.POST.get('nome_turma')
        id_professor = request.POST.get('id_professor')

        professor = Professor.objects.get(id=id_professor)

        grava_turma = Turma(
            nome_turma=nome_turma,
            id_professor=professor
        )
        grava_turma.save()
        messages.info(request, 'Turma '+nome_turma+' cadastrado com sucesso.')

        dados_professor = Professor.objects.filter(id=id_professor).values("nome", "id")
        usuario_logado = dados_professor[0]
        usuario_logado = usuario_logado['nome']
        id_logado = dados_professor[0]
        id_logado = id_logado['id']
        turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
        return render(request, 'Cons_Turma_Lista.html', {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor, 'id_logado': id_logado})
    

def ver_atividades(request, id_turma):
    turma_logado = Turma.objects.filter(id=id_turma).values("nome_turma", "id")
    turma_logado = turma_logado[0]
    turma_logado = turma_logado['nome_turma']

    return render(request, 'Cad_Atividade.html', {
        'turma_logado': turma_logado, 
        "id_turma": id_turma
    })

def salvar_atividade_nova(request):
    if (request.method =='POST'):
        nome_atividade = request.POST.get('nome_atividade')
        id_turma = request.POST.get('id_turma')

        turma = Turma.objects.get(id=id_turma)

        grava_atividade = Atividade(
            nome_atividade=nome_atividade,
            id_turma=turma
        )
        grava_atividade.save()
        messages.info(request, 'Atividade '+nome_atividade+' cadastrado com sucesso.')

        # dados_turma = Turma.objects.filter(id=id_turma).values("nome_turma", "id")
        # turma_logado = dados_turma[0]
        # id_logado = turma_logado['id']
        # atividades_da_turma = Turma.objects.filter(id=id_logado)
        # turma_nome = dados_turma[0]['nome_turma']


        atividades = Atividade.objects.filter(id_turma=id_turma)
        turma = Turma.objects.get(id=id_turma)
        context = {
            'turma': turma,
            'atividades': atividades,
         }
        for atividade in atividades:
            print (atividade.nome_atividade)
            print('fudeu')
        return render(request, 'Mostrar_Atividades.html', context)
    

def delete_turma(request, pk):
    if request.method == 'POST':
        turma = Turma.objects.get(id=pk)
        turma.delete()
        return redirect('cad_turma', turma.id_professor.id)



