"""Módulo de busca.

Implementa os mecanismos necessários para o comando de busca por tarefas.
"""

from typing import Callable
from datetime import date, timedelta
from classes.tarefa import Tarefa
from comandos.manipulacao_de_dados import listas
import terminal_utils as trm

def gerar_filtro_texto(texto: str) -> Callable:
    """Retorna uma função de filtro que pode ser usada para checar
    se o texto da string `valor` está contida em uma dada tarefa.
    """
    return (lambda tarefa, texto=texto:
                texto in tarefa.titulo.lower()
                or texto in tarefa.nota.lower()
                or any((texto in tag.lower()) for tag in tarefa.tags))


def gerar_filtro_lista_nome(nome: str) -> Callable:
    """Retorna uma função de filtro que pode ser usada para checar
    se uma dada tarefa está associada à lista de nome `valor`.
    """
    lista_id: int
    for lista in listas:
        if lista.titulo.lower() == nome.lower():
            lista_id = lista.id
            break
    else:
        raise ValueError("Lista não encontrada")
    
    return (lambda tarefa, lista_id=lista_id:
                tarefa.lista_associada == lista_id)


def gerar_filtro_lista_id(id: str | int) -> Callable:
    """Retorna uma função de filtro que pode ser usada para checar
    se uma dada tarefa está associada à lista cujo id é `id`.
    """
    try:
        id = int(id)
    except ValueError:
        raise ValueError("ID inválido")
    
    for lista in listas:
        if lista.id == id:
            break
    else:
        raise ValueError("Lista não encontrada")
    
    return (lambda tarefa, id=id: tarefa.lista_associada == id)


def gerar_filtro_tags(tags: str) -> Callable:
    """Retorna uma função de filtro que pode ser usada para checar
    se uma dada tarefa contém a(s) tag(s) da string `tags`.
    """
    return (lambda tarefa, tags=tags:
                all((tag.strip() in tarefa.tags)
                        for tag in tags.split(",") if tag))


def gerar_filtro_ate_data(valor: str) -> Callable:
    """Retorna uma função de filtro que pode ser usada para checar
    se a data de uma dada tarefa é igual ou anterior à data ou prazo
    fornecido pela string `valor`.
    """
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
    
    return (lambda tarefa, target_date=target_date:
                tarefa.data <= target_date)


def gerar_filtro_concluida(valor: str) -> Callable:
    """Retorna uma função de filtro que pode ser usada para checar
    se uma dada tarefa está ou não concluída (a depender do `valor`,
    que pode indicar sim ou não).
    """
    concluida: bool = valor.startswith("s")
    return (lambda tarefa, concluida=concluida:
                tarefa.concluida == concluida)


def obter_filtro(tipo: str, valor: str) -> Callable | None:
    """Obtém uma função de filtro do tipo `tipo` a partir do valor `valor`."""
    match tipo:
        case "TEXTO":
            return gerar_filtro_texto(valor)
        case "LISTA_NOME":
            try:
                return gerar_filtro_lista_nome(valor)
            except ValueError:
                print(f'Lista com título "{valor}" não encontrada!')
                print(f'Tente rodar "ver listas" para ver as listas disponíveis.')
                return None
        case "LISTA_ID":
            try:
                return gerar_filtro_lista_id(valor)
            except ValueError:
                print(f'Lista com o id "{valor}" não encontrada!')
                print(f'Tente rodar "ver listas" para ver as listas disponíveis.')
                return None
        case "TAGS" | "TAG":
            return gerar_filtro_tags(valor)
        case "ATE" | "ATÉ":
            try:
                return gerar_filtro_ate_data(valor)
            except (ValueError, TypeError):
                print('Data inválida! Use "HOJE", "7 DIAS" ou' \
                    ' uma data no formato "DD/MM/AAAA".')
                return None
        case "CONCLUIDA" | "CONCLUÍDA" | "CONCLUIDAS" | "CONCLUÍDAS":
            return gerar_filtro_concluida(valor)


def gerar_busca(words: list[str]) -> tuple[list[Callable], Callable] | tuple[None, None]:
    """Obtém todas as funções de filtro necessárias para uma dada busca."""

    filtros: list[Callable] = []

    # Ordenação padrão é, primariamente, por data
    sorting_key: Callable = lambda tarefa: (
                tarefa.data if tarefa.data else date.max,
                -tarefa.prioridade,
                tarefa.lista_associada,
            )

    for i in range(0, len(words) - 1, 2):
        # extrai cada filtro do input, com o tipo e seu respectivo valor
        tipo: str = words[i].strip(" :").upper()
        valor: str = words[i + 1].lower()

        if tipo != "ORDENAR":
            filtro: Callable = obter_filtro(tipo, valor)
            if not filtro:
                return None, None
            filtros.append(filtro)
        else:
            # Ordenação padrão já é por data, então só é preciso
            # mudar quando o usuário quer ordenar por prioridade
            if valor.upper() == "PRIORIDADE":
                sorting_key = lambda tarefa: (
                        -tarefa.prioridade,
                        tarefa.data if tarefa.data else date.max,
                        tarefa.lista_associada,
                    )
    
    return (filtros, sorting_key)


def imprimir_ajuda_busca() -> None:
    """Imprime um tutorial para a utilização do comando de busca."""
    print()
    print(trm.underline(trm.bold("Uso:")), trm.bold('Buscar tarefas FILTRO1:"filtro" FILTRO2:"outro filtro"'))
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


def buscar_tarefas(*args) -> None:
    """Faz uma busca por tarefas com base nos filtros fornecidos.
    
    Imprime os resultados no terminal.
    """
    texto: str = " ".join(args)
    if not texto:
        imprimir_ajuda_busca()
        return
    
    # separa os argumentos do input adequadamente pelas aspas
    words: list[str] = texto.split('"')
    if len(words) == 1:
        print("Certifique-se de usar aspas ao redor de cada valor de filtro na busca.")
        return

    filtros: list[Callable]
    sorting_key: Callable
    filtros, sorting_key = gerar_busca(words)
    if filtros is None:
        return

    # filtra todas as tarefas, guarda apenas as que atendem
    # a todos os critérios dos filtros, e ordena os resultados
    resultados: list[Tarefa] = []
    for lista in listas:
        for tarefa in lista.tarefas:
            if all(filtro(tarefa) for filtro in filtros):
                resultados.append(tarefa)
    resultados.sort(key=sorting_key)
    
    if not resultados:
        print("Nenhuma tarefa encontrada nessa busca. :/")
        return
    print(trm.bold(trm.italic("\n>>>>>> RESULTADOS DA BUSCA:\n")))
    print("\n\n".join(str(tarefa) for tarefa in resultados))
    print()
