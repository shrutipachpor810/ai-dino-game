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
│
├── game/                    # All game-related Python modules
│   ├── __init__.py          # (Optional) Makes this a package
│   ├── dino_game.py         # Simple playable Dino game
│   ├── ai_dino.py           # NEAT AI trainer game logic
│   ├── assets/              # Images, sprites, sound effects
│   │   ├── dino.png
│   │   ├── dino_jump.png
│   │   ├── bird.png
│   │   ├── cactus1.png
│   │   ├── cactus2.png
│   │   ├── cactus3.png
│  
│
├── training_logs/           # Auto-saved logs for AI training
│   ├── logs.json
│   ├── logs_backup.json     # (Optional) backup
│
├── neat_config.txt          # NEAT-Python configuration file
│
├── main.py                  # GUI menu to pick Classic or AI mode
│
│
├── .gitignore               # Files/folders to ignore in Git
│
└── README.md                # Full project overview & instructions

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