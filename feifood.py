
# --- BLOC0 1: CONFIGURAÇÃO E FERRAMENTAS DE ARQUIVO ---
# Nomes dos arquivos de dados
ARQUIVO_USUARIOS = "usuarios_feifood.txt"
ARQUIVO_PEDIDOS = "pedidos_feifood.txt"
ARQUIVO_ALIMENTOS = "alimentos_feifood.txt" 

def ler_arquivo(nome_arquivo):
    """Função Genérica para LER um arquivo, transformando-o em uma lista de listas."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            lista_dados = []
            for linha in f:
                linha_limpa = linha.strip()
                if linha_limpa:
                    lista_dados.append(linha_limpa.split(','))
            return lista_dados
    except FileNotFoundError:
        return []

def escrever_arquivo(nome_arquivo, lista_dados):
    """Função Genérica para ESCREVER (salvar) dados no arquivo, sobrescrevendo ('w')."""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for linha_lista in lista_dados:
            linha_str = ','.join(linha_lista)
            f.write(linha_str + '\n') 

# --- BLOC0 2: FUNÇÕES DE NEGÓCIO DO FEIFOOD (CRUD) ---
# As funções cadastrar_usuario, fazer_login, buscar_alimento permanecem nao mudadas

def cadastrar_usuario():
    #IMPLEMENTA: Cadastrar novo usuário 
    print("\n--- Cadastro de Novo Usuário ---")
    
    lista_de_usuarios = ler_arquivo(ARQUIVO_USUARIOS)
    
    while True:
        username = input("Digite um username único: ") 
        existe = False
        for usuario in lista_de_usuarios:
            if usuario[0].lower() == username.lower():
                existe = True
                break
        
        if existe:
            print("Erro: Esse username já existe. Tente outro.") 
        else:
            break
            
    password = input("Digite uma senha: ")
    nome = input("Digite seu nome completo: ")
    
    novo_usuario = [username, password, nome]
    lista_de_usuarios.append(novo_usuario)
    
    escrever_arquivo(ARQUIVO_USUARIOS, lista_de_usuarios)
    print(f"Usuário {username} cadastrado com sucesso!")

def fazer_login():
    #IMPLEMENTA: Login de usuário (
    print("\n--- Login de Usuário ---")
    
    lista_de_usuarios = ler_arquivo(ARQUIVO_USUARIOS)
    
    username = input("Username: ")
    password = input("Senha: ")

    for usuario in lista_de_usuarios:
        if usuario[0] == username and usuario[1] == password:
            print(f"Login bem-sucedido! Bem-vindo, {usuario[2]}.")
            return usuario[0] 
    
    print("Usuário ou senha inválidos.")
    return None

def buscar_alimento(lista_alimentos_fixa):
    #IMPLEMENTA: Buscar/Listar alimentos 
    print("\n--- Buscar Alimentos ---")

    termo_busca = input("Digite o nome do alimento: ")
    encontrados = [] 
    
    for alimento in lista_alimentos_fixa:
        if termo_busca.lower() in alimento[1].lower():
            encontrados.append(alimento) 
            
    if not encontrados: 
        print("Nenhum alimento encontrado com esse nome.")
    else:
        print("\n--- Alimentos Encontrados ---")
        for alim in encontrados:
            print(f"ID: {alim[0]} | {alim[1]} | R$ {alim[2]} | (Restaurante: {alim[3]})")
        print("-" * 30)

def cadastrar_pedido(lista_alimentos_fixa, username_logado):
    #IMPLEMENTA: Cadastrar pedido (
    print("\n--- NOVO PEDIDO ---")
    
    if not lista_alimentos_fixa:
        print("Nenhum alimento disponível para pedido.")
        return
        
    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS)
    carrinho_ids = [] 
    
    while True:
        print("\nItens disponíveis (digite o ID para adicionar):")
        for alim in lista_alimentos_fixa:
            print(f"ID: {alim[0]} | {alim[1]} | R$ {alim[2]}")
        
        id_para_add = input("\nDigite o ID (ou '0' para fechar o pedido): ")
        
        if id_para_add == '0':
            break
        
        alimento_encontrado = next((a for a in lista_alimentos_fixa if a[0] == id_para_add), None)
        
        if alimento_encontrado:
            carrinho_ids.append(id_para_add) 
            print(f"-> '{alimento_encontrado[1]}' adicionado ao carrinho!")
        else:
            print("ID de alimento inválido.")

    if len(carrinho_ids) > 0:
        novo_id_pedido = str(len(lista_pedidos) + 1)
        ids_alimentos_str = ";".join(carrinho_ids) 
        
        novo_pedido = [novo_id_pedido, username_logado, ids_alimentos_str, "NA"]
        
        lista_pedidos.append(novo_pedido) 
        escrever_arquivo(ARQUIVO_PEDIDOS, lista_pedidos)
        print(f"\nPedido N° {novo_id_pedido} cadastrado com sucesso!")
    else:
        print("Nenhum item no carrinho. Pedido cancelado.")

def editar_pedido(lista_alimentos_fixa, username_logado):
    
    #IMPLEMENTA: Editar Pedido (U - Update).
    #Permite adicionar ou remover itens de um pedido existente, desde que não esteja avaliado.
    
    print("\n--- EDITAR PEDIDO ---")
    
    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS)
    pedidos_editaveis = [p for p in lista_pedidos if p[1] == username_logado and p[3] == "NA"]

    if not pedidos_editaveis:
        print("Você não tem pedidos pendentes (não avaliados) para editar.")
        return
    
    print("\nSeus pedidos editáveis:")
    for pedido in pedidos_editaveis:
        print(f"ID: {pedido[0]} (Itens: {pedido[2].replace(';', ', ')})")
        
    id_para_editar = input("Digite o ID do pedido que deseja editar: ")
    
    indice_pedido = -1
    for i, pedido in enumerate(lista_pedidos):
        # Encontra o pedido pelo ID, username E se não foi avaliado
        if pedido[0] == id_para_editar and pedido[1] == username_logado and pedido[3] == "NA":
            indice_pedido = i
            break
            
    if indice_pedido == -1:
        print("ID do pedido inválido, não pertence a você ou já foi avaliado.")
        return

    # O pedido está na lista_pedidos[indice_pedido]
    pedido_encontrado = lista_pedidos[indice_pedido]
    
    # Transforma a string de IDs em uma lista (para manipulação)
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
        
        elif opcao_edicao == '1': # ADICIONAR ITEM
            print("\nItens disponíveis:")
            for alim in lista_alimentos_fixa:
                print(f"ID: {alim[0]} | {alim[1]}")
            
            id_para_add = input("Digite o ID do item para ADICIONAR: ")
            alimento_existe = next((a for a in lista_alimentos_fixa if a[0] == id_para_add), None)
            
            if alimento_existe:
                lista_ids_atuais.append(id_para_add)
                print(f"Item {id_para_add} adicionado. (Não se preocupe com duplicatas agora).")
            else:
                print("ID de item inválido.")

        elif opcao_edicao == '2': # REMOVER ITEM
            id_para_remover = input("Digite o ID do item para REMOVER: ")
            
            if id_para_remover in lista_ids_atuais:
                # Remove apenas a primeira ocorrência do item
                lista_ids_atuais.remove(id_para_remover)
                print(f"Item {id_para_remover} removido.")
            else:
                print("ID do item não encontrado no pedido.")
        
        else:
            print("Opção inválida.")
            
    # 3. Finalização e Salvamento
    if lista_ids_atuais:
        # Atualiza o campo de itens do pedido na lista principal
        lista_pedidos[indice_pedido][2] = ";".join(lista_ids_atuais)
        escrever_arquivo(ARQUIVO_PEDIDOS, lista_pedidos)
        print(f"\nPedido N° {id_para_editar} atualizado com sucesso!")
    else:
        print("O carrinho ficou vazio. Use a opção 'Excluir Pedido' se for o caso.")
        
def avaliar_pedido(username_logado):
    #IMPLEMENTA: Avaliar pedido 
    print("\n--- AVALIAR PEDIDO ---")
    
    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS)
    
    pedidos_pendentes = [p for p in lista_pedidos if p[1] == username_logado and p[3] == "NA"]
            
    if not pedidos_pendentes:
        print("Você não tem pedidos pendentes de avaliação.")
        return 

    print("\nSeus pedidos pendentes de avaliação:")
    for pedido in pedidos_pendentes:
        print(f"ID: {pedido[0]} (Itens: {pedido[2].replace(';', ', ')})")
        
    id_para_avaliar = input("Digite o ID do pedido que deseja avaliar: ")
    
    pedido_atualizado = False
    
    for i in range(len(lista_pedidos)):
        
        if (lista_pedidos[i][0] == id_para_avaliar and 
            lista_pedidos[i][1] == username_logado and
            lista_pedidos[i][3] == "NA"):
            
            while True:
                nota = input("Digite sua nota (0 a 5 estrelas): ")
                
                if nota in ['0', '1', '2', '3', '4', '5']:
                    lista_pedidos[i][3] = nota 
                    
                    escrever_arquivo(ARQUIVO_PEDIDOS, lista_pedidos) 
                    print("Pedido avaliado com sucesso!")
                    pedido_atualizado = True
                    break
                else:
                    print("Nota inválida. Digite um número de 0 a 5.")
            
            break

    if not pedido_atualizado:
        print("ID do pedido inválido, não pertence a você ou já foi avaliado.")

def excluir_pedido(username_logado):
    #IMPLEMENTA: Excluir pedido 
    print("\n--- EXCLUIR PEDIDO ---")

    lista_pedidos = ler_arquivo(ARQUIVO_PEDIDOS) 
    
    pedidos_do_usuario = [p for p in lista_pedidos if p[1] == username_logado]

    if not pedidos_do_usuario:
        print("Você não tem pedidos para excluir.")
        return

    print("\nSeus pedidos registrados:")
    for pedido in pedidos_do_usuario:
        print(f"ID: {pedido[0]} (Itens: {pedido[2].replace(';', ', ')}) | Avaliação: {pedido[3]}")
    
    id_para_excluir = input("Digite o ID do pedido que deseja EXCLUIR: ")
    
    pedido_removido = False
    
    for i, pedido in enumerate(lista_pedidos):
        if pedido[0] == id_para_excluir and pedido[1] == username_logado:
            
            confirmacao = input(f"Tem certeza que deseja excluir o pedido {id_para_excluir}? (s/n): ").lower()
            
            if confirmacao == 's':
                lista_pedidos.pop(i) 
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
    """Função de encerramento do programa."""
    print("Obrigado por usar o FEIFood. Até logo!")
    exit()



# - BLOC0 3: FUNÇÃO PRINCIPAL  E FLUXO DO PROGRAMA 

def main():
    
    #Função principal que controla o fluxo do programa, exibe menus e chama as funções.

    alimentos = ler_arquivo(ARQUIVO_ALIMENTOS)
    
    usuario_logado = None 
    
    menu_deslogado = {"1": "Fazer Login", "2": "Cadastrar Novo Usuário", "0": "Sair do Programa"}
    menu_logado = {
        "3": "Buscar por alimento", 
        "4": "Cadastrar novo pedido", 
        "5": "Avaliar um pedido",
        "6": "Excluir Pedido", 
        "7": "Editar Pedido", # NOVO
        "9": "Fazer Logoff", 
        "0": "Sair do Programa"
    }

    while True:
        print("\n" + "=" * 25)
        print("--- BEM-VINDO AO FEIFOOD ---")
        print("=" * 25)
        
        menu_atual = menu_deslogado
        if usuario_logado is not None:
            menu_atual = menu_logado
            print(f"Logado como: {usuario_logado}\n") 
        else:
            print("Você está deslogado.\n")
        
        for key, value in menu_atual.items():
            print(f"{key}. {value}")
            
        opcao = input("\nEscolha uma opção: ")

        # Controle de Opções e Chamada das Funções
        
        if opcao == "1" and usuario_logado is None:
            usuario_logado = fazer_login()
        
        elif opcao == "2" and usuario_logado is None:
            cadastrar_usuario() 
        
        elif opcao == "3" and usuario_logado is not None:
            buscar_alimento(alimentos)
        
        elif opcao == "4" and usuario_logado is not None:
            cadastrar_pedido(alimentos, usuario_logado)
        
        elif opcao == "5" and usuario_logado is not None:
            avaliar_pedido(usuario_logado)
        
        elif opcao == "6" and usuario_logado is not None:
            excluir_pedido(usuario_logado)
        
        # NOVA OPÇÃO
        elif opcao == "7" and usuario_logado is not None:
            editar_pedido(alimentos, usuario_logado)

        elif opcao == "9" and usuario_logado is not None:
            usuario_logado = None
            print("Logoff realizado com sucesso.")

        elif opcao == "0":
            sair()

        else:
            print("Opção inválida ou não permitida.")



# --- BLOC0 4: PONTO DE ENTRADA ---

if __name__ == "__main__":
    main()