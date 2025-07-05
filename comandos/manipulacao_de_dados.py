from datetime import date
import json
from classes.lista import ListaDeTarefas
from classes.tarefa import Tarefa
import terminal_utils as trm

listas: list[ListaDeTarefas] = [] # Inicializa uma lista global para armazenar objetos ListaDeTarefas
arquivo: str = "tarefas.json"

def salvar_dados() -> None:
    """ Salva os dados das listas de tarefas em um arquivo JSON. """
    dados = {}
    for l in listas:
        tarefas_l = []
        for t in l.tarefas:
            tarefas_l.append(t.para_dicio()) # Converte cada tarefa em um dicionário
        dados[l.titulo] = tarefas_l # Armazena as tarefas sob o título da lista
    
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

def carregar_dados() -> None:
    """ Carrega os dados das listas de tarefas de um arquivo JSON. """
    global listas
    try:
        with open(arquivo, "r") as f:
            dados_carregados = json.load(f)
    
        listas = []

        # Itera sobre os dados carregados para recriar as listas e tarefas
        for titulo_lista, dados_tarefas in dados_carregados.items():
            nova_lista = ListaDeTarefas(titulo_lista)
            for tarefa_dict in dados_tarefas:
                data_str = tarefa_dict.get("data")
                data_obj = None
                if data_str:
                    dia, mes, ano = map(int, data_str.split("/"))
                    data_obj = date(ano, mes, dia)
                
                # Cria um novo objeto Tarefa com os dados carregados
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
    """ Pergunta ao usuário se deseja salvar as mudanças, retornando True ou False.  """
    while True:
        c = input("Salvar mudanças? (S/N): ")
        if c == "S" or c == "s":
            return True
        elif c == "N" or c == "n":
            print("Ação cancelada")
            return False
        else:
            print("Digite S ou N")

carregar_dados()