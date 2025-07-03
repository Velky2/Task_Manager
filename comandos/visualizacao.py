from classes.tarefa import Tarefa
from comandos.manipulacao_de_dados import listas
from comandos.edicao import imprimir_tarefa
import terminal_utils as trm
from typing import Callable
from datetime import date, timedelta

def ver_lista(*titulo) -> None:
        titulo: str = "".join(titulo).strip('"').lower()
        if not titulo:
            print('Uso: ver lista "Titulo da Lista"')
            print("Listas disponiveis:", end="\n   ")
            print(*(f'("{lista.titulo}" - ID: {lista.id})' for lista in listas), sep=" | ")
            return
        
        for lista in listas:
            if titulo == "".join(lista.titulo).lower():
                for t in lista.tarefas:
                    imprimir_tarefa(t)
                return

def ver_listas() -> None:
        # TODO: make it more robust
        print(*(f'("{lista.titulo}" - ID: {lista.id})' for lista in listas), sep=" | ")

def ver_tudo() -> None:
        for lista in listas:
            print()
            print(f"===== Lista: {lista.titulo} =====")
            print()
            for tarefa in lista.tarefas:
                imprimir_tarefa(tarefa)
                print()

def buscar_tarefas(*args) -> None:
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
            imprimir_tarefa(tarefa)