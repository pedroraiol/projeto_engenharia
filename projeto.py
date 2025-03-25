import pygame 
import random
import math
from functools import partial
from datetime import datetime, timedelta

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 1024, 1024
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Polygame")

# Cores
BRANCO = (240, 248, 255)
PRETO = (0, 0, 0)
AZUL = (70, 130, 180)
AZUL_ESCURO = (0, 0, 139)
VERDE = (34, 139, 34)
VERMELHO = (220, 20, 60)
CINZA = (200, 200, 200)
AMARELO = (255, 255, 0)
LARANJA = (255, 165, 0)
ROXO = (128, 0, 128)
COR_FUNDO_COLORIDA = (255, 255, 255)
COR_FUNDO_PB = (0, 0, 0)
cores_botoes = [VERDE, AZUL, BRANCO, PRETO, VERMELHO]

# Fontes
try:
    imagem_inicio = pygame.image.load("tela_de_fundo.png")
    imagem_inicio = pygame.transform.scale(imagem_inicio, (1024, 1024))
    print("Imagem carregada com sucesso")
    
    # Carregar imagem do troféu
    try:
        trofeu_img = pygame.image.load("trofeu.png").convert_alpha()
        trofeu_img = pygame.transform.scale(trofeu_img, (200, 200))
    except:
        trofeu_img = None
    
    FONTE = pygame.font.Font(pygame.font.match_font('impact'), 32)
    if not FONTE:
        FONTE = pygame.font.Font(None, 32)

    FONTE_PRINCIPAL = pygame.font.Font(pygame.font.match_font('impact'), 48)
    if not FONTE_PRINCIPAL:
        FONTE_PRINCIPAL = pygame.font.Font(None, 48)
except pygame.error as e:
    print(f"Erro ao carregar a fonte: {e}")
    print(f"Erro ao carregar imagem de início: {e}")
    imagem_inicio = None
    trofeu_img = None
    pygame.quit()
    exit()

# Banco de palavras por nível
palavras = {
    "iniciante": {
        "apple": {"traducao": "maçã", "caixa": 1, "proxima_revisao": datetime.now()},
        "dog": {"traducao": "cachorro", "caixa": 1, "proxima_revisao": datetime.now()},
        "house": {"traducao": "casa", "caixa": 1, "proxima_revisao": datetime.now()},
        "book": {"traducao": "livro", "caixa": 1, "proxima_revisao": datetime.now()},
        "sun": {"traducao": "sol", "caixa": 1, "proxima_revisao": datetime.now()},
        "car": {"traducao": "carro", "caixa": 1, "proxima_revisao": datetime.now()},
        "tree": {"traducao": "árvore", "caixa": 1, "proxima_revisao": datetime.now()},
        "water": {"traducao": "água", "caixa": 1, "proxima_revisao": datetime.now()},
        "moon": {"traducao": "lua", "caixa": 1, "proxima_revisao": datetime.now()},
        "cat": {"traducao": "gato", "caixa": 1, "proxima_revisao": datetime.now()}
    },
    "intermediario": {
        "computer": {"traducao": "computador", "caixa": 1, "proxima_revisao": datetime.now()},
        "chair": {"traducao": "cadeira", "caixa": 1, "proxima_revisao": datetime.now()},
        "table": {"traducao": "mesa", "caixa": 1, "proxima_revisao": datetime.now()},
        "phone": {"traducao": "telefone", "caixa": 1, "proxima_revisao": datetime.now()},
        "window": {"traducao": "janela", "caixa": 1, "proxima_revisao": datetime.now()},
        "door": {"traducao": "porta", "caixa": 1, "proxima_revisao": datetime.now()},
        "school": {"traducao": "escola", "caixa": 1, "proxima_revisao": datetime.now()},
        "teacher": {"traducao": "professor", "caixa": 1, "proxima_revisao": datetime.now()},
        "student": {"traducao": "estudante", "caixa": 1, "proxima_revisao": datetime.now()},
        "country": {"traducao": "país", "caixa": 1, "proxima_revisao": datetime.now()}
    },
    "avancado": {
        "knowledge": {"traducao": "conhecimento", "caixa": 1, "proxima_revisao": datetime.now()},
        "environment": {"traducao": "meio ambiente", "caixa": 1, "proxima_revisao": datetime.now()},
        "government": {"traducao": "governo", "caixa": 1, "proxima_revisao": datetime.now()},
        "technology": {"traducao": "tecnologia", "caixa": 1, "proxima_revisao": datetime.now()},
        "population": {"traducao": "população", "caixa": 1, "proxima_revisao": datetime.now()},
        "education": {"traducao": "educação", "caixa": 1, "proxima_revisao": datetime.now()},
        "international": {"traducao": "internacional", "caixa": 1, "proxima_revisao": datetime.now()},
        "communication": {"traducao": "comunicação", "caixa": 1, "proxima_revisao": datetime.now()},
        "development": {"traducao": "desenvolvimento", "caixa": 1, "proxima_revisao": datetime.now()},
        "responsibility": {"traducao": "responsabilidade", "caixa": 1, "proxima_revisao": datetime.now()}
    }
}

# Variáveis globais
pontuacao = 0
alternativas = []
cor_botao_atual = VERDE
fundo_jogo = BRANCO  
fogos = []
nivel_atual = ""
palavras_usadas = []
english_word = ""
atual_correto = ""

# Classe para partículas de fogos de artifício
class Particula:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor
        self.raio = random.randint(2, 4)
        self.angulo = random.uniform(0, math.pi * 2)
        self.velocidade = random.uniform(2, 6)
        self.tempo_vida = random.randint(20, 40)
    
    def update(self):
        self.x += math.cos(self.angulo) * self.velocidade
        self.y += math.sin(self.angulo) * self.velocidade
        self.tempo_vida -= 1
        self.raio = max(0, self.raio - 0.1)
        return self.tempo_vida > 0
    
    def draw(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), int(self.raio))

# Função para criar fogos de artifício
def criar_fogos(x, y):
    cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    for _ in range(50):
        cor = random.choice(cores)
        fogos.append(Particula(x, y, cor))

# Função para exibir texto na tela com fundo
def exibir_texto_com_fundo(text, font, text_color, bg_color, x, y, padding=10):
    text_surface = font.render(text, True, text_color)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    
    bg_rect = pygame.Rect(x - text_width//2 - padding, y - text_height//2 - padding, 
                         text_width + padding*2, text_height + padding*2)
    
    pygame.draw.rect(tela, bg_color, bg_rect, border_radius=10)
    pygame.draw.rect(tela, PRETO, bg_rect, 2, border_radius=10)
    tela.blit(text_surface, (x - text_width//2, y - text_height//2))
    return bg_rect

# Função para exibir botões na tela
def exibir_botao(text, x, y, w, h, color, hover_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    is_hover = x < mouse[0] < x + w and y < mouse[1] < y + h
    
    button_color = hover_color if is_hover else color
    
    # Cria o retângulo do botão
    button_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(tela, button_color, button_rect, border_radius=10)
    pygame.draw.rect(tela, PRETO, button_rect, 3, border_radius=10)

    text_surface = FONTE.render(text, True, BRANCO)
    text_rect = text_surface.get_rect(center=button_rect.center)
    tela.blit(text_surface, text_rect)

    # Retorna o retângulo para detecção de colisão
    return button_rect

# Função para desenhar a barra de progresso
def desenhar_barra_progresso():
    # Configurações da barra de progresso (centro superior)
    progresso = pontuacao / 10
    barra_width = 300
    barra_height = 20
    barra_x = WIDTH // 2 - barra_width // 2  # Centralizada horizontalmente
    barra_y = 30
    
    # Cores da barra de progresso
    if pontuacao <= 4:
        cor = (255, int(255 * (pontuacao / 4)), 0)  # Vermelho -> Amarelo
    elif pontuacao <= 7:
        cor = (int(255 * (1 - (pontuacao - 4) / 3)), 255, 0)  # Amarelo -> Verde
    else:
        cor = (0, 255, 0)  # Verde
    
    # Desenha a barra de progresso
    pygame.draw.rect(tela, CINZA, (barra_x, barra_y, barra_width, barra_height), border_radius=10)
    pygame.draw.rect(tela, cor, (barra_x, barra_y, int(barra_width * progresso), barra_height), border_radius=10)
    pygame.draw.rect(tela, PRETO, (barra_x, barra_y, barra_width, barra_height), 2, border_radius=10)
    
    # Texto de progresso (acima da barra)
    texto_progresso = FONTE.render(f"Questão: {pontuacao}/10", True, PRETO)
    tela.blit(texto_progresso, (barra_x + (barra_width - texto_progresso.get_width()) // 2, barra_y - 30))

    # Caixa Leitner (centralizada abaixo da barra de progresso)
    caixas = {1:0, 2:0, 3:0, 4:0, 5:0}
    for nivel in palavras:
        for palavra in palavras[nivel]:
            caixas[palavras[nivel][palavra]["caixa"]] += 1
    
    caixa_width = 300  # Largura igual à barra de progresso
    caixa_height = 80
    caixa_x = WIDTH // 2 - caixa_width // 2  # Centralizada horizontalmente
    caixa_y = barra_y + barra_height + 40  # 40 pixels abaixo da barra
    
    # Desenha a caixa Leitner
    pygame.draw.rect(tela, BRANCO, (caixa_x, caixa_y, caixa_width, caixa_height), border_radius=10)
    pygame.draw.rect(tela, AZUL_ESCURO, (caixa_x, caixa_y, caixa_width, caixa_height), 2, border_radius=10)
    
    # Textos centralizados na caixa Leitner
    texto_titulo = FONTE.render("Sistema Leitner", True, AZUL_ESCURO)
    tela.blit(texto_titulo, (caixa_x + (caixa_width - texto_titulo.get_width()) // 2, caixa_y + 10))
    
    texto_caixas = FONTE.render(f"Caixa 1: {caixas[1]}   Caixa 2: {caixas[2]}", True, PRETO)
    tela.blit(texto_caixas, (caixa_x + (caixa_width - texto_caixas.get_width()) // 2, caixa_y + 35))
    
    texto_caixas2 = FONTE.render(f"Caixa 3: {caixas[3]}   Caixa 4: {caixas[4]}", True, PRETO)
    tela.blit(texto_caixas2, (caixa_x + (caixa_width - texto_caixas2.get_width()) // 2, caixa_y + 60))
    
# Tela de resposta errada
def tela_resposta_errada(resposta_correta):
    tela.fill(VERMELHO)
    exibir_texto_com_fundo("Resposta errada!", FONTE_PRINCIPAL, BRANCO, VERMELHO, WIDTH // 2, HEIGHT // 2 - 50)
    exibir_texto_com_fundo(f"A resposta correta era: {resposta_correta}", FONTE_PRINCIPAL, BRANCO, VERMELHO, WIDTH // 2, HEIGHT // 2 + 50)
    pygame.display.update()
    pygame.time.delay(1500)

# Tela de resposta correta
def tela_resposta_correta():
    global fogos
    fogos = []
    criar_fogos(WIDTH // 2, HEIGHT // 3)
    
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < 1500:
        tela.fill(BRANCO)
        
        fogos = [fogo for fogo in fogos if fogo.update()]
        for fogo in fogos:
            fogo.draw(tela)
        
        exibir_texto_com_fundo("Parabéns! Resposta correta!", FONTE_PRINCIPAL, VERDE, BRANCO, WIDTH // 2, HEIGHT // 2)
        
        pygame.display.update()
        clock.tick(30)

# Atualiza a caixa da palavra no sistema Leitner
def atualizar_caixa(palavra, nivel, acertou):
    """Atualiza a caixa da palavra baseado no desempenho"""
    if acertou:
        # Move para uma caixa superior (revisão menos frequente)
        palavras[nivel][palavra]["caixa"] = min(palavras[nivel][palavra]["caixa"] + 1, 5)
    else:
        # Retorna para a caixa 1 (revisão mais frequente)
        palavras[nivel][palavra]["caixa"] = 1
    
    # Define quando a palavra deve aparecer novamente
    intervalos = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}  # dias até próxima revisão
    palavras[nivel][palavra]["proxima_revisao"] = datetime.now() + timedelta(days=intervalos[palavras[nivel][palavra]["caixa"]])

# Seleciona a próxima palavra baseado no sistema Leitner
def obter_proxima_palavra():
    agora = datetime.now()
    
    # 1. Palavras que estão atrasadas para revisão
    atrasadas = [p for p in palavras if palavras[p]["proxima_revisao"] <= agora]
    
    # 2. Se não houver atrasadas, pegue as da caixa 1
    if not atrasadas:
        atrasadas = [p for p in palavras if palavras[p]["caixa"] == 1]
    
    # 3. Se ainda não houver, pegue qualquer palavra
    if not atrasadas:
        atrasadas = list(palavras.keys())
    
    return random.choice(atrasadas)

# Função para verificar a resposta
def verificar_resposta(resposta_selecionada, palavra_ingles, resposta_correta, nivel):
    global pontuacao, alternativas
    
    if resposta_selecionada == resposta_correta:
        atualizar_caixa(palavra_ingles, nivel, True)
        pontuacao += 1
        tela_resposta_correta()
    else:
        atualizar_caixa(palavra_ingles, nivel, False)
        tela_resposta_errada(resposta_correta)
    
    alternativas = []  # Limpa as alternativas para que uma nova palavra seja selecionada

# Função para criar a tela inicial
def tela_inicial():
    esperando = True
    clock = pygame.time.Clock()
    
    # Caixa de explicação do método Leitner
    explicacao = [
        "Método Leitner:",
        "1. Cartões começam na Caixa 1",
        "2. Acertou? Avança para próxima caixa",
        "3. Errou? Volta para a Caixa 1",
        "4. Caixas maiores = menos revisões"
    ]
    
    # Criar uma fonte menor para a explicação
    try:
        fonte_explicacao = pygame.font.Font(pygame.font.match_font('arial'), 20)
    except:
        fonte_explicacao = pygame.font.Font(None, 20)

    while esperando:
        tela.fill(BRANCO)
        
        if imagem_inicio:
            tela.blit(imagem_inicio, (0, 0))
        
        # Caixa de explicação (tamanho ajustado)
        caixa_width = 350
        caixa_height = 180
        caixa_x = 50
        caixa_y = 50
        
        # Desenha caixa de explicação
        pygame.draw.rect(tela, BRANCO, (caixa_x, caixa_y, caixa_width, caixa_height), border_radius=10)
        pygame.draw.rect(tela, AZUL_ESCURO, (caixa_x, caixa_y, caixa_width, caixa_height), 2, border_radius=10)
        
        # Centraliza cada linha de texto na caixa
        for i, linha in enumerate(explicacao):
            texto = fonte_explicacao.render(linha, True, PRETO)
            texto_x = caixa_x + (caixa_width - texto.get_width()) // 2  # Centraliza horizontalmente
            texto_y = caixa_y + 30 + i * 30  # Espaçamento vertical
            tela.blit(texto, (texto_x, texto_y))
        
        # Botões de nível (mantidos como antes)
        botao_iniciante = exibir_botao("Iniciante", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, VERDE, (100, 200, 100))
        botao_intermediario = exibir_botao("Intermediário", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, AZUL, (100, 100, 200))
        botao_avancado = exibir_botao("Avançado", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, VERMELHO, (200, 100, 100))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if botao_iniciante.collidepoint(pos_mouse):
                    return "iniciante"
                elif botao_intermediario.collidepoint(pos_mouse):
                    return "intermediario"
                elif botao_avancado.collidepoint(pos_mouse):
                    return "avancado"
        
        clock.tick(30)
        
# Função para obter próxima palavra adaptada para o nível
def obter_proxima_palavra(nivel):
    global palavras_usadas, english_word, atual_correto
    
    agora = datetime.now()
    palavras_disponiveis = [p for p in palavras[nivel] 
                           if p not in palavras_usadas and 
                           palavras[nivel][p]["proxima_revisao"] <= agora]
    
    if not palavras_disponiveis:
        palavras_disponiveis = [p for p in palavras[nivel] if p not in palavras_usadas]
    
    if not palavras_disponiveis:
        # Todas as palavras foram usadas, reinicia
        palavras_usadas = []
        palavras_disponiveis = list(palavras[nivel].keys())
    
    english_word = random.choice(palavras_disponiveis)
    atual_correto = palavras[nivel][english_word]["traducao"]
    palavras_usadas.append(english_word)
    
    return english_word

# Tela de parabéns
def tela_parabens(nivel):
    global fogos, trofeu_img
    
    fogos = []
    clock = pygame.time.Clock()
    
    # Criar fogos de artifício para celebração
    for _ in range(15):
        criar_fogos(random.randint(100, WIDTH-100), random.randint(100, HEIGHT//2))
    
    # Configurar fonte estilo conquista
    try:
        fonte_parabens = pygame.font.Font("PressStart2P-Regular.ttf", 24)
        fonte_nivel = pygame.font.Font("PressStart2P-Regular.ttf", 36)
    except:
        fonte_parabens = pygame.font.SysFont("Arial", 24, bold=True)
        fonte_nivel = pygame.font.SysFont("Arial", 36, bold=True)
    
    # Textos da conquista
    nivel_texto = nivel.upper() + "!"
    texto_conquista = fonte_parabens.render("CONQUISTA DESBLOQUEADA!", True, AMARELO)
    texto_nivel = fonte_nivel.render(nivel_texto, True, LARANJA)
    
    # Posicionamento lado a lado (troféu + texto)
    if trofeu_img:
        # Centraliza o conjunto troféu + texto
        conjunto_width = trofeu_img.get_width() + 20 + max(texto_conquista.get_width(), texto_nivel.get_width())
        inicio_x = WIDTH // 2 - conjunto_width // 2
        
        trofeu_x = inicio_x
        trofeu_y = HEIGHT // 2 - trofeu_img.get_height() // 2
        
        texto_x = trofeu_x + trofeu_img.get_width() + 20
        texto_y = HEIGHT // 2 - texto_nivel.get_height() // 2
    
    waiting = True
    while waiting:
        tela.fill(BRANCO)
        
        # Efeitos de fogos
        fogos = [fogo for fogo in fogos if fogo.update()]
        for fogo in fogos:
            fogo.draw(tela)
        
        if random.random() < 0.15:
            criar_fogos(random.randint(100, WIDTH-100), random.randint(100, HEIGHT//2))
        
        # Desenha o troféu e textos lado a lado
        if trofeu_img:
            tela.blit(trofeu_img, (trofeu_x, trofeu_y))
        
            # Texto de conquista
            tela.blit(texto_conquista, (texto_x, texto_y - 30))
            
            # Texto do nível com efeito de brilho
            pygame.draw.rect(tela, (50, 50, 50), (texto_x - 5, texto_y + 25, texto_nivel.get_width() + 10, texto_nivel.get_height() + 10), border_radius=5)
            tela.blit(texto_nivel, (texto_x, texto_y + 30))
        
        # Botão de continuar
        botao_rect = exibir_botao("Continuar", WIDTH // 2 - 100, HEIGHT - 150, 200, 50, VERDE, (100, 255, 100))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(event.pos):
                    return
        
        clock.tick(30)

# Função para reiniciar o jogo
def recomeçar_jogo():
    global pontuacao, alternativas, fogos
    pontuacao = 0
    alternativas = []
    fogos = []
    main()

# Função principal do jogo
def main():    
    global pontuacao, alternativas, cor_botao_atual, fogos, nivel_atual, palavras_usadas
    
    nivel_atual = tela_inicial()
    clock = pygame.time.Clock()
    running = True
    palavras_usadas = []
    
    while running:
        if pontuacao >= 10:
            tela_parabens(nivel_atual)
            recomeçar_jogo()
            return

        tela.fill(fundo_jogo)

        # Obter próxima palavra do nível atual
        if not alternativas:
            english_word = obter_proxima_palavra(nivel_atual)
            atual_correto = palavras[nivel_atual][english_word]["traducao"]
            
            # Prepara as alternativas
            alternativas = [atual_correto]
            while len(alternativas) < 4:
                palavra_aleatoria = random.choice([p["traducao"] for p in palavras[nivel_atual].values()])
                if palavra_aleatoria not in alternativas:
                    alternativas.append(palavra_aleatoria)
            random.shuffle(alternativas)

        desenhar_barra_progresso()
        
        espacamento_vertical = 60
        exibir_texto_com_fundo("Traduza a palavra:", FONTE, PRETO, cor_botao_atual, WIDTH // 2, HEIGHT // 2 - 2*espacamento_vertical)
        exibir_texto_com_fundo(english_word, FONTE_PRINCIPAL, PRETO, cor_botao_atual, WIDTH // 2, HEIGHT // 2 - espacamento_vertical//2)

        botao_largura, botao_altura = 200, 50
        espacamento_horizontal = 20
        base_y = HEIGHT // 2 + espacamento_vertical//2
        
        # Lista para armazenar os retângulos dos botões
        botoes_rect = []
        
        for i, alternativa in enumerate(alternativas):
            botao_x = (WIDTH - botao_largura * 2 - espacamento_horizontal) // 2 + (i % 2) * (botao_largura + espacamento_horizontal)
            botao_y = base_y + (i // 2) * (botao_altura + espacamento_horizontal)
            
            # Armazena o retângulo do botão
            rect = exibir_botao(alternativa, botao_x, botao_y, botao_largura, botao_altura,
                              cor_botao_atual, CINZA)
            botoes_rect.append((rect, alternativa))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, alternativa in botoes_rect:
                    if rect.collidepoint(mouse_pos):
                        verificar_resposta(alternativa, english_word, atual_correto, nivel_atual)
                        break

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()