import pygame

class Poligono:
    def __init__(self, cor=(255, 255, 255)):
        self.vertices = []
        self.cor = cor  # Cor de preenchimento
        self.preenchido = False  # Flag para indicar se foi preenchido
        self.scanlines = []  # Lista de scanlines preenchidas: (y, x_ini, x_fim)
        self.cor_original = (255, 255, 255)

    # Adiciona um vértice a lista de vértices
    def adicionar_vertice(self, ponto):
        self.vertices.append(ponto)

    # Desenha as arestas na tela
    def desenha_arestas(self, tela, mostrar_aresta, cor_arestas=(255, 255, 0)):
        if len(self.vertices) > 1:
            pygame.draw.lines(tela, cor_arestas, mostrar_aresta, self.vertices, 1)

    # Faz a pintura do polígonos de acordo com a lista de scanlines
    def preenchimento(self, tela):
        for (y, x_start, x_end) in self.scanlines:
            pygame.draw.line(tela, self.cor, (x_start, y), (x_end, y))
    
    # Percorre os polígonos a partir do ymin até o ymax
    # Utiliza aritmética incremental para calcular as posições das interseções das arestas do polígono com as linhas de varredura
    def rasteriza_poligono(self):
        if len(self.vertices) < 3:
            print("Polígono inválido: menos de 3 vértices.")
            return  # Não é um polígono válido

        # Limpa as scanlines anteriores
        self.scanlines = []

        # Encontra o Y mínimo e o Y máximo
        ymin_global = min(int(p[1]) for p in self.vertices)
        ymax_global = max(int(p[1]) for p in self.vertices)

        #print(f"Preenchendo polígono: Y_min={y_min}, Y_max={y_max}")

        # Constrói a Tabela de Arestas
        tabela_arestas = [[] for _ in range(ymax_global - ymin_global + 1)]
        n = len(self.vertices)
        for i in range(n):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % n] # Garante que o último vértice seja conectado de volta ao primeiro

            if p1[1] == p2[1]:
                continue  # Ignorar arestas horizontais
            # Determina que o ponto inicial da aresta (ymin) seja sempre o ponto com o menor valor de y
            if p1[1] < p2[1]:
                ymin = int(p1[1])
                ymax = int(p2[1])
                x = p1[0]
                Tx = (p2[0] - p1[0]) / (p2[1] - p1[1])
            else:
                ymin = int(p2[1])
                ymax = int(p1[1])
                x = p2[0]
                Tx = (p1[0] - p2[0]) / (p1[1] - p2[1])

            tabela_arestas[ymin - ymin_global].append({'ymax': ymax, 'x': x, 'Tx': Tx})

        # Inicializar a tabela das arestas que intersectam cada scanline
        aresta_proc = []

        # Processa cada scanline de ymin_global até ymax_global
        for y in range(ymin_global, ymax_global + 1):
            
            aux = []
            
            # Adiciona todas as arestas da tabela_arestas que começam na scanline atual
            if y - ymin_global < len(tabela_arestas):
                for aresta in tabela_arestas[y - ymin_global]:
                    aresta_proc.append(aresta)
               
            # Remove arestas da aresta_proc onde y >= ymax
            for aresta in aresta_proc:
                if aresta['ymax'] > y:
                    aux.append(aresta)
            aresta_proc = aux

            # Ordenar a aresta_proc em ordem crescente pela coordenada x
            aresta_proc.sort(key=lambda aresta: aresta['x'])

            # Adiciona pares de intersecções de cada scanline que será pintada à lista scanline
            for i in range(0, len(aresta_proc), 2):
                if i + 1 >= len(aresta_proc):
                    break
                x_ini = int(round(aresta_proc[i]['x']))
                x_fim = int(round(aresta_proc[i + 1]['x']))
                self.scanlines.append((y, x_ini, x_fim)) # Armazena o intervalo que será pintado

            # Atualizar x para as arestas na aresta_proc usando o inverso da inclinação
            for aresta in aresta_proc:
                aresta['x'] += aresta['Tx']

        self.preenchido = True

    # A função determina se um ponto está dentro de um polígono
    # A implementação utiliza o método Ray Casting (também chamado de Even–odd rule)
    def ponto_dentro(self, ponto):
        x, y = ponto
        n = len(self.vertices)
        inside = False

        for i in range(n):
            ax, ay = self.vertices[i]
            bx, by = self.vertices[(i + 1) % n]
            # Testa se o ponto está entre as coordenadas y da aresta
            if ((ay > y) != (by > y)):
                intersect_x = (bx - ax) * (y - ay) / (by - ay + 1e-10) + ax # soma 1e-10 para evitar divisão por zero
                # Verifica se o ponto está à esquerda da interseção
                if x < intersect_x:
                    inside = not inside # Muda a flag

        return inside