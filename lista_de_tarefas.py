from typing import Callable
from comandos.edicao import adicionar_tarefa, adicionar_lista, remover_tarefa, remover_lista, editar_tarefa, editar_lista, concluir_tarefa
from comandos.visualizacao import ver_lista, ver_listas, ver_tudo, buscar_tarefas
import terminal_utils as trm
from terminal_utils import clear_screen

class UserCommands:
    @staticmethod
    def ajuda() -> None:
        print()
        print(trm.bold("Digite algum dos comandos no terminal para realizar a ação:"))
        print()
        print(trm.bold("=> Ajuda:"), "mostra essa lista de comandos")
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
    def limpar_tela() -> None:
        clear_screen()
    
    @staticmethod
    def adicionar_tarefa() -> None:
        clear_screen()
        adicionar_tarefa()

    @staticmethod
    def adicionar_lista() -> None:
        clear_screen()
        adicionar_lista()

    @staticmethod
    def remover_tarefa() -> None:
        clear_screen()
        remover_tarefa()

    @staticmethod
    def remover_lista() -> None:
        clear_screen()
        remover_lista()
    
    @staticmethod
    def editar_tarefa() -> None:
        clear_screen()
        editar_tarefa()
    
    @staticmethod
    def editar_lista() -> None:
        clear_screen()
        editar_lista()
    
    @staticmethod
    def concluir_tarefa() -> None:
        clear_screen()
        concluir_tarefa()
    
    @staticmethod
    def ver_lista(*titulo) -> None:
        clear_screen()
        ver_lista(*titulo)
    
    @staticmethod
    def ver_listas() -> None:
        clear_screen()
        ver_listas()
    
    @staticmethod
    def ver_tudo() -> None:
        clear_screen()
        ver_tudo()
    
    @staticmethod
    def buscar_tarefas(*args) -> None:
        clear_screen()
        buscar_tarefas(*args)


def main() -> None:
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