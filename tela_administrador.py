import sqlite3

# Cria uma conexão com o banco de dados
conexao_db = sqlite3.connect('cyber_solucoes.db')

# Cria um cursor para executar comandos SQL
cursor = conexao_db.cursor()

# ***** ADMINISTRADOR  *****

def cadastrar_administrador():
    global id_usuario

    print( " (1) login            (2) Criar conta")
    print('='*20)
    entrada = input("escolha:")

    while( entrada!= '1' and entrada!='2' ):
        entrada = input("Escolha a alternativa correta:")

    while True:
        if (entrada =='1'):
            email = input("Digite seu email:")
            cursor.execute(f" SELECT * FROM administrador WHERE email_administrador = ? ",(email,))
            resposta = cursor.fetchone()
            if resposta:  
                print("usuario autentificado!")
                id_usuario = resposta[0]
                break  
            else:
                print(resposta)
                print("usuario não encontrado")

        elif entrada == '2':
            nome = input("Digite seu nome:")
            cpf = input("digite o seu CPF:")
            email = input("digite o seu email:")
            telefone = input("digite o seu telefone:")
            cursor.execute(" INSERT INTO administrador (nome_administrador,cpf_administrador,email_administrador,telefone_administrador) values (?,?,?,?)",(nome,cpf,email,telefone))
            id_usuario = cursor.lastrowid
            conexao_db.commit()
            break

def editar_administrador():
    item = input("[1]nome\n[2]email\n[3]telefone\n O que deseja mudar:")
    mudar = input('para que dejesa mudar:')
    dicionario = {'1':'nome_administrador','2':'email_administrador','3':'telefone_administrador'}
    cursor.execute(f'UPDATE administrador SET {dicionario[item]} =? where id_administrador=?',(mudar,id_usuario))
    conexao_db.commit()


# **** MODIFICAÇÕES *****

# Insere os valores em modificação ( Como se fosse um histórico do adminstrador )
def modificacoes_administrador(servico,administrador,nome):
    cursor.execute(f"INSERT INTO modificacoes VALUES( NULL,?,?,?)",(servico,administrador,nome))

# Lista modificação
def listar_modificacao_administrador():
    cursor.execute(""" SELECT id_modificacao,nome_administrador,email_administrador,nome_modificacoes FROM modificacoes 
                INNER JOIN administradores on fk_id_administrador = id_administrador 
                INNER JOIN servicos on fk_id_servico = id_servico """)
    resultados = cursor.fetchall()
    
    print(f"|{'ID':<3}|{'Nome ':<20}|{'Email do administrador':<30}|{'Modificação':<20}|")
    print('-'*70)
    for resultado in resultados:
        modificacao = list(resultado)
        print(f"|{modificacao[0]:<3}|{modificacao[1]:<20}|{modificacao[2]:<30}|{modificacao[3]:<20}|")

# ***** SERVIÇOS *****

def cadastrar_servico_administrador():
    nome_servico = input("Digite o nome do serviço:")
    tipo_servico = input("Digite o tipo do serviço:")

    cursor.execute(" INSERT INTO servico VALUES (NULL,?, ?)",(nome_servico,tipo_servico))
    id_servico = cursor.lastrowid
    modificacoes_administrador(id_servico, id_usuario,'cadastrou serviço')
    conexao_db.commit()

def editar_servico_administrador():
    id_servico = input("digite o id do serviço:")
    print('[1] nome\n[2] tipo')
    atributo = input("Qual atributo você dejesa editar:")
    troca = input("Qual dejesa colocar:")
    dicionario = {'1':'nome_servico','2':'tipo_servico'}

    cursor.execute(f" UPDATE servicos SET {dicionario[atributo]}=? WHERE id_servico = ?", (troca,id_servico))
    modificacoes_administrador(id_servico,id_usuario,'editou serviço')

    print("ESSE SERVIÇO FOI EDITADO !")
    conexao_db.commit()

def excluir_servico_administrador():
    id_servico = input("Digite o id do serviço:")

    cursor.execute(" DELETE FROM servicos WHERE id_servico = ?",(id_servico))
    print('-'*50)
    print(' ESSE SERVIÇO FOI DELETADO')
    conexao_db.commit()

# obter os valores de serviços
def obter_servico_administrador():
    cursor.execute(""" SELECT * FROM servicos """)

    resultados = cursor.fetchall()
    servicos = []
    for resultado in resultados:
        servico = list(resultado)
        servicos.append(servico)
    return servicos

def visualizar_servico_administrador():
    ver_servico = obter_servico_administrador()

    print(f"|{'ID':<3}|{'nome do serviço':<20}|{'tipo de serviço':<20}|")
    print('-'*43)

    for servico in ver_servico:
        print(f"|{servico[0]:<3}|{servico[1]:<20}|{servico[2]:<20}|")


# ***** SOLICITAÇÃO *****

# Obter os valores da tabela solicitação
def obter_solicitacao_administrador():
    cursor.execute(""" SELECT id_solicitacao,nome_cliente,email_cliente,nome_servico,tipo_servico,endereco_solicitacao FROM solicitacao
                    INNER JOIN servicos on id_servico = fk_id_servico
                    INNER JOIN clientes on id_cliente = fk_id_cliente  """)
    
    resultados = cursor.fetchall()
    
    for resultado in resultados:
        solicitacoes = []
        #transforma a tupla em uma lista
        solicitacao = list(resultado)
        #agrupa listas
        solicitacoes.append(solicitacao)
        return solicitacoes

# Função para visualizar os valores 
def visualizar_solicitacoes_administrador():
    ver_solicitacao = obter_servico_administrador()
    print(ver_solicitacao)
    
    print(f"| {'ID':<3} | {'cliente':<20} | {'email':<20} | {'serviço':<20} |{'tipo de serviço':<20} |{'local':<20} |")
    print('='* 130)
    for solicitacao in ver_solicitacao:
        
        print(f"| {solicitacao[0]:<3} | {solicitacao[1]:<20} | {solicitacao[2]:<20} | {solicitacao[3]:<20} |{solicitacao[4]:<20} |{solicitacao[5]:<20} |")


        
# *********** RANK *************

def rank():
    while True:
        print(""" ****************************************************
        __________________ OPÇÕES __________________

        [v] .............. Voltar 
        [1] .............. SERVIÇO
        [2] .............. LOCAL"""
        )
        escolha = input("Escolha:")

        if( escolha =='1'):
            rank_soliciação_servico()
        elif(escolha =='2'):
            rank_soliciação_local()

def rank_soliciação_servico():
    cursor.execute(""" SELECT nome_servico, COUNT(id_solicitacao)  AS quandidade_soliciacoes FROM solicitacao
                    INNER JOIN servico on id_servico = fk_id_servico
                    GROUP BY nome_servico
                    ORDER BY nome_servico DESC""")

    resultados = cursor.fetchall()
    print(f"|{'serviço':<20}|{'Quantidade de solicitações':<30}|")
    print('-'*50)
    for resultado in resultados:
        servico = list(resultado)
        print(f'|{servico[0]:<20}|{servico[1]:<30}|')

def rank_soliciação_local():
    cursor.execute(""" SELECT endereco_solicitacao, COUNT(id_solicitacao)  AS quandidade_soliciacoes FROM solicitacao
                    INNER JOIN servicos on id_servico = fk_id_servico
                    GROUP BY endereco_solicitacao
                    ORDER BY endereco_solicitacao DESC""")

    resultados = cursor.fetchall()
    print(f"|{'local':<20}|{'Quantidade de solicitações':<30}|")
    print('-'*50)
    for resultado in resultados:
        servico = list(resultado)
        print(f'|{servico[0]:<20}|{servico[1]:<30}|')

def menu_administrador():
    cadastrar_administrador()

    """
    - Função para exibir o menu principal do arquivo, que possui opções de : [v] Voltar ao menu principal, [1] , [2] , [3] ;
    - Não recebe parâmetros;
    - Exemplo de uso:
    >>> menu_administrador():
    """
    while True:
        opcao = input("""
****************************************************
    __________________ OPÇÕES __________________

    [v] .............. Voltar ao menu principal
    [1] .............. Visualizar solicitações
    [2] .............. Visualizar serviços
    [3] .............. Criar serviço
    [4] .............. Editar serviço
    [5] .............. Deletar serviço
    [6] .............. Ver histórico     
    [7] .............. Modificar cadastro  
    [8] .............. Ver rank                  
****************************************************

>>> Digite a opção: """)
        if opcao == 'v':
            print('\n - VOLTANDO AO MENU PRINCIPAL!!! - \n')
            break
        elif opcao == '1':
            print('\n - VISUALIZAR SOLICITAÇÕES - \n')
            visualizar_solicitacoes_administrador()
        elif opcao == '2':
            print('\n - VISUALIZAR SERVIÇOS - \n')
            visualizar_servico_administrador()
        elif opcao == '3':
            print('\n - CRIAR SERVIÇO - \n')
            cadastrar_servico_administrador(id_usuario)
        elif opcao == '4':
            print('\n - EDITAR SERVIÇO - \n')
            editar_servico_administrador()
        elif opcao == '5':
            print('\n - DELETAR SERVIÇO - \n')
            excluir_servico_administrador()
        elif opcao == '6':
            print('\n - VISUALIZAR HISTÓRICO - \n')
            ...
        elif opcao == '7':
            print('\n - MODIFICAR PERFIL - \n')
            editar_administrador()
        elif opcao == '8':
            rank()
        else:
            print('\n - OPÇÃO INVÁLIDA!!! - \n')

if __name__ == '__main__':
    menu_administrador()