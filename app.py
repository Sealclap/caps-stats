import tkinter as tk
import database as d

BG_COLOR = "#3d6466"
ACTIVE_COLOR = "#badee2"
FRAME_WIDTH = 700
FRAME_HEIGHT = 500

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
    btn_width = 15
    btn_height = 2

    # main_frame widgets
    tk.Label(main_frame, text="Please select a menu", bg=BG_COLOR,
             fg="white", font=("TkHeadingFont", 20)).place(anchor="center", x=window_width//2, y=int(window_height*0.15))

    tk.Button(main_frame, text="Skaters", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_skater_frame, width=btn_width, height=btn_height).place(anchor="center", x=window_width*0.2, y=row1)
    tk.Button(main_frame, text="Goalies", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_goalie_frame, width=btn_width, height=btn_height).place(anchor="center", x=window_width*0.5, y=row1)
    tk.Button(main_frame, text="Roster", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_roster_frame, width=btn_width, height=btn_height).place(anchor="center", x=window_width*0.8, y=row1)
    tk.Button(main_frame, text="Games", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_game_frame, width=btn_width, height=btn_height).place(anchor="center", x=window_width*0.33, y=row2)
    tk.Button(main_frame, text="Schedule", font=("TkMenuFont", 16), fg="white", cursor="hand2", bg=BG_COLOR,
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_schedule_frame, width=btn_width, height=btn_height).place(anchor="center", x=window_width*0.66, y=row2)


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
    root.update()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    hdr_row_y = int(window_height*0.2)
    col1_su = int(window_width*0.055)
    col2_su = int(window_width*0.224)
    col3_su = int(window_width*0.27)
    col4_su = int(window_width*0.33)
    col5_su = int(window_width*0.43)
    col6_su = int(window_width*0.505)
    col7_su = int(window_width*0.583)
    col8_su = int(window_width*0.765)

    next_row_mult = 0.25

    # TODO: Finish frame
    # Name, No, Pos, Sh/C, Ht, Wt, Bday, Bplace
    # Page header
    tk.Label(roster_frame, text="2024-2025 Roster", bg=BG_COLOR,
             fg="white", font=("TkHeaderFont", 20)).place(anchor="center", x=window_width//2, y=int(window_height*0.1))
    # Column headers
    tk.Label(roster_frame, text="Name", bg=BG_COLOR, fg="white", font=(
        "TkHeaderFont", 16)).place(anchor="w", x=col1_su, y=hdr_row_y)
    tk.Label(roster_frame, text="#", bg=BG_COLOR, fg="white", font=(
        "TkHeaderFont", 16)).place(anchor="w", x=col2_su, y=hdr_row_y)
    tk.Label(roster_frame, text="Pos", bg=BG_COLOR, fg="white", font=(
        "TkHeaderFont", 16)).place(anchor="w", x=col3_su, y=hdr_row_y)
    tk.Label(roster_frame, text="Sh/C", bg=BG_COLOR, fg="white",
             font=("TkHeaderFont", 16)).place(anchor="w", x=col4_su, y=hdr_row_y)
    tk.Label(roster_frame, text="Ht", bg=BG_COLOR, fg="white", font=(
        "TkHeaderFont", 16)).place(anchor="w", x=col5_su, y=hdr_row_y)
    tk.Label(roster_frame, text="Wt", bg=BG_COLOR, fg="white", font=(
        "TkHeaderFont", 16)).place(anchor="w", x=col6_su, y=hdr_row_y)
    tk.Label(roster_frame, text="Born", bg=BG_COLOR, fg="white", font=(
        "TkHeaderFont", 16)).place(anchor="w", x=col7_su, y=hdr_row_y)
    tk.Label(roster_frame, text="Birthplace", bg=BG_COLOR, fg="white", font=(
        "TkHeaderFont", 16)).place(anchor="w", x=col8_su, y=hdr_row_y)

    # Inputs
    col1_p = int(window_width*0.01)
    col1_width = 20
    col2_p = int(window_width*0.22)
    col2_width = 3
    col3_p = int(window_width*0.285)
    col3_width = 3
    col4_p = int(window_width*0.351)
    col4_width = 2
    col5_p = int(window_width*0.41)
    col5_width = 8
    col6_p = int(window_width*0.515)
    col6_width = 3
    col7_p = int(window_width*0.575)
    col7_width = 10
    col8_p = int(window_width*0.695)
    col8_width = 33
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col1_width).place(
        anchor="w", x=col1_p, y=int(window_height*next_row_mult))
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col2_width).place(
        anchor="w", x=col2_p, y=int(window_height*next_row_mult))
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col3_width).place(
        anchor="w", x=col3_p, y=int(window_height*next_row_mult))
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col4_width).place(
        anchor="w", x=col4_p, y=int(window_height*next_row_mult))
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col5_width).place(
        anchor="w", x=col5_p, y=int(window_height*next_row_mult))
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col6_width).place(
        anchor="w", x=col6_p, y=int(window_height*next_row_mult))
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col7_width).place(
        anchor="w", x=col7_p, y=int(window_height*next_row_mult))
    tk.Entry(roster_frame, bg="#badee2", fg="black", width=col8_width).place(
        anchor="w", x=col8_p, y=int(window_height*next_row_mult))

    # buttons
    tk.Button(roster_frame, text="Back", bg=BG_COLOR, font=("TkMenuFont", 18), fg="white", cursor="hand2",
              activebackground=ACTIVE_COLOR, activeforeground="black", command=load_main_frame).place(anchor="center", x=window_width//2, y=int(window_height*0.9))


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
