import os
import sys


# ============================================
#                Classes
# ============================================

class Sonda:
    def __init__(self, bottom_left_corner, top_right_corner, position_ini, direction_ini, movements):
        self.bottom_left_corner = bottom_left_corner
        self.top_right_corner = top_right_corner
        self.position_ini = position_ini
        self.direction_ini = direction_ini
        self.movements = movements

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


def extract_info(info):
    error_msg = 'Por favor, verifique esse parâmetro no arquivo.'
    first_line = info.readline()                                # Lê a primeira linha do arquivo. 
    pxy = [int(s) for s in first_line.split() if s.isdigit()]   # Extrai as coordenadas (x, y) do canto superior direito.
    if len(pxy) != 2:
        sys.exit('Limite superior direito não definido corretamente.\n'+error_msg)

    top_right_corner = (pxy[0], pxy[1])

    sondas = []
    coordenate_check = ['N', 'S', 'E', 'W']
    movements_check = ['M', 'L', 'R']

    for i, line in enumerate(info):                             # Lê as próximas linhas do arquivo em sequencia.
        pxy = [int(s) for s in line.split() if s.isdigit()]     # Extrai as coordenadas (x, y) iniciais da sonda.
        if len(pxy) != 2:
            sys.exit(f'Coordenadas da sonda {i+1} não foram definidas corretamente.\n'+error_msg)         
        if not any(c in line for c in coordenate_check):        # Checa se a sonda possui direção e se está dentro dos padrões definidos.
            sys.exit(f'Direção da sonda {i+1} não foi definida corretamente.\n'+error_msg)
        
        position_ini = (pxy[0], pxy[1])
        direction_ini = [c for c in line.split() if c.isalpha()][0]
        movements_lines = info.readline()                       # Lê a linha seguinte correspondente aos movimentos da sonda.
        movements = [c for c in movements_lines if c.isalpha() and c in movements_check]    # Checa se movimentos estão dentro dos padrões definidos.
        sondas.append(Sonda((0,0), top_right_corner, position_ini, direction_ini, movements))   # Cria um objeto Sonda e adiciona no array de sondas.

    return sondas



# ============================================
#                Main Function
# ============================================

def main():
    filename = get_filename()
    info = open(filename, 'r')

    sondas = extract_info(info)
    
    for i, s in enumerate(sondas):
        print(f'[Sonda {i+1}]')
        print('Limite (x, y) esquerdo inferior:', s.bottom_left_corner)
        print('Limite (x, y) direito superior:', s.top_right_corner)        
        print('Posição (x, y) inicial:', s.position_ini)
        print('Direção inicial:', s.direction_ini)
        print('Lista de movimentos:', s.movements)
        print()

if __name__ == "__main__":
    main()