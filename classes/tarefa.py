from datetime import date

class Tarefa:
    id_count: int = 0

    def __init__(self,
                titulo: str,
                lista_associada: int,
                nota: str = "",
                data: date | None = None,
                tags: list[str] = [],
                prioridade: int = 0,
                repeticao: int = 0,
                concluida: bool = False):
        
        self.id = Tarefa.id_count
        Tarefa.id_count += 1

        self.titulo = titulo
        self.nota = nota
        self.data = data
        self.tags = tags
        self.lista_associada = lista_associada
        self.prioridade = prioridade
        self.repeticao = repeticao
        self.concluida = concluida
    
    def __repr__(self) -> None:
        print(f"Tarefa: {self.titulo}")
        for attr in ("nota", "data", "tags", "lista_associada",
                     "prioridade", "repeticao", "concluida"):
            print(f"- {attr.capitalize()}: {getattr(self, attr)}")


if __name__ == "__main__":
    print(Tarefa.id_count)
    the = Tarefa(*([None] * 8))
    print(the.id)
    print(Tarefa.id_count, the.id_count)
    j = Tarefa(*([None] * 8))
    print(the.id, j.id)
    print(Tarefa.id_count, the.id_count, j.id_count)