"""Módulo de edição.

Contém os mecanismos de manipulação de tarefas pelo usuário.
"""

from datetime import date, timedelta
from classes.tarefa import Tarefa, Repeticao
from classes.lista import ListaDeTarefas
from comandos.manipulacao_de_dados import salvar_mudanças, salvar_dados, listas
import terminal_utils as trm

def encontrar_tarefa_pelo_id(id: int) -> tuple[Tarefa, ListaDeTarefas] | tuple[None, None]:
    """ Itera sobre todas as listas e tarefas para encontrar uma tarefa pelo ID """
    for l in listas:
        for t in l.tarefas:
            if t.id == id:
                return t, l
    return None, None


def encontrar_lista_pelo_id(id: int) -> ListaDeTarefas | None:
    """ Itera sobre as listas para encontrar uma lista pelo ID. """
    for l in listas:
        if l.id == id:
            return l
    return None


def confirmar_id_int() -> int:
    """ Solicita e valida a entrada de um ID como um número interio. """
    while True:
        try:
            n = int(input("ID: "))
        except ValueError:
            print("ID inválido!")
        else:
            return n


def adicionar_tarefa() -> None:
    """ Adiciona uma nova tarefa a uma lista existente. """
    while True:
        titulo = input("Escolha um título: ")
        if titulo == "":
            print("O título não pode ser vazio, tente novamente")
        else:
            break

    print("Listas disponíveis: ")
    for l in listas:
        print(f"Título: {l.titulo} | ID: {l.id}")
    
    lista_associada = confirmar_id_int()

    lista = encontrar_lista_pelo_id(lista_associada)
    
    if lista:
        nota = input("Nota: ")
        data_str = input("Data (DD/MM/AAAA): ")

        if data_str:
            # Valida o formato da data inserida pelo usuário
            while True:
                try:
                    dia, mes, ano = map(int, data_str.split('/'))
                    data_obj = date(ano, mes, dia)
                except (ValueError, TypeError):
                    print("Formato de data inválido! Use DD/MM/AAAA")
                    data_str = input("Data (DD/MM/AAAA): ")
                else:
                    break
        else:
            data_obj = None

        tags_str = input("Tags (vírgula para separar): ")
        tags = set(tag.strip().lower() for tag in tags_str.split(" "))
        
        # Loop para validar a entrada de prioridade
        while True:
            try:
                prioridade = int(input("Prioridade (Sem prioridade = 0 | Baixa = 1 | Média = 2 | Alta = 3): "))
            except ValueError:
                print("Somente escreva números inteiros")
                continue

            if prioridade > 3 or prioridade < 0:
                print("Insira um valor entre 0 e 4")
            else:
                break
        # Loop para validar a entrada de repetição
        while True:
            try:
                repeticao = int(input("Repeticao (Nenhuma = 0 | Diária = 1 | Semanal = 2 | Mensal = 3 | Anual = 4): "))
            except ValueError:
                print("Somente escreva números inteiros")
                continue

            if repeticao > 4 or repeticao < 0:
                print("Insira um valor entre 0 e 4")
            else:
                break
        
        # Cria uma nova instância de Tarefa com os dados coletados
        nova_tarefa = Tarefa(
            titulo=titulo,
            lista_associada=lista_associada,
            nota=nota,
            data=data_obj,
            tags=tags,
            prioridade=prioridade,
            repeticao=repeticao,
            concluida=False
        )
        if not salvar_mudanças():
            return
        lista.adicionar_tarefa(nova_tarefa)
        salvar_dados()
        print("Feito :D")
    else:
        print("Lista não encontrada")


def adicionar_lista() -> None:
    """ Adiciona uma nova lista de tarefas. """
    while True:
        p = True
        novo_titulo = input(trm.bold(("Digite o título: ")))
        if novo_titulo == "":
            print("Digite um título não vazio")
            continue
        # Verifica se o título já existe
        for l in listas:
            if novo_titulo.lower() == l.titulo.lower():
                p = False
        if p:
            nova_lista = ListaDeTarefas(titulo=novo_titulo)
            if not salvar_mudanças():
                return
            listas.append(nova_lista)
            salvar_dados()
            print("Feito :D")
            return
        else:
            print("Já existe uma lista com esse título, tente novamente")


def remover_tarefa() -> None:
    """ Remove uma tarefa existente e as tarefas dentro dela. """
    print(trm.bold("Escolha a tarefa que deseja remover:"))
    for l in listas:
        for t in l.tarefas:
            print(f"Título: {t.titulo} | ID: {t.id}")
    
    tarefa_id = confirmar_id_int()
    
    tarefa, lista = encontrar_tarefa_pelo_id(tarefa_id)

    if tarefa and lista:
        if not salvar_mudanças():
            return
        lista.remover_tarefa(tarefa.id)
        salvar_dados()
        print("Feito :D")
    else:
        print("Tarefa não encontrada")


def remover_lista() -> None:
    """ Remove uma lista existente"""
    if len(listas) <= 1:
        print()
        print("Somente há uma lista salva, você não pode exclui-la")
        return
    
    print(trm.bold("Escolha a lista que deseja remover:"))
    for l in listas:
        print(f"Título: {l.titulo} | ID: {l.id}")
    
    lista_id = confirmar_id_int()

    lista = encontrar_lista_pelo_id(lista_id)

    if lista:
        while True:
            confirmacao = input("Apagar a lista também excluirá todas as tarefas contidas nela. Você quer continuar com a ação? (S/N): ")
            if confirmacao == "S" or confirmacao == "s":
                listas.remove(lista)
                salvar_dados()
                print("Feito :D")
                return
            elif confirmacao == "N" or confirmacao == "n":
                print("Ação cancelada")
                return
            else:
                print("Digite S ou N")
                print()
    else:
        print("Lista não encontrada")


def editar_tarefa() -> None:
    """ Edita os atributos de uma tarefa existente. """
    print(trm.bold("Selecione a tarefa que deseja editar:"))
    for l in listas:
        for t in l.tarefas:
            print(f"Título: {t.titulo} | ID: {t.id}")
    
    tarefa_id = confirmar_id_int()

    tarefa, lista = encontrar_tarefa_pelo_id(tarefa_id)
    
    if tarefa:
        print()
        print(trm.bold("O valor anterior do atributo será apresentado dentro de colchetes"))
        print("Pressione Enter para não alterar o valor")
        print()
        titulo = input(f"Novo título [{tarefa.titulo}]: ")
        
        # Edição da lista associada, com validação de ID
        while True:
            print("Listas disponíveis:")
            for l in listas:
                print(f"    Título: {l.titulo} | ID: {l.id}")
            lista_associada = input(f"Novo id da lista associada [{tarefa.lista_associada}]: ")
            
            if lista_associada == "":
                break
            try:
                lista_associada = int(lista_associada)
            except ValueError:
                print("ID inválido!")
                continue        
            if encontrar_lista_pelo_id(int(lista_associada)):
                break
            else:
                print("O ID colocado não existe, tente novamente")

        nota = input(f"Nova nota [{tarefa.nota}]: ")
        
        data_obj1 = None
        if tarefa.data:
            data_obj1 = tarefa.data.strftime("%d/%m/%Y")
        
        data_str = input(f"Nova data [{data_obj1}]: ")
        
        # Validação do novo formato de data
        if data_str:
            while True:
                try:
                    dia, mes, ano = map(int, data_str.split('/'))
                    data_obj2 = date(ano, mes, dia)
                except (ValueError, TypeError):
                    print("Formato de data inválido! Use DD/MM/AAAA")
                    data_str = input("Data (DD/MM/AAAA): ")
                else:
                    break
        else:
            data_obj2 = None

        print(f"Novas tags separadas por vírgula [{tarefa.tags}]")
        tags_str = input(f"  (substituirão as antigas): ")
        
        # Edição e validação da prioridade
        while True:
            prioridade = input(f"Nova prioridade [{tarefa.prioridade}] (Sem prioridade = 0 | Baixa = 1 | Média = 2 | Alta = 3): ")
            if prioridade == "":
                break
            try:
                prioridade = int(prioridade)
            except ValueError:
                print("Somente números inteiros são aceitos")
            else:
                break
        
        # Edição e validação da repetição
        while True:
            repeticao = input(f"Nova repetição [{tarefa.repeticao}] (Nenhuma = 0 | Diária = 1 | Semanal = 2 | Mensal = 3 | Anual = 4): ")
            if repeticao == "":
                break
            try:
                repeticao = int(repeticao)
            except ValueError:
                print("Somente números inteiros são aceitos")
            else:
                break
        
        if not salvar_mudanças():
            return

        # Atualiza os atributos da tarefa se novos valores forem fornecidos
        if titulo:
            tarefa.titulo = titulo
        if lista_associada:
            tarefa.lista_associada = lista_associada
        if nota:    
            tarefa.nota = nota
        if data_obj2:
            tarefa.data = data_obj2
        if tags_str:
            tarefa.tags = set(tag.strip().lower() for tag in tags_str.split(" "))
        if prioridade:
            tarefa.prioridade = prioridade
        if repeticao:    
            tarefa.repeticao = repeticao
        
        salvar_dados()
        print("Feito :D")
    else:
        print("Tarefa não encontrada")


def editar_lista() -> None:
    """ Edita o título de uma lista existente. """
    print(trm.bold("Selecione a lista que deseja editar:"))
    for l in listas:
        print(f"Título: {l.titulo} | ID: {l.id}")

    lista_id = confirmar_id_int()

    lista = encontrar_lista_pelo_id(lista_id)
    
    if lista:
        # Loop para garantir que um novo título válido seja fornecido
        while True:
            p = True
            titulo = input("Novo título: ")

            if not titulo:
                print("Novo título não inserido")
                continue
            
            # Verifica se o novo título já existe
            for l in listas:
                if l.titulo.lower() == titulo.lower():
                    print("Título já existente, tente novamente")
                    p = False
                    break
            if p:
                break
        
        if not salvar_mudanças():
            return
        
        lista.titulo = titulo

        salvar_dados()
        print("Feito :D")
    else:
        print("Lista não encontrada")


def concluir_tarefa() -> None:
    """ Marca uma tarefa como concluída e, se for repetível, cria uma nova tarefa considerqando o tipo de repetição. """
    print(trm.bold("Selecione a tarefa que foi concluída:"))

    # Exibe apenas as tarefas não concluídas
    for l in listas:
        for t in l.tarefas:
            if not t.concluida:
                print(f"Título: {t.titulo} | ID: {t.id}")

    tarefa_id = confirmar_id_int()

    tarefa, lista = encontrar_tarefa_pelo_id(tarefa_id)

    if not tarefa or not lista:
        print("Tarefa ou lista não encontrada!")
        return
    tarefa.concluida = True

    # Se a tarefa não for repetível, apenas a marca como concluída
    if tarefa.repeticao == Repeticao.NENHUMA.value:
        print("Tarefa concluída com sucesso!")
        return
    
    # Cria uma nova instância da tarefa para a próxima repetição
    nova_tarefa = Tarefa(
        titulo=tarefa.titulo,
        lista_associada=tarefa.lista_associada,
        nota=tarefa.nota,
        data=tarefa.data,
        tags=tarefa.tags.copy(),
        prioridade=tarefa.prioridade,
        repeticao=tarefa.repeticao,
        concluida=False
    )

    if tarefa.data is None:
        tarefa.data = date.today()
    
    # Define a data da nova tarefa com base na repetição
    match tarefa.repeticao:
        case Repeticao.DIARIA.value:
            nova_tarefa.data = tarefa.data + timedelta(days=1)
        
        case Repeticao.SEMANAL.value:
            nova_tarefa.data = tarefa.data + timedelta(weeks=1)
        
        case Repeticao.MENSAL.value:
            nova_tarefa.data = tarefa.data + timedelta(days=30)
        
        case Repeticao.ANUAL.value:
            try:
                nova_tarefa.data = tarefa.data.replace(
                        year=tarefa.data.year + 1)
            except ValueError:
                # Caso ano bissexto (29 fev)
                nova_tarefa.data = tarefa.data.replace(
                        year=tarefa.data.year + 1) + timedelta(days=-1)

    if not salvar_mudanças():
        return
    
    lista.adicionar_tarefa(nova_tarefa)
    print(f"Tarefa concluída! Nova tarefa criada para {nova_tarefa.data.strftime('%d/%m/%Y')}")

    salvar_dados()