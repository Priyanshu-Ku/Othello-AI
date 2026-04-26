# Othello AI: Minimax with Alpha-Beta Pruning

## Objective
This project is an implementation of the classic board game Othello (Reversi), featuring an integrated AI opponent. It was developed to demonstrate advanced searching techniques and decision-making in adversarial, zero-sum environments.

## AI & Searching Techniques Used
The core of this project is the AI agent, which calculates optimal moves using the following algorithms:

* **Minimax Algorithm:** Builds a game tree to evaluate possible future states. The AI acts as the Maximizer (seeking the highest score), while assuming the human plays perfectly as the Minimizer.
* **Alpha-Beta Pruning:** An optimization technique that drastically reduces the number of nodes evaluated in the search tree. By "pruning" branches that are guaranteed to yield worse outcomes than previously explored paths, the AI can search deeper (e.g., depth 3 to 5) in real-time. The time complexity improves from $O(b^d)$ to a best-case of $O(b^{d/2})$.
* **Positional Heuristic Matrix:** Since the AI cannot compute the game to the very end due to the massive state space, it relies on a heuristic evaluation function. The board uses a weighted matrix where corners (highly advantageous) are scored positively, and squares adjacent to corners (highly dangerous) are penalized.

## Tech Stack
* **Language:** Python 3.x
* **UI/Rendering:** Pygame

## How to Run
1. Clone the repository: `git clone [your-repo-link]`
2. Install dependencies: `pip install pygame`
3. Run the application: `python main.py`

## Demonstration
The game is played on an 8x8 grid. The AI (Black) moves first. Valid moves must flank at least one opponent piece to flip it. The game concludes when neither player can make a valid move.