import tkinter as tk
import database as d

BG_COLOR = "#3d6466"
ACTIVE_COLOR = "#badee2"

# Create app window
root = tk.Tk()
root.title("Washington Capitals Stats")

# Create frames
main_frame = tk.Frame(root, bg=BG_COLOR)
skater_frame = tk.Frame(root, bg=BG_COLOR)
goalie_frame = tk.Frame(root, bg=BG_COLOR)
roster_frame = tk.Frame(root, bg=BG_COLOR)
game_frame = tk.Frame(root, bg=BG_COLOR)
schedule_frame = tk.Frame(root, bg=BG_COLOR)
frames = [main_frame, skater_frame, goalie_frame,
          roster_frame, game_frame, schedule_frame]


def destroy_frames(ex: tk.Frame) -> None:
    ...


if __name__ == '__main__':
    root.mainloop()
