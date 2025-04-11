Tic Tac Toe with Minimax Evaluation
This project is a two-player Tic Tac Toe game built using wxPython.
The game features:

Graphical User Interface (GUI): The board is displayed as a 3x3 grid of buttons.

Two-Player Mode: Two players (X and O) can play the game by taking turns.

Minimax Evaluation: A minimax algorithm evaluates the current board state and displays:

Evaluation Bar: A graphical gauge that represents the current advantage on a scale from -1 to 1 (mapped to a gauge range of 0 to 200, with 100 representing a tie).

Textual Evaluation: A label showing the numerical evaluation along with a prediction of which player is winning:

1 means a predicted win for X,

-1 means a predicted win for O,

0 indicates a predicted tie.

Reset Functionality: Easily reset the game using the "Reset" button.

How to Run
Install wxPython:
Ensure that wxPython is installed on your system. You can install it via pip:

bash
Copiar
Editar
pip install -U wxPython
Run the Game:
Execute the Python script:

bash
Copiar
Editar
python tic_tac_toe.py
Enjoy the game and explore how the minimax evaluation changes as you play!
