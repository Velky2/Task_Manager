from datetime import date
from enum import Enum

class Prioridade(Enum):
    NENHUMA = 0
    BAIXA = 1
    MEDIA = 2
    ALTA = 3


class Repeticao(Enum):
    NENHUMA = 0
    DIARIA = 1
    SEMANAL = 2
    MENSAL = 3
    ANUAL = 4


class Tarefa:
    id_count: int = 0

    def __init__(self,
                titulo: str,
                lista_associada: int,
                nota: str = "",
                data: date | None = None,
                tags: set[str] = set(),
                prioridade: int = 0,
                repeticao: int = 0,
                concluida: bool = False) -> None:
        
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
    
    def __str__(self) -> str:
        lines: list[str] = [f"Tarefa: {self.titulo} | ID: {self.id}"]
        lines.append(f"Lista associada: {self.lista_associada}")
        lines.append(f"Nota: {self.nota}")
        if self.data:
            ano, mes, dia = map(int, str(self.data).split("-"))
            lines.append(f"Data: {dia}/{mes}/{ano}")
        else:
            lines.append("Data: ")

        lines.append(f"Tags: {self.tags}")

        match self.prioridade:
            case Prioridade.NENHUMA.value:
                lines.append(f"Prioridade: nenhuma")
            case Prioridade.BAIXA.value:
                lines.append(f"Prioridade: baixa")
            case Prioridade.MEDIA.value:
                lines.append(f"Prioridade: média")
            case Prioridade.ALTA.value:
                lines.append(f"Prioridade: alta")
        
        match self.repeticao:
            case Repeticao.NENHUMA.value:
                lines.append(f"Sem repetição")
            case Repeticao.DIARIA.value:
                lines.append(f"Repetição: diária")
            case Repeticao.SEMANAL.value:
                lines.append("Repetição: semanal")
            case Repeticao.MENSAL.value:
                lines.append("Repetição: mensal")
            case Repeticao.ANUAL.value:
                lines.append("Repetição: anual")
        
        if self.concluida:
            lines.append("Concluída: sim ✓")
        else:
            lines.append("Concluída: não ✗")

        return "\n".join(lines)
    
    def para_dicio(self) -> dict:
        data_json = None
        if self.data:
            data_json = self.data.strftime("%d/%m/%Y")

        return {
            "titulo": self.titulo,
            "nota": self.nota,
            "data": data_json,
            "tags": list(self.tags),
            "lista_associada": self.lista_associada,
            "prioridade": self.prioridade,
            "repeticao": self.repeticao,
            "concluida": self.concluida,
            "id": self.id
        }

if __name__ == "__main__":
    print(Tarefa.id_count)
    the = Tarefa(*([None] * 8))
    print(the.id)
    print(Tarefa.id_count, the.id_count)
    j = Tarefa(*([None] * 8))
    print(the.id, j.id)
    print(Tarefa.id_count, the.id_count, j.id_count)