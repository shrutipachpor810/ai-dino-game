import pygame, neat, os, random, sys, json
from neat.reporting import BaseReporter

pygame.init()

# Setup logs
log_data = []  # Will hold logs for each generation

# Get the correct path for training_logs
script_dir = os.path.dirname(os.path.abspath(__file__))
training_logs_dir = os.path.join(script_dir, "..", "training_logs")
os.makedirs(training_logs_dir, exist_ok=True)

print(f"📁 Training logs will be saved to: {os.path.abspath(training_logs_dir)}")

# Screen setup
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Dino Trainer")
clock = pygame.time.Clock()

# Load assets with fallback to colored rectangles if images not found
def load_image_or_fallback(path, size, color):
    """Load image or create colored rectangle if image not found"""
    try:
        return pygame.transform.scale(pygame.image.load(path), size)
    except (pygame.error, FileNotFoundError):
        print(f"⚠️  Image {path} not found, using colored rectangle instead")
        surf = pygame.Surface(size)
        surf.fill(color)
        return surf

# Load assets
assets_dir = os.path.join(script_dir, "..", "assets")
dino_img = load_image_or_fallback(os.path.join(assets_dir, "dino.png"), (60, 60), (34, 139, 34))
cactus_imgs = [
    load_image_or_fallback(os.path.join(assets_dir, "cactus1.png"), (40, 60), (0, 128, 0)),
    load_image_or_fallback(os.path.join(assets_dir, "cactus2.png"), (50, 70), (0, 100, 0)),
    load_image_or_fallback(os.path.join(assets_dir, "cactus3.png"), (30, 50), (0, 150, 0))
]

# Constants
GROUND_Y = 300
FONT = pygame.font.SysFont('Arial', 20)
gen = 0  # Track generation

# Dino class
class Dino:
    def __init__(self):
        self.img = dino_img
        self.rect = self.img.get_rect(midbottom=(100, GROUND_Y))
        self.gravity = 0
        self.score = 0
        self.is_alive = True

    def jump(self):
        if self.rect.bottom >= GROUND_Y:
            self.gravity = -15

    def move(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y

    def draw(self, screen):
        screen.blit(self.img, self.rect)

# Cactus class
class Cactus:
    def __init__(self):
        self.img = random.choice(cactus_imgs)
        self.rect = self.img.get_rect(midbottom=(WIDTH, GROUND_Y))

    def move(self):
        self.rect.x -= 5

    def draw(self, screen):
        screen.blit(self.img, self.rect)

# Drawing function
def draw_screen(dinos, cactus, score, gen):
    screen.fill((135, 206, 235))  # Sky blue background
    pygame.draw.line(screen, (101, 67, 33), (0, GROUND_Y), (WIDTH, GROUND_Y), 3)  # Brown ground
    cactus.draw(screen)
    for dino in dinos:
        dino.draw(screen)

    gen_text = FONT.render(f"Gen: {gen}", True, (50, 50, 50))
    score_text = FONT.render(f"Score: {score}", True, (50, 50, 50))
    alive_text = FONT.render(f"Alive: {len(dinos)}", True, (50, 50, 50))
    
    screen.blit(gen_text, (10, 10))
    screen.blit(score_text, (10, 35))
    screen.blit(alive_text, (10, 60))
    pygame.display.update()

# Evaluation function for NEAT
def eval_genomes(genomes, config):
    global gen
    gen += 1
    print(f"🚀 Starting Generation {gen}")

    nets = []
    ge = []
    dinos = []

    cactus = Cactus()
    score = 0

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        dinos.append(Dino())
        genome.fitness = 0
        ge.append(genome)

    run = True
    while run and len(dinos) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Save logs before quitting
                save_logs_safely()
                pygame.quit()
                sys.exit()

        cactus.move()

        i = 0
        while i < len(dinos):
            dino = dinos[i]
            dino.move()
            ge[i].fitness += 0.1  # survive reward

            # Inputs: dino_y, cactus_x, distance
            input_data = (dino.rect.y, cactus.rect.x, cactus.rect.x - dino.rect.x)
            output = nets[i].activate(input_data)

            if output[0] > 0.5:
                dino.jump()

            # Collision
            if dino.rect.colliderect(cactus.rect):
                ge[i].fitness -= 1
                dinos.pop(i)
                nets.pop(i)
                ge.pop(i)
            else:
                i += 1

        # Reset cactus if passed
        if cactus.rect.right < 0:
            score += 1
            cactus = Cactus()
            for g in ge:
                g.fitness += 5  # passing reward

        draw_screen(dinos, cactus, score, gen)

# Logger class
class SimpleLogger(BaseReporter):
    def __init__(self):
        self.generation = 0

    def start_generation(self, generation):
        self.generation = generation

    def post_evaluate(self, config, population, species, best_genome):
        entry = {
            "generation": self.generation,
            "best_fitness": round(best_genome.fitness, 2),
            "species_count": len(species.species),
            "population_size": len(population)
        }
        log_data.append(entry)
        print(f"📊 Gen {self.generation:3d} | Best Fitness: {entry['best_fitness']:6.1f} | Species: {entry['species_count']:2d}")
        
        # Save logs after each generation (backup)
        save_logs_safely()

    def end_generation(self, config, population, species):
        self.generation += 1

    def found_solution(self, config, generation, best):
        print(f"🎉 Solution found in generation {generation}!")

    def info(self, msg):
        print(f"ℹ️  {msg}")

    def reset(self):
        self.generation = 0

def save_logs_safely():
    """Save logs with error handling"""
    if not log_data:
        print("⚠️  No log data to save yet")
        return
    
    try:
        log_path = os.path.join(training_logs_dir, "logs.json")
        
        # Create a backup if file exists
        if os.path.exists(log_path):
            backup_path = os.path.join(training_logs_dir, "logs_backup.json")
            try:
                os.rename(log_path, backup_path)
            except:
                pass
        
        # Write the logs
        with open(log_path, "w") as f:
            json.dump({
                "total_generations": len(log_data),
                "training_status": "in_progress" if gen < 50 else "completed",
                "current_generation": gen,
                "logs": log_data
            }, f, indent=4)
        
        print(f"💾 Logs saved: {len(log_data)} generations to {log_path}")
        
    except Exception as e:
        print(f"❌ Error saving logs: {e}")
        print(f"📄 Log data preview: {log_data[-1] if log_data else 'No data'}")

# Run function
def run(config_path):
    global log_data
    
    print(f"🔧 Loading config from: {config_path}")
    
    try:
        config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path,
        )
        print("✅ Config loaded successfully")
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(SimpleLogger())
    population.add_reporter(neat.StatisticsReporter())

    print("🦕 Starting AI Dino Training...")
    
    try:
        winner = population.run(eval_genomes, 50)
        print("🏁 Training completed successfully!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Training interrupted by user")
    except Exception as e:
        print(f"❌ Training error: {e}")
    
    # Final save
    save_logs_safely()
    
    # Print summary
    if log_data:
        best_fitness = max([entry["best_fitness"] for entry in log_data])
        print(f"\n📈 Training Summary:")
        print(f"   Generations completed: {len(log_data)}")
        print(f"   Best fitness achieved: {best_fitness:.2f}")
        print(f"   Logs saved to: {os.path.join(training_logs_dir, 'logs.json')}")
    
    return winner if 'winner' in locals() else None

# Entry point
if __name__ == "__main__":
    local_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(local_dir, "..", "neat_config.txt")
    
    print(f"🎮 AI Dino Trainer Starting...")
    print(f"📁 Script directory: {local_dir}")
    print(f"🔧 Config path: {config_path}")
    
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        print("Please make sure neat_config.txt exists in the parent directory")
        sys.exit(1)
    
    try:
        run(config_path)
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        save_logs_safely()  # Try to save logs even if there's an error