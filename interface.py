import pygame
from poligono import Poligono

class Interface:
    def __init__(self, largura=1280, altura=720):
        # Inicialização do Pygame
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Preenchimento de Polígonos Fillpoly")
        self.clock = pygame.time.Clock()
        
        self.poligonos = []  # Lista de todos os polígonos desenhados
        self.poligono_atual = Poligono()  # Polígono que está sendo desenhado
        self.cor_selecionada = (255, 255, 255)
        self.poligono_selecionado = None  # Armazena o polígono selecionado
        self.selecionar_arestas = True  # Flag para pintar as arestas

        # Configuração do seletor de cores
        self.r = 255
        self.g = 255
        self.b = 255

        # Inicializa a fonte para os textos
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)

    # Função que exibe o menu 
    def exibir_menu_cores(self):
        
        # Seletor de cor RGB
        texto_seletor_cores = self.font.render('Seletor Cores:', True, (255, 255, 255))
        self.tela.blit(texto_seletor_cores, (10, 10))
        pygame.draw.rect(self.tela, (self.r, 0, 0), pygame.Rect(150, 10, 40, 40))
        pygame.draw.rect(self.tela, (0, self.g, 0), pygame.Rect(200, 10, 40, 40))
        pygame.draw.rect(self.tela, (0, 0, self.b), pygame.Rect(250, 10, 40, 40))
        
        # Exibe a cor selecionada
        texto_seletor_cores = self.font.render('Cor:', True, (255, 255, 255))
        self.tela.blit(texto_seletor_cores, (300, 10))
        pygame.draw.rect(self.tela, (self.r, self.g, self.b), pygame.Rect(350, 10, 40, 40))

        # Botão para mostrar/ocultar as arestas
        texto_arestas = self.font.render('Pintar Arestas:', True, (255, 255, 255))
        self.tela.blit(texto_arestas, (420, 10))
        if self.selecionar_arestas:
            pygame.draw.rect(self.tela, (0, 255, 0), pygame.Rect(570, 10, 40, 40))  # Verde para mostrar
        else:
            pygame.draw.rect(self.tela, (255, 0, 0), pygame.Rect(570, 10, 40, 40))  # Vermelho para ocultar
            
        # Texto sobre a exclusão de polígonos
        texto_seletor_cores = self.font.render('Deletar Polígono: Delete / Backspace', True, (255, 255, 255))
        self.tela.blit(texto_seletor_cores, (700, 10))
        
    # Função que processa os cliques dentro da área do menu
    def processar_clique_menu(self, pos):

        if 150 <= pos[0] <= 190:  # Incrementa o valor de R
            self.r = (self.r + 15) % 256
        elif 200 <= pos[0] <= 240:  # Incrementa o valor de G
            self.g = (self.g + 15) % 256
        elif 250 <= pos[0] <= 290:  # Incrementa o valor de B
            self.b = (self.b + 15) % 256
        elif 570 <= pos[0] <= 610:  # Botão de arestas
            self.selecionar_arestas = not self.selecionar_arestas

        # Atualiza a cor selecionada
        self.cor_selecionada = (self.r, self.g, self.b)

        # Se um polígono estiver selecionado, altera sua cor
        if self.poligono_selecionado:
            self.poligono_selecionado.cor = self.cor_selecionada
            self.poligono_selecionado.cor_original = self.cor_selecionada

    # Loop principal do programa
    def rodar(self):
        rodando = True
        while rodando:
            self.clock.tick(60)  # Limita a 60 FPS
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if evento.button == 1:  # Clique esquerdo
                        if pos[1] <= 60:  # Menu
                            self.processar_clique_menu(pos)
                            
                        else:
                            self.poligono_atual.adicionar_vertice(pos)
                    elif evento.button == 2:  # Clique do meio para seleção
                        self.poligono_selecionado = None
                        # Percorre a lista de polígonos de trás para a frente para selecionar o polígono de cima
                        for poligono in reversed(self.poligonos):
                            if poligono.ponto_dentro(pos):
                                self.poligono_selecionado = poligono
                                break
                    elif evento.button == 3:  # Clique direito para finalizar o polígono
                        # Finaliza o polígono atual e o adiciona à lista de polígonos
                        if len(self.poligono_atual.vertices) >= 3:
                            self.poligono_atual.cor = self.cor_selecionada
                            self.poligono_atual.cor_original = self.cor_selecionada
                            self.poligono_atual.rasteriza_poligono()
                            self.poligonos.append(self.poligono_atual)
                            self.poligono_atual = Poligono()
                            
                elif evento.type == pygame.KEYDOWN:
                    # Exclui o polígono
                    if evento.key == pygame.K_DELETE or evento.key == pygame.K_BACKSPACE:
                        if self.poligono_selecionado:
                            self.poligonos.remove(self.poligono_selecionado)
                            self.poligono_selecionado = None

            # Desenha tela e os elementos
            self.tela.fill((0, 0, 0))  # Limpa a tela
            
            # Desenha todos os polígonos preenchidos e suas arestas
            for poligono in self.poligonos:
                if poligono.preenchido:
                    poligono.preenchimento(self.tela)
                    cor_arestas = (255, 255, 0) if not self.selecionar_arestas else poligono.cor_original
                    poligono.desenha_arestas(self.tela, True, cor_arestas)

            # Mostra os vértices criados e as arestas
            if len(self.poligono_atual.vertices) > 0:
                if len(self.poligono_atual.vertices) > 1:
                    pygame.draw.lines(self.tela, (255, 255, 0), False, self.poligono_atual.vertices, 1)
                for vert in self.poligono_atual.vertices:
                    pygame.draw.circle(self.tela, (255, 0, 0), vert, 3)

            # Desenhar linha de separação entre o menu e a área de pintura
            pygame.draw.line(self.tela, (255, 255, 255), (0, 60), (self.largura, 60), 2)

            self.exibir_menu_cores()
            pygame.display.flip()

        pygame.quit()