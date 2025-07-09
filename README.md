# 🦕 AI Dino Game

**Dino Legends: AI Dino Trainer** is a fun twist on the classic Chrome Dino game.  
Play it yourself or train an AI agent to master jumping over obstacles using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.

---

## 🚀 Features

- 🕹️ **Classic Dino Mode:** Play the simple endless runner yourself.
- 🤖 **AI Mode:** Watch your dinosaur evolve using neural networks and genetic algorithms.
- 🎨 **Modern Menu:** Choose between Classic or AI Mode from an animated Pygame GUI.
- 📁 **NeatConfig:** Easily configurable AI training parameters.
- 🧩 **Modular Design:** Clean OOP structure with separate game logic and training logic.
- 🧮 **Logging:** Training logs saved automatically for analysis.

---

## ⚙️ Tech Stack

| Tech             | Purpose                                |
|------------------|----------------------------------------|
| **Python **      | Main programming language              |
| **Pygame**       | Graphics, game loop, and GUI           |
| **NEAT-Python**  | Neuroevolution library for AI training |
| **JSON**         | Configuration and logging              |
| **OOP Design**   | Maintainable and modular codebase      |

---

## 📂 Project Structure

ai-dino-trainer/
├── game/                # All game-related Python modules
│   ├── __init__.py      # (Optional) Makes this a package
│   ├── dino_game.py     # Classic Dino game logic
│   ├── ai_dino.py       # NEAT AI Dino trainer logic
│   └── assets/          # Game assets (images, sprites)
│       ├── dino.png
│       ├── dino_jump.png
│       ├── bird.png
│       ├── cactus1.png
│       ├── cactus2.png
│       └── cactus3.png
│
├── training_logs/       # Auto-saved training logs
│   ├── logs.json
│   └── logs_backup.json # (Optional) Backup logs
│
├── neat_config.txt      # NEAT-Python configuration
├── main.py              # Launches GUI menu for game modes
├── .gitignore           # Ignore Python cache, logs, etc.
├── requirements.txt     # Project dependencies
└── README.md            # Project overview & instructions


---

## ⚙️ How to Run

1️⃣ Clone this repo:
```bash
git clone https://github.com/your-username/ai-dino-trainer.git
cd ai-dino-trainer

2️⃣ Install dependencies:

pip install -r requirements.txt

3️⃣ Start the game:

python main.py

4️⃣ Pick your mode:

Classic Mode: Play manually

AI Neural Evolution: Train & watch your AI Dino evolve!

📊 Logs
Training progress is saved automatically to training_logs/logs.json.

Backups are created as logs_backup.json to prevent loss.

You can review the logs to analyze NEAT performance.

🤝 Contribution
Pull requests are welcome! Improve gameplay, polish the GUI, or add new obstacles. Just fork this repo, make changes, and submit a PR.

📄 License
MIT — free to use, share, and modify.
