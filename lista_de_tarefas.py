import json
import os
from datetime import date, timedelta
from typing import Callable
from classes.tarefa import Tarefa
from classes.lista import ListaDeTarefas
import terminal_utils as trm
from terminal_utils import clear_screen

listas: list[ListaDeTarefas] = []

arquivo: str = "tarefas.json"

class UserCommands:
    @staticmethod
    def salvar_dados() -> None:
        clear_screen()
        dados = {}
        for l in listas:
            tarefas_l = []
            for t in l.tarefas:
                tarefas_l.append(t.para_dicio())
            dados[l.titulo] = tarefas_l
        
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print("Feito :D")

    @staticmethod
    def carregar_dados() -> None:
        global listas
        try:
            with open(arquivo, "r") as f:
                dados_carregados = json.load(f)
            
            listas = []

            for titulo_lista, dados_tarefas in dados_carregados.items():
                nova_lista = ListaDeTarefas(titulo_lista)
                for tarefa_dict in dados_tarefas:
                    data_str = tarefa_dict.get("data")
                    data_obj = None
                    if data_str:
                        dia, mes, ano = map(int, data_str.split("/"))
                        data_obj = date(ano, mes, dia)
                    
                    nova_tarefa = Tarefa(
                        titulo=tarefa_dict["titulo"],
                        lista_associada=tarefa_dict["lista_associada"],
                        nota=tarefa_dict["nota"],
                        data=data_obj,
                        tags=set(tarefa_dict["tags"]),
                        prioridade=tarefa_dict["prioridade"],
                        repeticao=tarefa_dict["repeticao"],
                        concluida=tarefa_dict["concluida"],
                    )

                    nova_lista.adicionar_tarefa(nova_tarefa)
                
                listas.append(nova_lista)
            print()
            print(trm.bold("Dados carregados"))

        except FileNotFoundError:
            print(trm.bold("Começando com um arquivo vazio"))
            listas = [ListaDeTarefas("Cuba")]
        except json.JSONDecodeError:
            print(trm.bold("Começando com um arquivo vazio"))
            listas = [ListaDeTarefas("Cuba")]

    @staticmethod
    def limpar_tela() -> None:
        clear_screen()
    
    @staticmethod
    def ajuda() -> None:
        print()
        print(trm.bold("Escreva algum dos comandos no terminal para realizar a ação:"))
        print()
        print(trm.bold("=> Adicionar tarefa:"), "cria uma tarefa e a adiciona a uma lista existente")
        print(trm.bold("=> Adicionar lista:"), "cria uma lista")
        print(trm.bold("=> Remover tarefa:"), "remove uma tarefa")
        print(trm.bold("=> Remover lista:"), "remove uma lista e as tarefas que nela residem")
        print(trm.bold("=> Editar tarefa:"), "edita os valores de uma tarefa, à mercê do usuário")
        print(trm.bold("=> Editar lista:"), "edita o título de uma lista")
        print(trm.bold("=> Ver lista:"), "mostra as tarefas presentes em uma lista") # use the ID and title of a list to search
        print(trm.bold("=> Ver listas:"), "mostra o título e o ID de todas as listas existentes")
        print(trm.bold("=> Ver tudo:"), "mostra todas as listas, as tarefas dentro delas e as propriedades das tarefas")
        print(trm.bold("=> Buscar tarefas:"), "mostra a lista de comandos disponíveis para encontrar tarefas com certas características")
        print(trm.bold("=> Concluir tarefa:"), "conclui uma tarefa")

    @staticmethod
    def encontrar_tarefa_pelo_id(id: int) -> tuple[Tarefa, ListaDeTarefas] | tuple[None, None]:
        for l in listas:
            for t in l.tarefas:
                if t.id == id:
                    return t, l
        return None, None
    
    @staticmethod
    def encontrar_lista_pelo_id(id: int) -> ListaDeTarefas | None:
        for l in listas:
            if l.id == id:
                return l
        return None
    
    @staticmethod
    def confirmar_id_int():
            while True:
                try:
                    n = int(input("ID: "))
                except ValueError:
                    print("ID inválido!")
                else:
                    return n
    
    @staticmethod
    def imprimir_tarefa(tarefa):
        titulo = tarefa.titulo
        lista_associada = tarefa.lista_associada
        nota = tarefa.nota
        data = tarefa.data
        tags = tarefa.tags
        prioridade = tarefa.prioridade
        repetição = tarefa.repeticao
        concluida = tarefa.concluida
        id = tarefa.id

        print(f"Tarefa: {titulo} | ID: {id}")
        print(f"Lista associada: {lista_associada}")
        print(f"Nota: {nota}")
        if data:
            ano, mes, dia = map(int, str(data).split("-"))
            print(f"Data: {dia}/{mes}/{ano}")
        else:
            print("Data: ")

        print(f"Tags: {tags}")

        if prioridade == 0:
            print(f"Prioridade: nenhuma")
        elif prioridade == 1:
            print(f"Prioridade: baixa")
        elif prioridade == 2:
            print(f"Prioridade: média")
        else:
            print(f"Prioridade: alta")
        
        if repetição == 0:
            print(f"Sem repetição")
        elif repetição == 1:
            print(f"Repetição: diária")
        elif repetição == 2:
            print("Repetição: semanal")
        elif repetição == 3:
            print("Repetição: mensal")
        else:
            print("Repetição anual")
        
        if concluida:
            print("Concluida: sim")
        else:
            print("Concluida: não")

    @staticmethod
    def adicionar_tarefa() -> None:
        clear_screen()
        while True:
            titulo = input("Escolha um título: ")
            if titulo == "":
                print("O tĩtulo não pode ser vazio, tente novamente")
            else:
                break

        print("Listas disponíveis: ")
        for l in listas:
            print(f"Título: {l.titulo} | ID: {l.id}")
        
        lista_associada = UserCommands.confirmar_id_int()

        lista = UserCommands.encontrar_lista_pelo_id(lista_associada)
        
        if lista:
            nota = input("Nota: ")
            data_str = input("Data (DD/MM/AAAA): ")

            if data_str:
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
            tags = set(tag.strip().lower() for tag in tags_str.split(","))
            
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
            lista.adicionar_tarefa(nova_tarefa)
            print("Feito :D")
            UserCommands.salvar_dados()
        else:
            print("Lista não encontrada")
    
    @staticmethod
    def adicionar_lista() -> None:
        clear_screen()
        while True:
            p = True
            novo_titulo = input(trm.bold(("Digite o título: ")))
            if novo_titulo == "":
                print("Digite um título não vazio")
                continue
            for l in listas:
                if novo_titulo.lower() == l.titulo.lower():
                    p = False
            if p:
                nova_lista = ListaDeTarefas(titulo=novo_titulo)
                listas.append(nova_lista)
                print("Feito :D")
                UserCommands.salvar_dados()
            else:
                print("Já existe uma lista com esse título, tente novamente")

    @staticmethod
    def remover_tarefa() -> None:
        clear_screen()
        print(trm.bold("Escolha a tarefa que deseja remover:"))
        for l in listas:
            for t in l.tarefas:
                print(f"Título: {t.titulo} | ID: {t.id}")
        
        tarefa_id = UserCommands.confirmar_id_int()
        
        tarefa, lista = UserCommands.encontrar_tarefa_pelo_id(tarefa_id)

        if tarefa and lista:
            lista.remover_tarefa(tarefa.id)
            print("Feito :D")
            UserCommands.salvar_dados()
        else:
            print("Tarefa não encontrada")

    @staticmethod
    def remover_lista() -> None:
        clear_screen()
        if len(listas) <= 1:
            print()
            print("Somente há uma lista salva, você não pode exclui-la")
            return
        
        print(trm.bold("Escolha a lista que deseja remover:"))
        for l in listas:
            print(f"Título: {l.titulo} | ID: {l.id}")
        
        lista_id = UserCommands.confirmar_id_int()

        lista = UserCommands.encontrar_lista_pelo_id(lista_id)

        if lista:
            confirmacao = input("Apagar a lista também excluirá todas as tarefas contidas nela. Você quer continuar com a ação? (S/N): ")
            if confirmacao == "S":
                listas.remove(lista)
                print("Feito :D")
                UserCommands.salvar_dados()
            else:
                print("Ação cancelada")
        else:
            print("Lista não encontrada")
    
    @staticmethod
    def ver_lista(*titulo) -> None:
        clear_screen()
        titulo: str = "".join(titulo).strip('"').lower()
        if not titulo:
            print('Uso: ver lista "Titulo da Lista"')
            print("Listas disponiveis:", end="\n   ")
            print(*(f'("{lista.titulo}" - ID: {lista.id})' for lista in listas), sep=" | ")
            return
        
        for lista in listas:
            if titulo == "".join(lista.titulo).lower():
                for t in lista.tarefas:
                    UserCommands.imprimir_tarefa(t)
                return
    
    @staticmethod
    def ver_listas() -> None:
        clear_screen()
        # TODO: make it more robust
        print(*(f'("{lista.titulo}" - ID: {lista.id})' for lista in listas), sep=" | ")
    
    @staticmethod
    def ver_tudo() -> None:
        clear_screen()
        for lista in listas:
            print()
            print(f"===== Lista: {lista.titulo} =====")
            print()
            for t in lista.tarefas:
                UserCommands.imprimir_tarefa(t)
                print()
    
    @staticmethod
    def buscar_tarefas(*args) -> None:
        clear_screen()
        texto: str = " ".join(args)
        if not texto:
            print()
            print(trm.bold("Uso:"), trm.bold('Buscar tarefas FILTRO1:"filtro" FILTRO2:"outro filtro"'))
            print()
            print("- Deve-se incluir aspas ao redor de cada valor de filtro na busca.")
            print("- Deve-se usar um ou múltiplos dos filtros disponíveis:")
            print()
            print(trm.bold('=> TEXTO:"foo"'), '- busca por tarefas que contenham o texto no título, nota ou tags;')
            print(trm.bold('=> LISTA_NOME:"titulo da lista"'), '- busca por tarefas pertencentes à lista com esse título.')
            print(trm.bold('=> LISTA_ID:"id da lista"'), '- busca por tarefas pertencentes à lista com esse título.')
            print(trm.bold('=> TAGS:"bar, baz"'), '- busca por tarefas que contenham a(s) tag(s) fornecida(s);')
            print('    > Separe múltiplas tags por vírgula (",").')
            print(trm.bold('=> ATE:"prazo"'), '- busca por tarefas cujo prazo é até:')
            print('    > "HOJE", ou que já estão atrasadas')
            print('    > "7 DIAS", prazo contido nos próximos 7 dias ou já atrasadas')
            print('    > "DD/MM/AAAA", até a data específica dada (inclui atrasadas)')
            print(trm.bold('=> CONCLUIDA:"s"'), '- busca por tarefas concluídas ("s", "sim") ou pendentes ("n", "nao");')
            print(trm.bold('=> ORDENAR:"criterio"'), '- ordena os resultados pelo critério "DATA" ou "PRIORIDADE".')
            return
        keywords: list[str] = texto.split('"')
        filters: list[Callable] = []
        if len(keywords) == 1:
            print("Certifique-se de usar aspas ao redor de cada valor de filtro na busca.")
            return
        
        # Ordenação padrão é, primariamente, por data
        sorting_key: Callable = lambda tarefa: (
                    tarefa.data if tarefa.data else date.max,
                    -tarefa.prioridade,
                    tarefa.lista_associada,
                )

        for i in range(0, len(keywords) - 1, 2):
            tipo: str = keywords[i].strip(" :").upper()
            valor: str = keywords[i + 1].lower()

            # TODO: nothing 😎 (i hope), save from organizing
            match tipo:
                case "TEXTO":
                    filters.append(
                            lambda tarefa, valor=valor:
                                valor in tarefa.titulo.lower()
                                or valor in tarefa.nota.lower()
                                or any((valor in tag.lower())
                                        for tag in tarefa.tags)
                            )
                case "LISTA_NOME":
                    lista_id: int
                    for lista in listas:
                        if lista.titulo == valor:
                            lista_id = lista.id
                            break
                    else:
                        print(f'Lista com título "{valor}" não encontrada!')
                        print(f'Tente rodar "ver listas" para ver as listas disponíveis.')
                        return
                    filters.append(
                            lambda tarefa, valor=valor:
                                tarefa.lista_associada == lista_id
                            )
                case "LISTA_ID":
                    for lista in listas:
                        if lista.id == valor:
                            break
                    else:
                        print(f'Lista com o id "{valor}" não encontrada!')
                        print(f'Tente rodar "ver listas" para ver as listas disponíveis.')
                        return
                    filters.append(
                            lambda tarefa, valor=valor:
                                tarefa.lista_associada == lista_id
                            )
                case "TAGS":
                    filters.append(
                            lambda tarefa, valor=valor:
                                all((tag.strip() in tarefa.tags)
                                for tag in valor.split(",") if tag)
                            )
                case "ATE":
                    target_date: date
                    match valor.upper():
                        case "HOJE":
                            target_date = date.today()
                        case "7 DIAS":
                            target_date = date.today() + timedelta(days=7)
                        case _:
                            try:
                                day, month, year = map(int, valor.split("/"))
                                target_date = date(year, month, day)
                            except (ValueError, TypeError):
                                print('Data inválida! Use "HOJE", "7 DIAS" ou' \
                                    ' uma data no formato "DD/MM/AAAA".')
                                return
                    filters.append(lambda tarefa, target_date=target_date:
                                    tarefa.data <= target_date)
                case "CONCLUIDA":
                    concluida: bool = valor.startswith("s")
                    filters.append(lambda tarefa, concluida=concluida:
                                    tarefa.concluida == concluida)
                case "ORDENAR":
                    # Ordenação padrão já é por data, então só é preciso
                    # mudar quando o usuário quer ordenar por prioridade
                    if valor.upper() == "PRIORIDADE":
                        sorting_key = lambda tarefa: (
                                    -tarefa.prioridade,
                                    tarefa.data if tarefa.data else date.max,
                                    tarefa.lista_associada,
                                )

        resultados: list[Tarefa] = []
        for lista in listas:
            for tarefa in lista.tarefas:
                if all(filtro(tarefa) for filtro in filters):
                    resultados.append(tarefa)
        resultados.sort(key=sorting_key)
        
        if not resultados:
            print("Nenhuma tarefa encontrada nessa busca. :/")
            return
        print(">>>>>> RESULTADOS DA BUSCA:")
        for tarefa in resultados:
            UserCommands.imprimir_tarefa(tarefa)
                
    @staticmethod
    def editar_tarefa() -> None:
        clear_screen()

        print(trm.bold("Selecione a tarefa que deseja editar:"))
        for l in listas:
            for t in l.tarefas:
                print(f"Título: {t.titulo} | ID: {t.id}")
        
        tarefa_id = UserCommands.confirmar_id_int()

        tarefa, lista = UserCommands.encontrar_tarefa_pelo_id(tarefa_id)
        
        if tarefa:
            print()
            print(trm.bold("O valor anterior do atributo será apresentado dentro de colchetes"))
            print("Pressione Enter para não alterar o valor")
            print()
            titulo = input(f"Novo título [{tarefa.titulo}]: ")
            
            while True:
                for l in listas:
                    print(f"Título: {l.titulo} | ID: {l.id}")
                lista_associada = input(f"Novo id da lista associada [{tarefa.lista_associada}]: ")
                
                if lista_associada == "":
                    break
                try:
                    int(lista_associada)
                except ValueError:
                    print("ID inválido!")
                    continue        
                if UserCommands.encontrar_lista_pelo_id(int(lista_associada)):
                    break
                else:
                    print("O ID colocado não existe, tente novamente")

            nota = input(f"Nova nota [{tarefa.nota}]: ")
            data_str = input(f"Nova data [{tarefa.data}]: ")

            if data_str:
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

            tags_str = input(f"Novas tags separadas por vírgula (substituirão as antigas) [{tarefa.tags}]: ")
            
            while True:
                prioridade = input(f"Nova prioridade [{tarefa.prioridade}] (Sem prioridade = 0 | Baixa = 1 | Média = 2 | Alta = 3): ")
                if prioridade == "":
                    break
                try:
                    int(prioridade)
                except ValueError:
                    print("Somente números inteiros são aceitos")
                else:
                    break
            
            while True:
                repeticao = input(f"Nova repetição [{tarefa.repeticao}] (Nenhuma = 0 | Diária = 1 | Semanal = 2 | Mensal = 3 | Anual = 4): ")
                if repeticao == "":
                    break
                try:
                    int(repeticao)
                except ValueError:
                    print("Somente números inteiros são aceitos")
                else:
                    break
            
            if titulo:
                tarefa.titulo = titulo
            if lista_associada:
                tarefa.lista_associada = lista_associada
            if nota:    
                tarefa.nota = nota
            if data_obj:
                tarefa.data = data_obj
            if tags_str:
                tarefa.tags = set(tag.strip().lower() for tag in tags_str.split(","))
            if prioridade:
                tarefa.prioridade = prioridade
            if repeticao:    
                tarefa.repeticao = repeticao
            print("Feito :D")
            UserCommands.salvar_dados()
        else:
            print("Tarefa não encontrada")

    
    @staticmethod
    def editar_lista() -> None:
        clear_screen()
        print(trm.bold("Selecione a lista que deseja editar:"))
        for l in listas:
            print(f"Título: {l.titulo} | ID: {l.id}")

        lista_id = UserCommands.confirmar_id_int()

        lista = UserCommands.encontrar_lista_pelo_id(lista_id)
        
        if lista:
            while True:
                p = True
                titulo = input("Novo título: ")

                if not titulo:
                    print("Novo título não inserido")
                    continue

                for l in listas:
                    if l.titulo.lower() == titulo.lower():
                        print("Título já existente, tente novamente")
                        p = False
                        break
                if p:
                    break

            lista.titulo = titulo
            print("Feito :D")
            UserCommands.salvar_dados()
        else:
            print("Lista não encontrada")
    
    @staticmethod
    def concluir_tarefa() -> None:
        clear_screen()
        print(trm.bold("Selecione a tarefa que foi concluída:"))

        for l in listas:
            for t in l.tarefas:
                if not t.concluida:
                    print(f"Título: {t.titulo} | ID: {t.id}")

        tarefa_id = UserCommands.confirmar_id_int()

        tarefa, lista = UserCommands.encontrar_tarefa_pelo_id(tarefa_id)

        if not tarefa or not lista:
            print("Tarefa ou lista não encontrada!")
            return
        tarefa.concluida = True
        if tarefa.repeticao != 0:
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

            if tarefa.data:
                if tarefa.repeticao == 1:  # Diária
                    nova_tarefa.data = tarefa.data + timedelta(days=1)
                elif tarefa.repeticao == 2:  # Semanal
                    nova_tarefa.data = tarefa.data + timedelta(weeks=1)
                elif tarefa.repeticao == 3:  # Mensal
                    nova_tarefa.data = tarefa.data + timedelta(days=30)
                elif tarefa.repeticao == 4:  # Anual
                    nova_tarefa.data = tarefa.data.replace(year=tarefa.data.year + 1)
                lista.adicionar_tarefa(nova_tarefa)
                print(f"Tarefa concluída! Nova tarefa criada para {nova_tarefa.data.strftime('%d/%m/%Y')}")
                UserCommands.salvar_dados()
        else:
            print("Tarefa concluída com sucesso!")


def main() -> None:
    UserCommands.carregar_dados()
    UserCommands.ajuda()
    while True:
        user_input: str = input(trm.bold("manager") + "> ")
        words: list[str] = user_input.lower().split()
        if not words:
            continue
        if len(words) == 1:
            command: str = words[0]
            args: tuple = tuple()
        else:
            c1, c2, *args = words
            command: str = f"{c1}_{c2}"
        if hasattr(UserCommands, command):
            method: Callable = getattr(UserCommands, command)
            method(*args)
        else:
            print(f'Comando "{trm.bold(user_input.lower())}" não encontrado.')
            print('Digite "ajuda" para ver os comandos disponíveis.')
        print()

if __name__ == "__main__":
    main()