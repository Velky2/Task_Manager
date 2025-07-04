from comandos.manipulacao_de_dados import listas

def ver_lista(*titulo) -> None:
    titulo: str = " ".join(titulo).strip('"').lower()
    if not titulo:
        print('Uso: ver lista "Titulo da Lista"')
        print("Listas disponiveis:", end="\n   ")
        print(*(f'("{lista.titulo}" - ID: {lista.id})' for lista in listas), sep=" | ")
        return
    
    for lista in listas:
        if titulo == "".join(lista.titulo).lower():
            print(lista)
            break

def ver_listas() -> None:
    # TODO: make it more robust
    print(*(f'("{lista.titulo}" - ID: {lista.id})' for lista in listas), sep=" | ")

def ver_tudo() -> None:
    print()
    print("\n\n".join(str(lista) for lista in listas))
