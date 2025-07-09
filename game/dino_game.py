import pygame, sys, random

def run_game():
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    clock = pygame.time.Clock()
    pygame.display.set_caption("AI Dino Trainer")

    # Load sounds
    jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
    gameover_sound = pygame.mixer.Sound("assets/sounds/gameover.wav")

    # Load and scale dino
    dino_img = pygame.image.load("assets/dino.png")
    dino_img = pygame.transform.scale(dino_img, (60, 60))
    dino_rect = dino_img.get_rect(midbottom=(100, 300))

    # Load and scale cactus options
    cactus_imgs = [
        pygame.transform.scale(pygame.image.load("assets/cactus1.png"), (40, 60)),
        pygame.transform.scale(pygame.image.load("assets/cactus2.png"), (50, 50)),
        pygame.transform.scale(pygame.image.load("assets/cactus3.png"), (30, 70)),
    ]
    current_cactus = random.choice(cactus_imgs)
    cactus_rect = current_cactus.get_rect(midbottom=(800, 300))

    # Font and Score
    font = pygame.font.Font(None, 40)
    score = 0

    # Game State
    game_active = True

    # Gravity and jump
    gravity = 0
    is_jumping = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_active = True
                cactus_rect.left = 800
                dino_rect.bottom = 300
                gravity = 0
                score = 0

        screen.fill((255, 255, 255))
        pygame.draw.line(screen, (0, 0, 0), (0, 300), (800, 300), 2)  # Ground line

        if game_active:
            # Handle jump
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and not is_jumping:
                gravity = -15
                is_jumping = True
                jump_sound.play()

            # Gravity effect
            gravity += 1
            dino_rect.y += gravity

            if dino_rect.bottom >= 300:
                dino_rect.bottom = 300
                is_jumping = False

            # Move cactus
            cactus_rect.x -= 5
            if cactus_rect.right < 0:
                current_cactus = random.choice(cactus_imgs)
                cactus_rect = current_cactus.get_rect(midbottom=(800, 300))

            # Collision
            if dino_rect.colliderect(cactus_rect) and dino_rect.bottom >= 290:
                game_active = False
                gameover_sound.play()


            # Draw
            screen.blit(dino_img, dino_rect)
            screen.blit(current_cactus, cactus_rect)

            score += 0.1

        else:
            # Game Over message
            game_over_text = font.render("Game Over! Press R to Restart", True, (200, 0, 0))
            screen.blit(game_over_text, (200, 180))

        # Score display
        score_surface = font.render(f"Score: {int(score)}", True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))

        pygame.display.update()
        clock.tick(60)
