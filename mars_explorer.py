import os
import sys

# ============================================
#                Classes
# ============================================

class Sonda:
    def __init__(self, id, bottom_left_corner, top_right_corner, position_ini, direction_ini, movements):
        self.id = id                                    # Identificador da sonda.
        self.bottom_left_corner = bottom_left_corner    # Limite inferior esquerdo do planalto.
        self.top_right_corner = top_right_corner        # Limite superior direito do planalto.
        self.position_ini = position_ini                # Posição inicial (x, y) da sonda.
        self.position_current = position_ini            # Posição atual (x, y) da sonda.
        self.direction_ini = direction_ini              # Direção inicial da sonda.
        self.direction_current = direction_ini          # Direção atual da sonda.
        self.movements = movements                      # Lista de movimentos a ser executada pela sonda.
    

    def go_forward(self):
        x = 0               # x e y tem a função apenas de índice para os arrays de posição.
        y = 1
        if self.direction_current == 'N':
            self.position_current[y] += 1       # Incrementa a posição y da sonda.
            if self.position_current[y] > self.top_right_corner[y]:     # Checa se o avanço não ultrapassou as restrições de limite.
                sys.exit(f'Coordenadas da sonda {self.id} ultrapassaram o limite superior do planalto.')
        elif self.direction_current == 'S':
            self.position_current[y] -= 1       # Decrementa a posição y da sonda.
            if self.position_current[y] < self.bottom_left_corner[y]:   # Checa se o avanço não ultrapassou as restrições de limite.
                sys.exit(f'Coordenadas da sonda {self.id} ultrapassaram o limite inferior do planalto.')  
        elif self.direction_current == 'E':
            self.position_current[x] += 1       # Incrementa a posição x da sonda.
            if self.position_current[x] > self.top_right_corner[x]:     # Checa se o avanço não ultrapassou as restrições de limite.
                sys.exit(f'Coordenadas da sonda {self.id} ultrapassaram o limite direito do planalto.')            
        elif self.direction_current == 'W':
            self.position_current[x] -= 1       # Decrementa a posição x da sonda.
            if self.position_current[x] < self.bottom_left_corner[x]:   # Checa se o avanço não ultrapassou as restrições de limite.
                sys.exit(f'Coordenadas da sonda {self.id} ultrapassaram o limite esquerdo do planalto.')              


    def process_command(self, m):
        directions = ['N', 'E', 'S', 'W']
        num_of_directions = len(directions)
        index = directions.index(self.direction_current)        # Pega o index da posição atual da sonda no array de direções.

        if m == 'M':                                            # Se commando = M, incrementa uma posição na direção atual.
            self.go_forward()

        elif m =='L':
            index -= 1                                          # Se commando = L, rotaciona index de direções para à esquerda.
            if index < 0:
                index = num_of_directions - 1
            self.direction_current = directions[index]

        elif m == 'R':                                          # Se commando = R, rotaciona index de direções para à direita.
            index += 1
            if index > num_of_directions - 1:
                index = 0
            self.direction_current = directions[index]


    def move(self):                                             # Executa os movimentos da sonda em sequencia.
        for m in self.movements:
            self.process_command(m)

    

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
    first_line = info.readline()                                            # Lê a primeira linha do arquivo. 
    top_right_corner = [int(s) for s in first_line.split() if s.isdigit()]  # Extrai as coordenadas (x, y) do canto superior direito.
    if len(top_right_corner) != 2:                                          # Checa se a sonda possui informação de limite superior direito e se está dentro dos padrões definidos.
        sys.exit('Limite superior direito não definido corretamente.\n'+error_msg)

    sondas = []
    coordenate_check = ['N', 'E', 'S', 'W']
    movements_check = ['M', 'L', 'R']

    for i, line in enumerate(info):                                                                 # Lê as próximas linhas do arquivo em sequencia.
        id = i+1
        position_ini = [int(s) for s in line.split() if s.isdigit()]                                # Extrai as coordenadas (x, y) iniciais da sonda.
        if len(position_ini) != 2:                                                                  # Checa se a sonda possui informação de posição inical e se está dentro dos padrões definidos.
            sys.exit(f'Coordenadas da sonda {id} não foram definidas corretamente.\n'+error_msg)         
        if not any(c in line for c in coordenate_check):                                            # Checa se a sonda possui informação de direção e se está dentro dos padrões definidos.
            sys.exit(f'Direção da sonda {id} não foi definida corretamente.\n'+error_msg)

        direction_ini = [c for c in line.split() if c.isalpha()][0]
        movements_lines = info.readline()                                                           # Lê a linha seguinte correspondente aos movimentos da sonda.
        movements = [c for c in movements_lines if c.isalpha() and c in movements_check]            # Checa se movimentos estão dentro dos padrões definidos.
        sondas.append(Sonda(id, [0,0], top_right_corner, position_ini, direction_ini, movements))   # Cria um objeto Sonda e adiciona no array de sondas.

    return sondas



# ============================================
#                Main Function
# ============================================

def main():
    filename = get_filename()
    info = open(filename, 'r')

    sondas = extract_info(info)         # Extração e estruturação dos dados do arquivo de entrada.

    x = 0       # x e y tem a função apenas de índice para os arrays de posição.
    y = 1
    
    for i, s in enumerate(sondas):      # Execução sequencial dos movimentos de cada sonda.
        # print(f'[Sonda {i+1}]')
        # print('Limite (x, y) esquerdo inferior:', s.bottom_left_corner)
        # print('Limite (x, y) direito superior:', s.top_right_corner)        
        # print('Posição (x, y) inicial:', s.position_ini)
        # print('Direção inicial:', s.direction_ini)
        # print('Lista de movimentos:', s.movements)
        s.move()
        print(s.position_current[x], s.position_current[y], s.direction_current)    # Saída para o console das posições finais das sondas.

if __name__ == "__main__":
    main()