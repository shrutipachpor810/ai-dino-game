import pygame
import sys
import math
import random

pygame.init()

# ✅ Match the game window size
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🦕 DINO LEGENDS - Choose Your Adventure")

# Colors
DARK_BG = (15, 23, 42)
ACCENT_BLUE = (59, 130, 246)
ACCENT_GREEN = (34, 197, 94)
ACCENT_PURPLE = (168, 85, 247)
ACCENT_ORANGE = (251, 146, 60)
WHITE = (255, 255, 255)
LIGHT_GRAY = (148, 163, 184)

# Fonts
title_font = pygame.font.Font(None, 48)
subtitle_font = pygame.font.Font(None, 24)
button_font = pygame.font.Font(None, 20)
small_font = pygame.font.Font(None, 16)

class Particle:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(1, 2)
        self.speed = random.uniform(0.5, 1.5)
        self.alpha = random.randint(30, 80)
        
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -10
            self.x = random.randint(0, WIDTH)
    
    def draw(self, surface):
        pygame.draw.circle(surface, (*LIGHT_GRAY, self.alpha), (int(self.x), int(self.y)), int(self.size))

class AnimatedButton:
    def __init__(self, x, y, width, height, text, color, icon=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_rect = self.rect.copy()
        self.text = text
        self.color = color
        self.icon = icon
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.glow_alpha = 0
        self.target_glow = 0
        self.bounce_offset = 0
        self.click_effect = 0
        
    def update(self, mouse_pos, dt):
        hovering = self.original_rect.collidepoint(mouse_pos)
        self.target_scale = 1.05 if hovering else 1.0
        self.target_glow = 120 if hovering else 0

        self.hover_scale += (self.target_scale - self.hover_scale) * dt * 8
        self.glow_alpha += (self.target_glow - self.glow_alpha) * dt * 10

        center = self.original_rect.center
        new_size = (int(self.original_rect.width * self.hover_scale), 
                    int(self.original_rect.height * self.hover_scale))
        self.rect = pygame.Rect(0, 0, *new_size)
        self.rect.center = center

        self.bounce_offset = math.sin(pygame.time.get_ticks() * 0.003) * 2

        if self.click_effect > 0:
            self.click_effect -= dt * 300

    def handle_click(self):
        self.click_effect = 100

    def draw(self, surface):
        if self.glow_alpha > 0:
            glow_surf = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (*self.color, int(self.glow_alpha * 0.3)), 
                             (0, 0, self.rect.width + 10, self.rect.height + 10), border_radius=15)
            surface.blit(glow_surf, (self.rect.x - 5, self.rect.y - 5 + self.bounce_offset))

        button_rect = pygame.Rect(self.rect.x, self.rect.y + self.bounce_offset, self.rect.width, self.rect.height)

        pygame.draw.rect(surface, self.color, button_rect, 2, border_radius=10)

        if self.click_effect > 0:
            click_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(click_surf, (255, 255, 255, int(self.click_effect)), 
                             (0, 0, self.rect.width, self.rect.height), border_radius=10)
            surface.blit(click_surf, button_rect.topleft)

        full_text = f"{self.icon} {self.text}" if self.icon else self.text
        text_surf = button_font.render(full_text, True, WHITE)
        text_rect = text_surf.get_rect(center=button_rect.center)
        surface.blit(text_surf, text_rect)

def draw_title(surface):
    title_surf = title_font.render("DINO LEGENDS", True, WHITE)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, 60))
    surface.blit(title_surf, title_rect)

    subtitle_surf = subtitle_font.render("Choose Your Adventure", True, LIGHT_GRAY)
    subtitle_rect = subtitle_surf.get_rect(center=(WIDTH // 2, 100))
    surface.blit(subtitle_surf, subtitle_rect)

def main_menu():
    clock = pygame.time.Clock()
    particles = [Particle() for _ in range(30)]

    simple_button = AnimatedButton(WIDTH // 2 - 150, 150, 300, 50, "PLAY CLASSIC MODE", ACCENT_GREEN, "🎮")
    ai_button = AnimatedButton(WIDTH // 2 - 150, 220, 300, 50, "AI NEURAL EVOLUTION", ACCENT_PURPLE, "🧠")
    quit_button = AnimatedButton(WIDTH // 2 - 75, 290, 150, 40, "EXIT GAME", ACCENT_ORANGE, "🚪")

    buttons = [simple_button, ai_button, quit_button]

    while True:
        dt = clock.tick(60) / 1000.0
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if simple_button.rect.collidepoint(event.pos):
                    simple_button.handle_click()
                    from game.dino_game import run_game
                    run_game()
                elif ai_button.rect.collidepoint(event.pos):
                    ai_button.handle_click()
                    from game.ai_dino import run as run_ai_dino
                    import os
                    config_path = os.path.join(os.path.dirname(__file__), "neat_config.txt")
                    run_ai_dino(config_path)
                elif quit_button.rect.collidepoint(event.pos):
                    quit_button.handle_click()
                    pygame.quit()
                    sys.exit()

        screen.fill(DARK_BG)

        for particle in particles:
            particle.update()
            particle.draw(screen)

        draw_title(screen)

        for button in buttons:
            button.update(mouse_pos, dt)
            button.draw(screen)

        version_surf = small_font.render("v2.0 | Lite", True, LIGHT_GRAY)
        screen.blit(version_surf, (WIDTH - 100, HEIGHT - 30))

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
