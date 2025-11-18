ARQUIVO_USUARIOS = "usuarios_feifood.txt"
ARQUIVO_PEDIDOS = "pedidos_feifood.txt"
ARQUIVO_ALIMENTOS = "alimentos_feifood.txt" 

# Bloco 2 funcoes de Gerenciamento BD

def ler_arquivo(nome_arquivo):
    """Esta função lê um arquivo de texto e o transforma em uma lista de listas. """
    try:
        # encoding=utf-8 garante que ç/á vai ser lido certo
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            # cria uma lista vazia para guardar os dados do arquivo.
            lista_dados = []
            for linha in f:
                # 'linha.strip()' remove os espaços e branco e quebras de linha
                linha_limpa = linha.strip()
                
                if linha_limpa:
                    # 'linha_limpa.split quebra a string usando virgula
                    lista_dados.append(linha_limpa.split(','))
            
            return lista_dados
    
    # 'except FileNotFoundError' é um tratamento de erro.
    # se o arquivo usuarios.txt não existir, ele não vai crashar o prog
    except FileNotFoundError:
        return []

def escrever_arquivo(nome_arquivo, lista_dados):
    """
    essa função faz o OPOSTO da 'ler_arquivo'.
    ela pega uma lista de listas e a escreve de volta no arquivo de texto.
    """
    

    # !! nao esquecer !! O modo 'w' APAGA TUDO que estava no arquivo antes.
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        
        
        for linha_lista in lista_dados:
            
            
            linha_str = ','.join(linha_lista)
            
            # Escreve a string no arquivo e add quebra de linha
            f.write(linha_str + '\n') 

# Bloco 3 Funções de Gerenciamento de Usuário 

def cadastrar_usuario():
    """REGISTRA NEW USER    """
    
    print("\n--- Cadastro de Novo Usuário ---")
    
    lista_de_usuarios = ler_arquivo(ARQUIVO_USUARIOS)
    
    #  while True vai garantir que o username seja único.
    while True:
        username = input("Digite um username único: ") 
        
        existe = False
        
        # verifica cada usuário na lista.
        for usuario in lista_de_usuarios:
            # usuario[0] é o username, primeiro item da lista
            if usuario[0].lower() == username.lower():
                existe = True # Aachou! 
                break 
        
        if existe:
            print("Erro: Esse username já existe. Tente outro.") 
        
        else:
            break 
    password = input("Digite uma senha: ")
    nome = input("Digite seu nome completo: ")
    
    # 2 edit os dados:
    # cria a lista do novo usuário.
    novo_usuario = [username, password, nome]
    # adiciona a lista do novo usuário à lista principal.
    lista_de_usuarios.append(novo_usuario)
    
    # 3 write os dados:
    # salva a lista principal com o novo usuário de volta no arquivo.
    escrever_arquivo(ARQUIVO_USUARIOS, lista_de_usuarios)
    print(f"Usuário {username} cadastrado com sucesso!")

def fazer_login():
    """
    Função para verificar se um usuário e senha existem.
    Se sim, retorna o nome de usuário. Se não, retorna 'None'.
    """
    print("\n--- Login de Usuário ---")
    
    # lista de users do txt
    lista_de_usuarios = ler_arquivo(ARQUIVO_USUARIOS)
    
    username = input("Username: ")
    password = input("Senha: ")

    for usuario in lista_de_usuarios:
        # user[0] é o username, user[1] é a senha.
        if usuario[0] == username and usuario[1] == password:
            # 'user[2]' é o nome ful.
            print(f"Login bem-sucedido! Bem-vindo, {usuario[2]}.")
            # login feito return nome do user
            return usuario[0] 
    
    #aviso falhaa de log
    print("Usuário ou senha inválidos.")
    return None

#  Bloco 4: functions de logica do app 

def buscar_alimento(lista_alimentos_fixa):
    """
    function para buscar e listar alimentos.
    """
    print("\n--- Buscar Alimentos ---")

    termo_busca = input("Digite o nome do alimento: ")
    # cri lista vazia para guardar os resultados da busca.
    encontrados = [] 
    
    for alimento in lista_alimentos_fixa:
        # 'alimento[1]' é o nome do alimento.
        if termo_busca.lower() in alimento[1].lower():
            # add o alimento nos resultados.
            encontrados.append(alimento) 

    if not encontrados: 
        print("Nenhum alimento encontrado com esse nome.")
    else:
        print("\n--- Alimentos Encontrados ---")
        for alim in encontrados:
            # formata os dados do alimento para exibição.
            print(f"ID: {alim[0]} | {alim[1]} | R$ {alim[2]} | (Restaurante: {alim[3]})")
        print("-" * 30)

def cadastrar_pedido(lista_alimentos_fixa, username_logado):
    """
    função para criar um novo pedido 
    """
    print("\n--- NOVO PEDIDO ---")
    #nao tem oq pedir
    if not lista_alimentos_fixa:
        print("Nenhum alimento disponível para pedido.")
        return 
        
    # carrega a lista de pedidos existentes (para sabermos qual o ID do próximo).
    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS)
    # novo carrio pra guardar os ids
    carrinho_ids = [] 
    
    # add no carrinho
    while True:
        print("\nItens disponíveis (digite o ID para adicionar):")
        # cardapio
        for alim in lista_alimentos_fixa:
            print(f"ID: {alim[0]} | {alim[1]} | R$ {alim[2]}")
        
        id_para_add = input("\nDigite o ID (ou '0' para fechar o pedido): ")
        
        #saida do loop
        if id_para_add == '0':
            break 
        
        # next= atalho para encontrar um item na lista.
        alimento_encontrado = next((a for a in lista_alimentos_fixa if a[0] == id_para_add), None)
        
        
        if alimento_encontrado:
            carrinho_ids.append(id_para_add) 
            print(f"-> '{alimento_encontrado[1]}' adicionado ao carrinho!")
        else:
            print("ID de alimento inválido.")

    # saida do loop e verify 1 item
    if len(carrinho_ids) > 0:
        # Define um novo ID para o pedido 
        novo_id_pedido = str(len(lista_pedidos) + 1)
        
        # junta a lista de IDs do carrinho em uma string únic.
        ids_alimentos_str = ";".join(carrinho_ids) 
        
        # novo pedido.
        novo_pedido = [novo_id_pedido, username_logado, ids_alimentos_str, "NA"]
        
        # add o novo pedido à lista principal de pedidos.
        lista_pedidos.append(novo_pedido) 
        # salva a lista atualizada de volta no arquivo.
        escrever_arquivo(ARQUIVO_PEDIDOS, lista_pedidos)
        print(f"\nPedido N° {novo_id_pedido} cadastrado com sucesso!")
    else:
        print("Nenhum item no carrinho. Pedido cancelado.")

def editar_pedido(lista_alimentos_fixa, username_logado):
    """
    Função para editar um pedido (adicionar/remover itens) que
    ainda não foi avaliado.
    """
    
    print("\n--- EDITAR PEDIDO ---")
    #1 read
    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS)
    
    #2 filtra
    # cria uma nova lista 'pedidos_editaveis' apenas com os pedidos que
    # p{3} NA
    pedidos_editaveis = [p for p in lista_pedidos if p[1] == username_logado and p[3] == "NA"]

    if not pedidos_editaveis:
        print("Você não tem pedidos pendentes (não avaliados) para editar.")
        return
    
    print("\nSeus pedidos editáveis:")
    for pedido in pedidos_editaveis:
        # so pra ficar mais bonito na tela
        print(f"ID: {pedido[0]} (Itens: {pedido[2].replace(';', ', ')})")
        
    id_para_editar = input("Digite o ID do pedido que deseja editar: ")
    
    # 3 encontra o indice
    # localizar a *posição* do pedido na lista_pedidos
    indice_pedido = -1. #invalido
    # 'enumerate' nos da o i e o pedido
    for i, pedido in enumerate(lista_pedidos):
        # ve se é o pedido
        if pedido[0] == id_para_editar and pedido[1] == username_logado and pedido[3] == "NA":
            indice_pedido = i # guarda o indice
            break 

    if indice_pedido == -1:
        print("ID do pedido inválido, não pertence a você ou já foi avaliado.")
        return

    #4 modifica
    pedido_encontrado = lista_pedidos[indice_pedido]
    
    # pega a string de itens do pedido e transforma em lista.
    lista_ids_atuais = pedido_encontrado[2].split(';')

    while True:
        print("\n--- Opções de Edição ---")
        print(f"Pedido N° {id_para_editar} | Itens Atuais: {', '.join(lista_ids_atuais)}")
        print("1. Adicionar Item")
        print("2. Remover Item")
        print("0. Finalizar Edição")
        
        opcao_edicao = input("Escolha uma opção: ")
        
        if opcao_edicao == '0':
            break 
        
        elif opcao_edicao == '1': # add
            print("\nItens disponíveis:")
            for alim in lista_alimentos_fixa:
                print(f"ID: {alim[0]} | {alim[1]}")
            
            id_para_add = input("Digite o ID do item para ADICIONAR: ")
            # checa na lista o alim
            alimento_existe = next((a for a in lista_alimentos_fixa if a[0] == id_para_add), None)
            
            if alimento_existe:
                lista_ids_atuais.append(id_para_add) # add na lista
                print(f"Item {id_para_add} adicionado.")
            else:
                print("ID de item inválido.")

        elif opcao_edicao == '2': # REMOVER
            id_para_remover = input("Digite o ID do item para REMOVER: ")
            
            if id_para_remover in lista_ids_atuais:
                lista_ids_atuais.remove(id_para_remover) # Remove da lista de itens.
                print(f"Item {id_para_remover} removido.")
            else:
                print("ID do item não encontrado no pedido.")
        
        else:
            print("Opção inválida.")
            
    #5 salva
    if lista_ids_atuais: # c a lista n tiver vazia
        # E atualiza o item na lista_pedidos
        lista_pedidos[indice_pedido][2] = ";".join(lista_ids_atuais)
        
        # salva a 'lista_pedidos modif
        escrever_arquivo(ARQUIVO_PEDIDOS, lista_pedidos)
        print(f"\nPedido N° {id_para_editar} atualizado com sucesso!")
    else:
        print("O carrinho ficou vazio. Use a opção 'Excluir Pedido' se for o caso.")
        
def avaliar_pedido(username_logado):
    """
    Função para dar uma nota (0-5) a um pedido NA.
    """
    print("\n--- AVALIAR PEDIDO ---")
    
    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS)
    
    #2 pega os pedidos NA
    pedidos_pendentes = [p for p in lista_pedidos if p[1] == username_logado and p[3] == "NA"]
            
    if not pedidos_pendentes:
        print("Você não tem pedidos pendentes de avaliação.")
        return 

    # e printa eles
    print("\nSeus pedidos pendentes de avaliação:")
    for pedido in pedidos_pendentes:
        print(f"ID: {pedido[0]} (Itens: {pedido[2].replace(';', ', ')})")
        
    id_para_avaliar = input("Digite o ID do pedido que deseja avaliar: ")
    
    # se att deu certo
    pedido_atualizado = False
    
    #3 encontra o indice
    # pra encontrar indice i
    for i in range(len(lista_pedidos)):
        
        # Cchecagem order certa.
        if (lista_pedidos[i][0] == id_para_avaliar and 
            lista_pedidos[i][1] == username_logado and
            lista_pedidos[i][3] == "NA"):
            
            while True:
                nota = input("Digite sua nota (0 a 5 estrelas): ")
                
                if nota in ['0', '1', '2', '3', '4', '5']:
                    
                    # 4 modify
                    # att no ultimo indice
                    lista_pedidos[i][3] = nota 
                    
                    # 5 save
                    escrever_arquivo(ARQUIVO_PEDIDOS, lista_pedidos) 
                    print("Pedido avaliado com sucesso!")
                    pedido_atualizado = True # avisa que deu certo.
                    break
                else:
                    print("Nota inválida. Digite um número de 0 a 5.")
            
            break 

    # se false id invalido
    if not pedido_atualizado:
        print("ID do pedido inválido, não pertence a você ou já foi avaliado.")

def excluir_pedido(username_logado):
    """
    Função para remover um pedido (qualquer pedido) do usuário.
    """
    print("\n--- EXCLUIR PEDIDO ---")

    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS) 
    
    #2 tds pedidos
    pedidos_do_usuario = [p for p in lista_pedidos if p[1] == username_logado]

    if not pedidos_do_usuario:
        print("Você não tem pedidos para excluir.")
        return

    # printa eles
    print("\nSeus pedidos registrados:")
    for pedido in pedidos_do_usuario:
        print(f"ID: {pedido[0]} (Itens: {pedido[2].replace(';', ', ')}) | Avaliação: {pedido[3]}")
    
    id_para_excluir = input("Digite o ID do pedido que deseja EXCLUIR: ")
    
    pedido_removido = False 
    
    #3 
    # achar o indicie i pra remover
    for i, pedido in enumerate(lista_pedidos):
        # verifica se eh do user e tem id certo
        if pedido[0] == id_para_excluir and pedido[1] == username_logado:
            
            confirmacao = input(f"Tem certeza que deseja excluir o pedido {id_para_excluir}? (s/n): ").lower()
            
            if confirmacao == 's':
                lista_pedidos.pop(i) 
                
                #salva d novo
                escrever_arquivo(ARQUIVO_PEDIDOS, lista_pedidos) 
                print(f"Pedido N° {id_para_excluir} excluído com sucesso!")
                pedido_removido = True
            else:
                print("Exclusão cancelada.")
                pedido_removido = True 
            
            break 

    if not pedido_removido:
        print("ID do pedido inválido ou não pertence a você.")

def sair():
    """Função simples para encerrar o programa."""
    print("Obrigado por usar o FEIFood. Até logo!")
    exit() 

# bloco 5 principal funcao

def main():
    """
    Esta é a função principal que controla o fluxo do programa.
    Ela decide qual menu mostrar e qual função chamar.
    """
    
    # carrega o cardápio na memoria
    alimentos = ler_arquivo(ARQUIVO_ALIMENTOS)
    
    # estado none= ngm logado
    usuario_logado = None 
    
    # def dos menus.
    menu_deslogado = {"1": "Fazer Login", "2": "Cadastrar Novo Usuário", "0": "Sair do Programa"}
    menu_logado = {
        "3": "Buscar por alimento", 
        "4": "Cadastrar novo pedido", 
        "5": "Avaliar um pedido",
        "6": "Excluir Pedido", 
        "7": "Editar Pedido",
        "9": "Fazer Logoff", 
        "0": "Sair do Programa"
    }

    # O loop principal do programa fica rodando até o usuário digitar 0
    while True:
        print("\n" + "=" * 25)
        print("--- BEM-VINDO AO FEIFOOD ---")
        print("=" * 25)
        
        # decide qual menu mostrar.
        menu_atual = menu_deslogado # starta deslogado
        
        # isnt none checa se tem user logado
        if usuario_logado is not None:
            menu_atual = menu_logado # se tive troca para o menu de logado.
            print(f"Logado como: {usuario_logado}\n") 
        else:
            print("Você está deslogado.\n")
        
        # imprime menu
        for key, value in menu_atual.items():
            print(f"{key}. {value}")
            
        opcao = input("\nEscolha uma opção: ")

        # chama funcoes
        
        if opcao == "1" and usuario_logado is None:
            # chama 'fazer_login e salva o user ou none
            usuario_logado = fazer_login()
        
        elif opcao == "2" and usuario_logado is None:
            cadastrar_usuario() 
        
        elif opcao == "3" and usuario_logado is not None:
            buscar_alimento(alimentos)
        
        elif opcao == "4" and usuario_logado is not None:
            # passa a lista de alimentos e o nome do usuário logado.
            cadastrar_pedido(alimentos, usuario_logado)
        
        elif opcao == "5" and usuario_logado is not None:
            avaliar_pedido(usuario_logado)
        
        elif opcao == "6" and usuario_logado is not None:
            excluir_pedido(usuario_logado)
        
        elif opcao == "7" and usuario_logado is not None:
            editar_pedido(alimentos, usuario_logado)

        elif opcao == "9" and usuario_logado is not None:
            usuario_logado = None
            print("Logoff realizado com sucesso.")

        elif opcao == "0":
            sair() 

        else:
            print("Opção inválida ou não permitida.")

# ponto de entrada
if __name__ == "__main__":
    main()