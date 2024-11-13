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
        
        ymin_global = int(min(p[1] for p in self.vertices))
        ymax_global = int(max(p[1] for p in self.vertices))

        # Inicializar a lista de arestas que serão processadas
        n = len(self.vertices)
        aresta_proc = {y: [] for y in range(ymin_global, ymax_global + 1)}
        # Processar cada par de vértices e adicionar as arestas à lista de processamento direto
        for i in range(n):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
    
            # Ignorar arestas horizontais
            if p1[1] == p2[1]:
                continue

            # Definir ymin, ymax, x inicial e Tx
            if p1[1] < p2[1]:
                ymin, ymax = int(p1[1]), int(p2[1])
                x = p1[0]
                Tx = (p2[0] - p1[0]) / (p2[1] - p1[1])
            else:
                ymin, ymax = int(p2[1]), int(p1[1])
                x = p2[0]
                Tx = (p1[0] - p2[0]) / (p1[1] - p2[1])

            for y in range(ymin, ymax):
                aresta_proc[y].append(x)
                x += Tx
            
        for y, intersecoes in aresta_proc.items():
            intersecoes.sort()  # Organizar interseções em ordem crescente de x
        
            # Processar em pares e adicionar à lista de scanlines
            for j in range(0, len(intersecoes) - 1, 2):
                x_ini = int(round(intersecoes[j]))
                x_fim = int(round(intersecoes[j + 1]))
                self.scanlines.append((y, x_ini, x_fim))
                
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