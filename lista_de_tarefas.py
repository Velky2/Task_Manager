import json
import os
from datetime import date
from typing import Callable
from datetime import timedelta
from classes.tarefa import Tarefa
from classes.lista import ListaDeTarefas
from terminal_utils import clear_screen, bold

# arquivo_tarefa = "classes.tarefa.json"
# arquivo_lista = "classes.lista.json"

listas: list[ListaDeTarefas] = [ListaDeTarefas("Cuba")]

class UserCommands:
    @staticmethod
    def limpar_tela() -> None:
        clear_screen()
    
    @staticmethod
    def ajuda() -> None:
        print("Escreva algum dos comandos no terminal para realizar a ação:")
        print("=> Adicionar tarefa: cria uma tarefa e a adiciona a uma lista existente")
        print("=> Adicionar lista: cria uma lista")
        print("=> Remover tarefa: remove uma tarefa")
        print("=> Remover lista: remove uma lista e as tarefas que nela residem")
        print("=> Editar tarefa: edita os valores de uma tarefa, à mercê do usuário")
        print("=> Editar lista: edita o título de uma lista")
        print("=> Ver lista: mostra as tarefas presentes em uma lista") # use the ID and title of a list to search
        print("=> Ver listas: mostra o título e o ID de todas as listas existentes")
        print("=> Ver tudo: mostra todas as listas, as tarefas dentro delas e as propriedades das tarefas")
        print("=> Concluir tarefa: Conclui uma tarefa")

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
    def adicionar_tarefa() -> None:
        clear_screen()
        while True:
            titulo = input(bold("Escolha um título: "))
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
                    else:
                        break
            else:
                data_obj = None

            tags_str = input("Tags (espaco para separar): ")
            tags = tags_str.split()
            
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
        else:
            print("Lista não encontrada")
    
    @staticmethod
    def adicionar_lista() -> None:
        clear_screen()
        while True:
            p = True
            novo_titulo = input(bold(("Digite o título: ")))
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
                break
            else:
                print("Já existe uma lista com esse título, tente novamente")

    @staticmethod
    def remover_tarefa() -> None:
        clear_screen()
        print(bold("Escolha a tarefa que deseja remover:"))
        for l in listas:
            for t in l.tarefas:
                print(f"Título: {t.titulo} - ID: {t.id}")
        
        tarefa_id = UserCommands.confirmar_id_int()
        
        tarefa, lista = UserCommands.encontrar_tarefa_pelo_id(tarefa_id)

        if tarefa and lista:
            lista.remover_tarefa(tarefa)
            print("Feito :D")
        else:
            print("Tarefa não encontrada")

    @staticmethod
    def remover_lista() -> None:
        clear_screen()
        print(bold("Escolha a lista que deseja remover:"))
        for l in listas:
            print(f"Título: {l.titulo}, ID: {l.id}")
        
        lista_id = UserCommands.confirmar_id_int()

        lista = UserCommands.encontrar_lista_pelo_id(lista_id)

        if lista:
            listas.remove(lista)
            print("Feito :D")
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
            if titulo == lista.titulo.lower():
                print(lista)
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
            print(lista)
            for t in lista.tarefas:
                print(t.titulo, " | ")
            print()
    
    @staticmethod
    def buscar_tarefas(*args) -> None:
        clear_screen()
        texto: str = " ".join(args)
        if not texto:
            print("workinprogress")
            # TODO: default to showing them all maybe?
            return
        filtros: list[str] = texto.split('"')
        if len(filtros) == 1:
            print("uhh error? where my quotes at??")
            return
        for i in range(0, len(filtros), 2):
            tipo: str = filtros[i].strip(" :").upper()
            filtro: str = filtros[i + 1]

            # TODO: several things 🫠
            match tipo:
                case "TEXTO":
                    pass
                case "LISTA_NOME":
                    pass
                case "LISTA_ID":
                    pass
                case "TAGS":
                    pass
                case "ATE":
                    pass
                
    @staticmethod
    def editar_tarefa() -> None:
        clear_screen()

        print(bold("Selecione a tarefa que deseja editar:"))
        for l in listas:
            for t in l.tarefas:
                print(f"Título: {t.titulo} - ID: {t.id}")
        
        tarefa_id = UserCommands.confirmar_id_int()

        tarefa, lista = UserCommands.encontrar_tarefa_pelo_id(tarefa_id)
        
        if tarefa:
            print(bold("Pressione Enter para não alterar o valor"))
            titulo = input(f"Novo título ({tarefa.titulo}): ")
            
            while True:
                for l in listas:
                    print(f"Título: {l.titulo} | ID: {l.id}")
                lista_associada = input(f"Novo id da lista associada ({tarefa.lista_associada}): ")
                
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

            nota = input(f"Nova nota ({tarefa.nota}): ")
            data = input(f"Nova data ({tarefa.data}): ")
            tags_str = input(f"Novas tags separadas por espaço ({tarefa.tags}): ")
            
            while True:
                prioridade = input(f"Nova prioridade ({tarefa.prioridade}): ")
                if prioridade == "":
                    break
                try:
                    int(prioridade)
                except ValueError:
                    print("Somente números inteiros são aceitos")
                    continue
            
            while True:
                repeticao = int(input(f"Nova repetição ({tarefa.repeticao}): "))
                if repeticao == "":
                    break
                try:
                    int(repeticao)
                except ValueError:
                    print("Somente números inteiros são aceitos")
                    continue
            
            if titulo:
                tarefa.titulo = titulo
            if lista_associada:
                tarefa.lista_associada = lista_associada
            if nota:    
                tarefa.nota = nota
            if data:
                tarefa.data = data
            if tags_str:
                tarefa.tags = tags_str.split()
            if prioridade:
                tarefa.prioridade = prioridade
            if repeticao:    
                tarefa.repeticao = repeticao
            print("Feito :D")
        else:
            print("Tarefa não encontrada")

    
    @staticmethod
    def editar_lista() -> None:
        clear_screen()

        print(bold("Selecione a lista que deseja editar:"))
        for l in listas:
            print(f"Título: {l.titulo} - ID: {l.id}")

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
        else:
            print("Lista não encontrada")
    
    @staticmethod
    def concluir_tarefa() -> None:
        clear_screen()
        print("Selecione a tarefa que foi concluída:")

        for l in listas:
            for t in l.tarefas:
                if not t.concluida:
                    print(f"Título: {t.titulo} - ID: {t.id}")

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
        else:
            print("Tarefa concluída com sucesso!")


def main() -> None:
    UserCommands.ajuda()
    while True:
        words: list[str] = input(bold("manager") + "> ").lower().split()
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

if __name__ == "__main__":
    main()