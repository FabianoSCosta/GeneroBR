from utils import *

def main():
    
    createtable()
    nome = input("Digite um nome: ")
    sexo = genero(nome)
    print(f"O sexo de maior ocorrência associado ao nome {nome} é {sexo}.")
    input("Aperte qualquer tecla para sair")

if __name__ == "__main__":
    main()