"""Arquivo principal, usado para executar o Gerenciador de Tarefas."""

from typing import Callable
import comandos.busca
import comandos.edicao
import comandos.visualizacao
import terminal_utils as trm

class UserCommands:
    """Classe que contém todos os comandos que podem
    ser executados pelo usuário.
    """

    @staticmethod
    def ajuda() -> None:
        """Mostra a lista de comandos disponíveis para o usuário."""
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
        print(trm.bold("=> Concluir tarefa:"), "conclui uma tarefa")
        print(trm.bold("=> Ver lista:"), "mostra as tarefas presentes em uma lista") # use the ID and title of a list to search
        print(trm.bold("=> Ver listas:"), "mostra o título e o ID de todas as listas existentes")
        print(trm.bold("=> Ver tudo:"), "mostra todas as listas, as tarefas dentro delas e as propriedades das tarefas")
        print(trm.bold("=> Buscar tarefas:"), "mostra a lista de comandos disponíveis para encontrar tarefas com certas características")
        print(trm.bold("=> Limpar tela:"), "limpa a tela do terminal")
        print(trm.bold("=> Sair:"), "encerra o programa")
        print()
    
    @staticmethod
    def adicionar_tarefa(*_) -> None:
        comandos.edicao.adicionar_tarefa()

    @staticmethod
    def adicionar_lista(*_) -> None:
        comandos.edicao.adicionar_lista()

    @staticmethod
    def remover_tarefa(*_) -> None:
        comandos.edicao.remover_tarefa()

    @staticmethod
    def remover_lista(*_) -> None:
        comandos.edicao.remover_lista()
    
    @staticmethod
    def editar_tarefa(*_) -> None:
        comandos.edicao.editar_tarefa()
    
    @staticmethod
    def editar_lista(*_) -> None:
        comandos.edicao.editar_lista()
    
    @staticmethod
    def concluir_tarefa(*_) -> None:
        comandos.edicao.concluir_tarefa()
    
    @staticmethod
    def ver_lista(*titulo) -> None:
        comandos.visualizacao.ver_lista(*titulo)
    
    @staticmethod
    def ver_listas(*_) -> None:
        comandos.visualizacao.ver_listas()
    
    @staticmethod
    def ver_tudo(*_) -> None:
        comandos.visualizacao.ver_tudo()
    
    @staticmethod
    def buscar_tarefas(*args) -> None:
        comandos.busca.buscar_tarefas(*args)

    @staticmethod
    def limpar_tela(*_) -> None:
        trm.clear_screen()

    @staticmethod
    def sair() -> None:
        print("Saindo...")
        print("Seus dados estão salvos. Até mais!")
        print()
        exit()


def main() -> None:
    """Função principal do programa."""
    UserCommands.ajuda()
    while True:
        # recebe o input do usuário e separa suas palavras
        user_input: str = input(trm.bold("manager") + "> ")
        words: list[str] = user_input.lower().split()

        if not words:
            continue

        if len(words) == 1:
            # comando de uma só palavra
            command: str = words[0]
            args: tuple = tuple()
        else:
            # comando de duas palavras
            c1, c2, *args = words
            command: str = f"{c1}_{c2}"
        
        # checa se o comando existe
        if hasattr(UserCommands, command):
            # se sim, extrai o método correspondente ao comando
            method: Callable = getattr(UserCommands, command)
            # executa tal método
            method(*args)
        else:
            print(f'Comando "{trm.bold(user_input.lower())}" não encontrado.')
            print('Digite "ajuda" para ver os comandos disponíveis.')
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCtrl+C pressionado. Saindo...")
        print("Seus dados estão salvos. Até mais!")
        print()
        exit()