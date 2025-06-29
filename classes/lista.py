from classes.tarefa import Tarefa

class ListaDeTarefas:
    id_count: int = 0
    
    def __init__(self, titulo: str) -> None:
        self.id = ListaDeTarefas.id_count
        ListaDeTarefas.id_count += 1
        self.titulo = titulo
        self.tarefas = []
    
    def __repr__(self) -> None:
        print(f"===== Lista: {self.titulo} =====")
        for tarefa in self.tarefas:
            print(tarefa)

    def adicionar_tarefa(self, tarefa: Tarefa) -> None:
        self.tarefas.append(tarefa)

    def remover_tarefa(self, id_tarefa: int):
        for t in self.tarefas:
            if t.id == id_tarefa:
                self.tarefas.remove(t)