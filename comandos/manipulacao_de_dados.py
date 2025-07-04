from datetime import date
import json
from classes.lista import ListaDeTarefas
from classes.tarefa import Tarefa
import terminal_utils as trm

listas: list[ListaDeTarefas] = []
arquivo: str = "tarefas.json"

def salvar_dados() -> None:
    dados = {}
    for l in listas:
        tarefas_l = []
        for t in l.tarefas:
            tarefas_l.append(t.para_dicio())
        dados[l.titulo] = tarefas_l
    
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

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
        return nova_lista
    except FileNotFoundError:
        print(trm.bold("Começando com um arquivo vazio"))
        listas = [ListaDeTarefas("Cuba")]
    except json.JSONDecodeError:
        print(trm.bold("Começando com um arquivo vazio"))
        listas = [ListaDeTarefas("Cuba")]

def salvar_mudanças():
    while True:
        c = input("Salvar mudanças? (S/N): ")
        if c == "S" or c == "s":
            salvar_dados()
            print("Feito :D")
            return
        elif c == "N" or c == "n":
            print("Ação cancelada")
            return
        else:
            print("Digite S ou N")

carregar_dados()