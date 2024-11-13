# Algoritmo Fillpoly
 Algoritmo para Preenchimento de Polígonos Fillpoly

1. Descrição:

    Este algoritmo é utilizado para preencher a área interna de um polígono. O preenchimento é feito processando o polígono linha por linha, identificando as interseções das arestas do polígono com cada scanline e preenchendo os pixels entre os pares de interseções.
    O cálculo das interseções começa no menor valor de y (ymin) e vai até o maior valor de y (ymax). Para determinar a próxima interseção em x, o algoritmo utiliza o inverso do coeficiente angular. A cada passo, o valor de y é incrementado em 1, e o valor de x é ajustado de acordo com o coeficiente angular.
    As interseções são armazenadas em uma tabela de arestas. Ao final, as interseções são ordenadas em ordem crescente de x, e para cada par de interseções em uma mesma scanline, os pixels entre elas são preenchidos.

2. Tecnologias Usadas:
    - Python 3.x.
    - Pygame: Biblioteca para renderização gráfica e interação do usuário com a interface.

3. Requisitos:

    É necessério os seguintes requisitos para a execução do programa:

3.1. Instalação do Python:
   - Linux:

         sudo apt update
         sudo apt install python3
       
   - Windows:
     
        - Baixe o instalador no site oficial https://www.python.org/downloads/
        - Marque a opção "Add Python to PATH"

3.2. Certifique-se que o pip esteja instalado:

    pip --version

3.3. Instale o Pygame:

    pip install pygame
    
3.4. Requisitos de Sistema:

   - Sistema Operacional: Linux ou Windows
   - Memória RAM: 2 GB ou mais
   - Processador: Dual-core ou superior
   - Espaço em disco: 200 MB livres

4. Instruções de Uso:

4.1. Abra o terminal no diretório do programa e execute:

    python main.py

4.2. Comandos:

   - Botão esquerdo do mouse: cria um vértice (Dentro da tela de desenho, abaixo do menu)
   - Botão direito do mmouse: Fecha o polígono (se houver ao menos 3 vértices)
   - Botão do meio do mouse: Seleciona um polígono (Clique dentro do polígono para selecionar e fora do polígono para deselecionar)
   - Teclas Delete / Backspace: Exclui um polígono selecionado
   - Menu:
     - Clique em cima dos botões de cores para alterar a cor (RGB);
     - Clique no botão 'Pintar Arestas' para ativar (verde) / desativar (vermelho) a pintura de arestas.
