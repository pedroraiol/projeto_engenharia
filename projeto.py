import pygame 
import random
import math
import sys
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
    fundo_perguntas = pygame.image.load("fundo_perguntas.png").convert()
    fundo_perguntas = pygame.transform.scale(fundo_perguntas, (WIDTH, HEIGHT))
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
    fundo_perguntas = None
    pygame.quit()
    exit()

# Banco de palavras por nível e idioma
palavras = {
    "inglês": {
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
            "cat": {"traducao": "gato", "caixa": 1, "proxima_revisao": datetime.now()},
            "flower": {"traducao": "flor", "caixa": 1, "proxima_revisao": datetime.now()},
            "bird": {"traducao": "pássaro", "caixa": 1, "proxima_revisao": datetime.now()},
            "fish": {"traducao": "peixe", "caixa": 1, "proxima_revisao": datetime.now()},
            "hand": {"traducao": "mão", "caixa": 1, "proxima_revisao": datetime.now()},
            "foot": {"traducao": "pé", "caixa": 1, "proxima_revisao": datetime.now()}
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
            "country": {"traducao": "país", "caixa": 1, "proxima_revisao": datetime.now()},
            "city": {"traducao": "cidade", "caixa": 1, "proxima_revisao": datetime.now()},
            "hospital": {"traducao": "hospital", "caixa": 1, "proxima_revisao": datetime.now()},
            "restaurant": {"traducao": "restaurante", "caixa": 1, "proxima_revisao": datetime.now()},
            "supermarket": {"traducao": "supermercado", "caixa": 1, "proxima_revisao": datetime.now()},
            "library": {"traducao": "biblioteca", "caixa": 1, "proxima_revisao": datetime.now()}
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
            "responsibility": {"traducao": "responsabilidade", "caixa": 1, "proxima_revisao": datetime.now()},
            "globalization": {"traducao": "globalização", "caixa": 1, "proxima_revisao": datetime.now()},
            "sustainability": {"traducao": "sustentabilidade", "caixa": 1, "proxima_revisao": datetime.now()},
            "innovation": {"traducao": "inovação", "caixa": 1, "proxima_revisao": datetime.now()},
            "democracy": {"traducao": "democracia", "caixa": 1, "proxima_revisao": datetime.now()},
            "revolution": {"traducao": "revolução", "caixa": 1, "proxima_revisao": datetime.now()}
        }
    },
    "russo": {
        "iniciante": {
            "яблоко": {"traducao": "maçã", "caixa": 1, "proxima_revisao": datetime.now()},
            "собака": {"traducao": "cachorro", "caixa": 1, "proxima_revisao": datetime.now()},
            "дом": {"traducao": "casa", "caixa": 1, "proxima_revisao": datetime.now()},
            "книга": {"traducao": "livro", "caixa": 1, "proxima_revisao": datetime.now()},
            "солнце": {"traducao": "sol", "caixa": 1, "proxima_revisao": datetime.now()},
            "машина": {"traducao": "carro", "caixa": 1, "proxima_revisao": datetime.now()},
            "дерево": {"traducao": "árvore", "caixa": 1, "proxima_revisao": datetime.now()},
            "вода": {"traducao": "água", "caixa": 1, "proxima_revisao": datetime.now()},
            "луна": {"traducao": "lua", "caixa": 1, "proxima_revisao": datetime.now()},
            "кошка": {"traducao": "gato", "caixa": 1, "proxima_revisao": datetime.now()},
            "цветок": {"traducao": "flor", "caixa": 1, "proxima_revisao": datetime.now()},
            "птица": {"traducao": "pássaro", "caixa": 1, "proxima_revisao": datetime.now()},
            "рыба": {"traducao": "peixe", "caixa": 1, "proxima_revisao": datetime.now()},
            "рука": {"traducao": "mão", "caixa": 1, "proxima_revisao": datetime.now()},
            "нога": {"traducao": "pé", "caixa": 1, "proxima_revisao": datetime.now()}
        },
        "intermediario": {
            "компьютер": {"traducao": "computador", "caixa": 1, "proxima_revisao": datetime.now()},
            "стул": {"traducao": "cadeira", "caixa": 1, "proxima_revisao": datetime.now()},
            "стол": {"traducao": "mesa", "caixa": 1, "proxima_revisao": datetime.now()},
            "телефон": {"traducao": "telefone", "caixa": 1, "proxima_revisao": datetime.now()},
            "окно": {"traducao": "janela", "caixa": 1, "proxima_revisao": datetime.now()},
            "дверь": {"traducao": "porta", "caixa": 1, "proxima_revisao": datetime.now()},
            "школа": {"traducao": "escola", "caixa": 1, "proxima_revisao": datetime.now()},
            "учитель": {"traducao": "professor", "caixa": 1, "proxima_revisao": datetime.now()},
            "ученик": {"traducao": "estudante", "caixa": 1, "proxima_revisao": datetime.now()},
            "страна": {"traducao": "país", "caixa": 1, "proxima_revisao": datetime.now()},
            "город": {"traducao": "cidade", "caixa": 1, "proxima_revisao": datetime.now()},
            "больница": {"traducao": "hospital", "caixa": 1, "proxima_revisao": datetime.now()},
            "ресторан": {"traducao": "restaurante", "caixa": 1, "proxima_revisao": datetime.now()},
            "супермаркет": {"traducao": "supermercado", "caixa": 1, "proxima_revisao": datetime.now()},
            "библиотека": {"traducao": "biblioteca", "caixa": 1, "proxima_revisao": datetime.now()}
        },
        "avancado": {
            "знание": {"traducao": "conhecimento", "caixa": 1, "proxima_revisao": datetime.now()},
            "окружающая среда": {"traducao": "meio ambiente", "caixa": 1, "proxima_revisao": datetime.now()},
            "правительство": {"traducao": "governo", "caixa": 1, "proxima_revisao": datetime.now()},
            "технология": {"traducao": "tecnologia", "caixa": 1, "proxima_revisao": datetime.now()},
            "население": {"traducao": "população", "caixa": 1, "proxima_revisao": datetime.now()},
            "образование": {"traducao": "educação", "caixa": 1, "proxima_revisao": datetime.now()},
            "международный": {"traducao": "internacional", "caixa": 1, "proxima_revisao": datetime.now()},
            "общение": {"traducao": "comunicação", "caixa": 1, "proxima_revisao": datetime.now()},
            "развитие": {"traducao": "desenvolvimento", "caixa": 1, "proxima_revisao": datetime.now()},
            "ответственность": {"traducao": "responsabilidade", "caixa": 1, "proxima_revisao": datetime.now()},
            "глобализация": {"traducao": "globalização", "caixa": 1, "proxima_revisao": datetime.now()},
            "устойчивое развитие": {"traducao": "sustentabilidade", "caixa": 1, "proxima_revisao": datetime.now()},
            "инновация": {"traducao": "inovação", "caixa": 1, "proxima_revisao": datetime.now()},
            "демократия": {"traducao": "democracia", "caixa": 1, "proxima_revisao": datetime.now()},
            "революция": {"traducao": "revolução", "caixa": 1, "proxima_revisao": datetime.now()}
        }
    }
}

# Variáveis globais
pontuacao = 0
alternativas = []
cor_botao_atual = VERDE
fundo_jogo = BRANCO  
fogos = []
nivel_atual = ""
idioma_atual = "inglês"  # Adicionado para controlar o idioma atual
palavras_usadas = []
english_word = ""
atual_correto = ""
palavras_erradas = []
palavras_por_nivel = {}

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

class ZTypeGame:
    def __init__(self, palavras_erradas):
        self.palavras_erradas = palavras_erradas
        self.words_to_practice = [word["palavra"] for word in palavras_erradas]
        self.total_words = len(self.words_to_practice)
        
        # Configurações do jogo
        self.player_speed = 5
        self.bullet_speed = 7
        self.enemy_speed_min = 0.5  # Velocidade reduzida
        self.enemy_speed_max = 1.5   # Velocidade reduzida
        self.star_speed_min = 0.1    # Velocidade reduzida
        self.star_speed_max = 0.3    # Velocidade reduzida
        
        # Estado do jogo
        self.player = {
            "x": WIDTH // 2,
            "y": HEIGHT - 50,
            "bullets": [],
            "health": 3,
            "score": 0
        }
        
        self.enemies = []
        self.stars = []
        self.game_over = False
        self.victory = False
        
        # Inicializa estrelas de fundo
        for _ in range(50):
            self.stars.append([
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.uniform(self.star_speed_min, self.star_speed_max)
            ])
    
    def run(self):
        clock = pygame.time.Clock()
        enemy_spawn_timer = 0
        
        while not self.game_over and not self.victory:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return self.player["score"]
                    
                    if event.key == pygame.K_SPACE:
                        self.player["bullets"].append([self.player["x"], self.player["y"] - 20])
                    
                    if event.unicode.isalpha():
                        for enemy in self.enemies:
                            if enemy["current_letter"] < len(enemy["letters"]):
                                if event.unicode.lower() == enemy["letters"][enemy["current_letter"]].lower():
                                    enemy["typed"] += enemy["letters"][enemy["current_letter"]]
                                    enemy["current_letter"] += 1
                                    
                                    if enemy["current_letter"] >= len(enemy["letters"]):
                                        self.player["score"] += 10 * len(enemy["word"])
                                        self.enemies.remove(enemy)
                                        break
            
            # Atualização do estado
            self.update_player()
            self.update_bullets()
            self.update_enemies(enemy_spawn_timer)
            self.update_stars()
            
            # Verifica condições de término
            if len(self.words_to_practice) == 0 and len(self.enemies) == 0:
                self.victory = True
            elif self.player["health"] <= 0:
                self.game_over = True
            
            # Desenho
            self.draw()
            
            pygame.display.flip()
            clock.tick(60)
            enemy_spawn_timer += 1
        
        # Mostra tela final
        self.show_end_screen()
        return self.player["score"]
    
    def update_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player["x"] > 30:
            self.player["x"] -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player["x"] < WIDTH - 30:
            self.player["x"] += self.player_speed
    
    def update_bullets(self):
        for bullet in self.player["bullets"][:]:
            bullet[1] -= self.bullet_speed
            if bullet[1] < 0:
                self.player["bullets"].remove(bullet)
    
    def update_enemies(self, timer):
        # Spawn de inimigos mais lento
        if timer >= 90 and self.words_to_practice:  # A cada ~1.5 segundos
            word = random.choice(self.words_to_practice)
            self.words_to_practice.remove(word)
            
            self.enemies.append({
                "word": word,
                "x": random.randint(50, WIDTH - 50),
                "y": random.randint(-100, -40),
                "speed": random.uniform(self.enemy_speed_min, self.enemy_speed_max),
                "typed": "",
                "letters": list(word),
                "current_letter": 0
            })
            
            if not self.words_to_practice:
                self.words_to_practice = [w["palavra"] for w in self.palavras_erradas 
                                        if w["palavra"] not in [e["word"] for e in self.enemies]]
        
        # Atualiza posição dos inimigos e verifica colisões
        player_rect = pygame.Rect(self.player["x"] - 15, self.player["y"] - 20, 30, 30)
        
        for enemy in self.enemies[:]:
            enemy["y"] += enemy["speed"]
            
            # Verifica se saiu da tela
            if enemy["y"] > HEIGHT + 20:
                self.player["health"] -= 1
                self.enemies.remove(enemy)
                continue
                
            # Verifica colisão com jogador
            enemy_rect = pygame.Rect(enemy["x"] - 15, enemy["y"] - 10, 30, 30)
            if player_rect.colliderect(enemy_rect):
                self.player["health"] -= 1
                self.enemies.remove(enemy)
                continue
                
            # Verifica colisão com balas
            for bullet in self.player["bullets"][:]:
                if (enemy["x"] - 15 < bullet[0] < enemy["x"] + 15 and 
                    enemy["y"] - 10 < bullet[1] < enemy["y"] + 20):
                    self.player["bullets"].remove(bullet)
                    enemy["letters"] = enemy["letters"][1:]
                    if not enemy["letters"]:
                        self.player["score"] += 10 * len(enemy["word"])
                        self.enemies.remove(enemy)
                    break
    
    def update_stars(self):
        for i, star in enumerate(self.stars):
            self.stars[i][1] += star[2]
            if star[1] > HEIGHT:
                self.stars[i] = [random.randint(0, WIDTH), 0, 
                                random.uniform(self.star_speed_min, self.star_speed_max)]
    
    def draw(self):
        tela.fill(PRETO)
        
        # Desenha estrelas de fundo
        for star in self.stars:
            pygame.draw.circle(tela, BRANCO, (int(star[0]), int(star[1])), 1)
        
        # Desenha jogador
        pygame.draw.polygon(tela, BRANCO, [
            (self.player["x"], self.player["y"] - 20),
            (self.player["x"] - 15, self.player["y"] + 10),
            (self.player["x"] + 15, self.player["y"] + 10)
        ])
        
        # Desenha balas
        for bullet in self.player["bullets"]:
            pygame.draw.rect(tela, VERDE, (bullet[0], bullet[1], 3, 10))
        
        # Desenha inimigos
        for enemy in self.enemies:
            pygame.draw.polygon(tela, VERMELHO, [
                (enemy["x"], enemy["y"] + 20),
                (enemy["x"] - 15, enemy["y"] - 10),
                (enemy["x"] + 15, enemy["y"] - 10)
            ])
            
            word_text = FONTE.render(enemy["word"], True, BRANCO)
            tela.blit(word_text, (enemy["x"] - word_text.get_width() // 2, enemy["y"] - 30))
            
            if enemy["typed"]:
                typed_text = FONTE.render(enemy["typed"], True, VERDE)
                tela.blit(typed_text, (enemy["x"] - typed_text.get_width() // 2, enemy["y"] - 50))
        
        # UI
        health_text = FONTE.render(f"Vidas: {self.player['health']}", True, BRANCO)
        tela.blit(health_text, (20, 20))
        
        score_text = FONTE.render(f"Pontos: {self.player['score']}", True, BRANCO)
        tela.blit(score_text, (20, 60))
        
        words_text = FONTE.render(f"Palavras: {self.total_words - len(self.words_to_practice)}/{self.total_words}", 
                                 True, BRANCO)
        tela.blit(words_text, (20, 100))
    
    def show_end_screen(self):
        clock = pygame.time.Clock()
        waiting = True
        
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                        waiting = False
            
            tela.fill(PRETO)
            
            if self.game_over:
                text = FONTE_PRINCIPAL.render("GAME OVER", True, VERMELHO)
            else:
                text = FONTE_PRINCIPAL.render("VITÓRIA!", True, VERDE)
            
            tela.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 50))
            
            score_text = FONTE.render(f"Pontuação final: {self.player['score']}", True, BRANCO)
            tela.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 + 20))
            
            continue_text = FONTE.render("Pressione ENTER para voltar", True, BRANCO)
            tela.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2 + 80))
            
            pygame.display.flip()
            clock.tick(60)

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
    texto_progresso = FONTE.render(f"Questão: {pontuacao}/10", True, BRANCO)
    tela.blit(texto_progresso, (barra_x + (barra_width - texto_progresso.get_width()) // 2, barra_y - 30))

    # Caixa Leitner (centralizada abaixo da barra de progresso)
    caixas = {1:0, 2:0, 3:0, 4:0, 5:0}
    for nivel in palavras[idioma_atual]:
        for palavra in palavras[idioma_atual][nivel]:
            caixas[palavras[idioma_atual][nivel][palavra]["caixa"]] += 1
    
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
        palavras[idioma_atual][nivel][palavra]["caixa"] = min(palavras[idioma_atual][nivel][palavra]["caixa"] + 1, 5)
    else:
        # Retorna para a caixa 1 (revisão mais frequente)
        palavras[idioma_atual][nivel][palavra]["caixa"] = 1
    
    # Define quando a palavra deve aparecer novamente
    intervalos = {1: 1, 2: 3, 3: 7, 4: 14, 5: 30}  # dias até próxima revisão
    palavras[idioma_atual][nivel][palavra]["proxima_revisao"] = datetime.now() + timedelta(days=intervalos[palavras[idioma_atual][nivel][palavra]["caixa"]])

# Seleciona a próxima palavra baseado no sistema Leitner
def obter_proxima_palavra(nivel):
    global palavras_por_nivel
    
    # Inicializa o dicionário se for a primeira vez
    if nivel not in palavras_por_nivel:
        palavras_por_nivel[nivel] = {
            "todas": list(palavras[idioma_atual][nivel].keys()),
            "usadas": []
        }
    
    agora = datetime.now()
    
    # 1. Prioridade para palavras da caixa 1
    caixa1 = [p for p in palavras[idioma_atual][nivel] 
             if palavras[idioma_atual][nivel][p]["caixa"] == 1 and
             p not in palavras_por_nivel[nivel]["usadas"]]
    
    # 2. Palavras atrasadas para revisão
    atrasadas = [p for p in palavras[idioma_atual][nivel] 
                if palavras[idioma_atual][nivel][p]["proxima_revisao"] <= agora and
                p not in palavras_por_nivel[nivel]["usadas"] and
                p not in caixa1]
    
    # 3. Palavras de outras caixas
    outras = [p for p in palavras[idioma_atual][nivel] 
             if p not in palavras_por_nivel[nivel]["usadas"] and
             p not in caixa1 and
             p not in atrasadas]
    
    # 4. Se todas as palavras já foram usadas, reinicie
    if not caixa1 and not atrasadas and not outras:
        palavras_por_nivel[nivel]["usadas"] = []
        return obter_proxima_palavra(nivel)
    
    # Seleção priorizando caixa 1, depois atrasadas, depois outras
    if caixa1:
        palavra = random.choice(caixa1)
    elif atrasadas:
        palavra = random.choice(atrasadas)
    else:
        palavra = random.choice(outras)
    
    palavras_por_nivel[nivel]["usadas"].append(palavra)
    return palavra

# Função para verificar a resposta
def verificar_resposta(resposta_selecionada, palavra_estrangeira, resposta_correta, nivel):
    global pontuacao, alternativas, palavras_erradas
    
    if resposta_selecionada == resposta_correta:
        atualizar_caixa(palavra_estrangeira, nivel, True)
        pontuacao += 1
        tela_resposta_correta()
    else:
        atualizar_caixa(palavra_estrangeira, nivel, False)
        # Verifica se a palavra já está na lista de erros
        palavra_ja_errada = False
        for erro in palavras_erradas:
            if erro["palavra"] == palavra_estrangeira:
                palavra_ja_errada = True
                break
        
        # Adiciona apenas se for a primeira vez que errou esta palavra
        if not palavra_ja_errada:
            erro = {
                "palavra": palavra_estrangeira,
                "traducao": resposta_correta,
                "resposta_errada": resposta_selecionada
            }
            palavras_erradas.append(erro)
        
        tela_resposta_errada(resposta_correta)
    
    alternativas = []  # Limpa as alternativas para que uma nova palavra seja selecionada

# Função para criar a tela de seleção de idioma
def tela_selecao_idioma():
    esperando = True
    clock = pygame.time.Clock()
    
    while esperando:
        tela.fill(BRANCO)
        
        if imagem_inicio:
            tela.blit(imagem_inicio, (0, 0))
        
        # Título
        exibir_texto_com_fundo("Selecione o Idioma", FONTE_PRINCIPAL, PRETO, BRANCO, WIDTH // 2, HEIGHT // 4)
        
        # Botões de idioma
        botao_ingles = exibir_botao("Inglês", WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50, VERDE, (100, 200, 100))
        botao_russo = exibir_botao("Russo", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, AZUL, (100, 100, 200))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if botao_ingles.collidepoint(pos_mouse):
                    return "inglês"
                elif botao_russo.collidepoint(pos_mouse):
                    return "russo"
        
        clock.tick(30)

# Função para criar a tela inicial
def tela_inicial():
    global idioma_atual
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
        
        # Caixa de explicação
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
        
        # Botões de nível 
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

# Tela de parabéns
def tela_parabens(nivel):
    global fogos, trofeu_img, palavras_erradas
    
    fogos = []
    clock = pygame.time.Clock()
    
    # Criar fogos de artifício
    for _ in range(15):
        criar_fogos(random.randint(100, WIDTH-100), random.randint(100, HEIGHT//2))
    
    # Configurar fontes
    fonte_titulo = pygame.font.Font(None, 48)
    fonte_subtitulo = pygame.font.Font(None, 36)
    fonte_botao = pygame.font.Font(None, 32)
    fonte_palavras = pygame.font.Font(None, 24)
    
    # Posições dos elementos
    centro_x = WIDTH // 2
    titulo_y = 150
    subtitulo_y = 220
    trofeu_y = 300
    palavras_y = 450
    botao_ztype_y = HEIGHT - 180  # Posição mais acima
    botao_continuar_y = HEIGHT - 100  # Posição mais abaixo
    
    waiting = True
    while waiting:
        tela.fill(BRANCO)
        
        # Efeitos de fogos
        fogos = [fogo for fogo in fogos if fogo.update()]
        for fogo in fogos:
            fogo.draw(tela)
        
        if random.random() < 0.15:
            criar_fogos(random.randint(100, WIDTH-100), random.randint(100, HEIGHT//2))
        
        # Título e subtítulo
        titulo = fonte_titulo.render("Nível Concluído!", True, AZUL_ESCURO)
        tela.blit(titulo, (centro_x - titulo.get_width() // 2, titulo_y))
        
        subtitulo = fonte_subtitulo.render(f"Dificuldade: {nivel.capitalize()}", True, VERDE)
        tela.blit(subtitulo, (centro_x - subtitulo.get_width() // 2, subtitulo_y))
        
        # Troféu centralizado
        if trofeu_img:
            tela.blit(trofeu_img, (centro_x - trofeu_img.get_width() // 2, trofeu_y))
        
        # Lista de palavras erradas (se houver)
        if palavras_erradas:
            titulo_palavras = fonte_palavras.render("Palavras para praticar:", True, VERMELHO)
            tela.blit(titulo_palavras, (centro_x - titulo_palavras.get_width() // 2, palavras_y))
            
            for i, erro in enumerate(palavras_erradas[:5]):  # Mostra até 5 palavras
                texto = fonte_palavras.render(
                    f"{erro['palavra']} = {erro['traducao']} (você respondeu: {erro['resposta_errada']})", 
                    True, PRETO
                )
                tela.blit(texto, (centro_x - texto.get_width() // 2, palavras_y + 30 + i * 30))
        
        # Botões separados
        if palavras_erradas:
            botao_ztype = exibir_botao("Praticar no ZType", centro_x - 200, botao_ztype_y, 400, 50, 
                                      AZUL, (100, 100, 255))
        
        botao_continuar = exibir_botao("Continuar", centro_x - 100, botao_continuar_y, 200, 50, 
                                      VERDE, (100, 255, 100))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 
                if event.key == pygame.K_SPACE and palavras_erradas:
                    ztype = ZTypeGame(palavras_erradas)
                    ztype.run()
                    palavras_erradas = []  # Limpa após praticar
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if palavras_erradas and 'botao_ztype' in locals() and botao_ztype.collidepoint(event.pos):
                    ztype = ZTypeGame(palavras_erradas)
                    ztype.run()
                    palavras_erradas = []  # Limpa após praticar
                    return
                if 'botao_continuar' in locals() and botao_continuar.collidepoint(event.pos):
                    return
        
        clock.tick(30)

# Função para reiniciar o jogo
def recomeçar_jogo():
    global pontuacao, alternativas, fogos, palavras_erradas, palavras_por_nivel
    pontuacao = 0
    alternativas = []
    fogos = []
    palavras_erradas = []
    palavras_por_nivel = {}  # Limpa o registro de palavras usadas por nível
    main()

# Função principal do jogo
def main():    
    global pontuacao, alternativas, cor_botao_atual, fogos, nivel_atual, palavras_usadas, english_word, atual_correto, idioma_atual
    
    # Primeiro seleciona o idioma
    idioma_atual = tela_selecao_idioma()
    
    # Depois seleciona o nível
    nivel_atual = tela_inicial()
    
    clock = pygame.time.Clock()
    running = True
    palavras_usadas = []
    
    while running:
        if pontuacao >= 10:
            tela_parabens(nivel_atual)
            recomeçar_jogo()
            return
        
        # Preencher fundo
        if fundo_perguntas:
            tela.blit(fundo_perguntas, (0, 0))
        else:
            # Gradiente azul claro como fallback
            tela.fill((230, 243, 255))  # Cor hexadecimal #E6F3FF
            pygame.draw.rect(tela, (255, 255, 255), (50, 50, WIDTH-100, HEIGHT-100), border_radius=20)

        # Obter próxima palavra do nível atual
        if not alternativas:
            english_word = obter_proxima_palavra(nivel_atual)
            atual_correto = palavras[idioma_atual][nivel_atual][english_word]["traducao"]
            
            # Prepara as alternativas
            alternativas = [atual_correto]
            while len(alternativas) < 4:
                palavra_aleatoria = random.choice([p["traducao"] for p in palavras[idioma_atual][nivel_atual].values()])
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
