import wx
import math

class TicTacToeFrame(wx.Frame):
    def __init__(self, parent, title):
        super(TicTacToeFrame, self).__init__(parent, title=title, size=(400, 500))
        self.current_player = "X"  # Current player (two players)
        self.board = [" "] * 9
        self.buttons = []

        # Create the main panel
        panel = wx.Panel(self)

        # Sizer for the board buttons (3x3 grid)
        grid_sizer = wx.GridSizer(rows=3, cols=3, gap=wx.Size(5, 5))
        for i in range(9):
            btn = wx.Button(panel, label=" ", size=(100, 100))
            btn.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
            btn.Bind(wx.EVT_BUTTON, lambda event, idx=i: self.player_move(idx))
            grid_sizer.Add(btn, 0, wx.EXPAND)
            self.buttons.append(btn)

        # Reset button
        self.reset_btn = wx.Button(panel, label="Reset")
        self.reset_btn.Bind(wx.EVT_BUTTON, lambda event: self.reset_game())

        # Gauge to display the minimax evaluation bar
        # We use a range of 0 to 200 to represent values from -1 to 1 (100 represents a tie)
        self.gauge = wx.Gauge(panel, range=200, size=(300, 25))
        # Label to display the evaluation value and the predicted winner
        self.eval_label = wx.StaticText(panel, label="Evaluation: 0 (Tie)")

        # Organize the components vertically
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, 10)
        vbox.Add(self.reset_btn, 0, wx.ALL | wx.CENTER, 10)
        vbox.Add(self.gauge, 0, wx.ALL | wx.CENTER, 10)
        vbox.Add(self.eval_label, 0, wx.ALL | wx.CENTER, 10)
        panel.SetSizer(vbox)

        # Initialize the minimax evaluation
        self.update_minimax_evaluation()

    def reset_game(self):
        self.board = [" "] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.SetLabel(" ")
            btn.Enable()
        self.update_minimax_evaluation()

    def get_winner(self, board):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for cond in win_conditions:
            if board[cond[0]] == board[cond[1]] == board[cond[2]] != " ":
                return board[cond[0]]
        return "Tie" if " " not in board else None

    def minimax(self, board, is_maximizing):
        winner = self.get_winner(board)
        if winner == "X":
            return -1  # X win returns -1
        elif winner == "O":
            return 1   # O win returns 1
        elif winner == "Tie":
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == " ":
                    new_board = board.copy()
                    new_board[i] = "O"
                    score = self.minimax(new_board, False)
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == " ":
                    new_board = board.copy()
                    new_board[i] = "X"
                    score = self.minimax(new_board, True)
                    best_score = min(score, best_score)
            return best_score

    def player_move(self, idx):
        if self.board[idx] == " ":
            # Update the board with the current player's move
            self.board[idx] = self.current_player
            self.buttons[idx].SetLabel(self.current_player)
            self.buttons[idx].Disable()
            if self.check_game_over():
                return
            # Alternate the player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.update_minimax_evaluation()

    def check_game_over(self):
        winner = self.get_winner(self.board)
        if winner:
            msg = "Tie!" if winner == "Tie" else f"Player {winner} wins!"
            wx.MessageBox(msg, "Game Over", wx.OK | wx.ICON_INFORMATION)
            self.reset_game()
            return True
        return False

    def update_minimax_evaluation(self):
        """
        Update the minimax evaluation bar and label.
        Since our minimax function returns -1 for X win and 1 for O win,
        we multiply by -1 so that:
          1  => predicted win for X,
          0  => predicted tie,
         -1  => predicted win for O.
        """
        is_maximizing = True if self.current_player == "O" else False
        minimax_value = self.minimax(self.board, is_maximizing)
        eval_value = -minimax_value  # Invert the sign: 1 for X, -1 for O

        # Update the gauge (0 to 200 scale; 100 means tie)
        gauge_value = int((eval_value + 1) * 100)
        self.gauge.SetValue(gauge_value)

        # Determine the label text based on the evaluation
        if eval_value == 1:
            result_text = "Predicted win for: X"
        elif eval_value == -1:
            result_text = "Predicted win for: O"
        else:
            result_text = "Predicted tie"

        self.eval_label.SetLabel(f"Evaluation: {eval_value} ({result_text})")
        self.Layout()

if __name__ == "__main__":
    app = wx.App(False)
    frame = TicTacToeFrame(None, "Tic Tac Toe - Two Players with Minimax Evaluation")
    frame.Show()
    app.MainLoop()
