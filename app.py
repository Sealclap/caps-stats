import tkinter as tk
import database as d

BG_COLOR = "#3d6466"
ACTIVE_COLOR = "#badee2"
FRAME_WIDTH = 600
FRAME_HEIGHT = 400

# Create app window
root = tk.Tk()
root.title("Capitals Tracker")
root.eval("tk::PlaceWindow . center")
root.resizable(False, False)
root.iconbitmap("assets/caps_icon.ico")

# Create frames
main_frame = tk.Frame(root, width=FRAME_WIDTH,
                      height=FRAME_HEIGHT, bg=BG_COLOR)
skater_frame = tk.Frame(root, width=FRAME_WIDTH,
                        height=FRAME_HEIGHT, bg=BG_COLOR)
goalie_frame = tk.Frame(root, width=FRAME_WIDTH,
                        height=FRAME_HEIGHT, bg=BG_COLOR)
roster_frame = tk.Frame(root, width=FRAME_WIDTH,
                        height=FRAME_HEIGHT, bg=BG_COLOR)
game_frame = tk.Frame(root, width=FRAME_WIDTH,
                      height=FRAME_HEIGHT, bg=BG_COLOR)
schedule_frame = tk.Frame(root, width=FRAME_WIDTH,
                          height=FRAME_HEIGHT, bg=BG_COLOR)
frames = [main_frame, skater_frame, goalie_frame,
          roster_frame, game_frame, schedule_frame]


def clear_widgets(ex: tk.Frame) -> None:
    for frame in frames:
        if frame == ex:
            continue
        for widget in frame.winfo_children():
            widget.destroy()


def load_main_frame():
    clear_widgets(main_frame)
    main_frame.tkraise()
    root.update()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    row1 = int(window_height*0.45)
    row2 = int(window_height*0.65)

    # main_frame widgets
    tk.Label(main_frame, text="Please select a menu", bg=BG_COLOR,
             fg="white", font=("TkHeadingFont", 20)).place(anchor="center", x=window_width//2, y=int(window_height*0.15))

    tk.Button(main_frame, text="Skaters", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_skater_frame, width=10).place(anchor="center", x=window_width*0.2, y=row1)
    tk.Button(main_frame, text="Goalies", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_goalie_frame, width=10).place(anchor="center", x=window_width*0.5, y=row1)
    tk.Button(main_frame, text="Roster", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_roster_frame, width=10).place(anchor="center", x=window_width*0.8, y=row1)
    tk.Button(main_frame, text="Games", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_game_frame, width=10).place(anchor="center", x=window_width*0.33, y=row2)
    tk.Button(main_frame, text="Schedule", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_schedule_frame, width=10).place(anchor="center", x=window_width*0.66, y=row2)


def load_skater_frame():
    clear_widgets(skater_frame)
    skater_frame.tkraise()
    skater_frame.pack_propagate(False)

    # TODO: Finish frame
    tk.Label(skater_frame, text="Under Construction", bg=BG_COLOR,
             fg="white", font=("TkHeadingFont", 20)).pack(pady=30)

    tk.Button(skater_frame, text="Back", bg=BG_COLOR, font=("TkMenuFont", 18), fg="white", cursor="hand2",
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_main_frame).pack(pady=60)


def load_goalie_frame():
    clear_widgets(goalie_frame)
    goalie_frame.tkraise()
    goalie_frame.pack_propagate(False)

    # TODO: Finish frame
    tk.Label(goalie_frame, text="Under Construction", bg=BG_COLOR,
             fg="white", font=("TkHeadingFont", 20)).pack(pady=30)

    tk.Button(goalie_frame, text="Back", bg=BG_COLOR, font=("TkMenuFont", 18), fg="white", cursor="hand2",
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_main_frame).pack(pady=60)


def load_roster_frame():
    clear_widgets(roster_frame)
    roster_frame.tkraise()

    # TODO: Finish frame
    tk.Label(roster_frame, text="Under Construction", bg=BG_COLOR,
             fg="white", font=("TkHeadingFont", 20)).pack(pady=30)

    tk.Button(roster_frame, text="Back", bg=BG_COLOR, font=("TkMenuFont", 18), fg="white", cursor="hand2",
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_main_frame).pack(pady=60)


def load_game_frame():
    clear_widgets(game_frame)
    game_frame.tkraise()
    game_frame.pack_propagate(False)

    # TODO: Finish frame
    tk.Label(game_frame, text="Under Construction", bg=BG_COLOR,
             fg="white", font=("TkHeadingFont", 20)).pack(pady=30)

    tk.Button(game_frame, text="Back", bg=BG_COLOR, font=("TkMenuFont", 18), fg="white", cursor="hand2",
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_main_frame).pack(pady=60)


def load_schedule_frame():
    clear_widgets(schedule_frame)
    schedule_frame.tkraise()
    schedule_frame.pack_propagate(False)

    # TODO: Finish frame
    tk.Label(schedule_frame, text="Under Construction", bg=BG_COLOR,
             fg="white", font=("TkHeadingFont", 20)).pack(pady=30)

    tk.Button(schedule_frame, text="Back", bg=BG_COLOR, font=("TkMenuFont", 18), fg="white", cursor="hand2",
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_main_frame).pack(pady=60)


for frame in frames:
    frame.grid(row=0, column=0, sticky="news")

load_main_frame()


if __name__ == '__main__':
    root.mainloop()
