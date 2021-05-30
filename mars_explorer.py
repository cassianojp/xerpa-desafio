import os
import sys

# ============================================
#                Useful Functions
# ============================================

def get_filename():
    error_msg = 'Por favor, informe o arquivo de coordenadas como parâmetro. Ex.: python mars_explorer.py coordenadas_teste.txt'
    if len(sys.argv) < 2:
        sys.exit(error_msg)
    if not os.path.exists(sys.argv[1]):
        sys.exit(f'Arquivo {sys.argv[1]} não encontrado!\n'+error_msg)
    return sys.argv[1]



# ============================================
#                Main Function
# ============================================

def main():
    filename = get_filename()
    info = open(filename, 'r')
    print(info.readlines())


if __name__ == "__main__":
    main()