import PySimpleGUI as psg
import database as d

psg.set_options(font=("Arial Bold", 16))


def get_main_window() -> psg.Window:
    layout = [
        [psg.Text("Please select a menu")],
        [psg.Button("Skaters"), psg.Button("Goalies"), psg.Button("Roster")],
        [psg.Button("Games"), psg.Button("Schedule"), psg.Button("Seasons")],
        [psg.Button("Exit")]
    ]

    return psg.Window("Main Menu", layout, finalize=True)


def get_skaters_window() -> psg.Window:
    layout = []

    return psg.Window("Skaters", layout, finalize=True)


def get_goalies_window() -> psg.Window:
    layout = []

    return psg.Window("Goalies", layout, finalize=True)


def get_roster_window() -> psg.Window:
    layout = []

    return psg.Window("Roster", layout, finalize=True)


def get_game_window() -> psg.Window:
    layout = []

    return psg.Window("Games", layout, finalize=True)


def get_schedule_window() -> psg.Window:
    layout = []

    return psg.Window("Schedule", layout, finalize=True)


def get_seasons_window() -> psg.Window:
    layout = []

    return psg.Window("Season Stats", layout, finalize=True)


if __name__ == '__main__':
    main_window: psg.Window | None = get_main_window()
    skaters_window: psg.Window | None = None
    goalies_window: psg.Window | None = None
    roster_window: psg.Window | None = None
    game_window: psg.Window | None = None
    schedule_window: psg.Window | None = None
    seasons_window: psg.Window | None = None

    def close_all_windows() -> None:
        main_window = None
        skaters_window = None
        goalies_window = None
        roster_window = None
        game_window = None
        schedule_window = None
        seasons_window = None

    while True:
        window, event, values = psg.read_all_windows()
        print(window.Title, event, values)

        if event in ("Exit", psg.WIN_CLOSED):
            break
        elif event == "Back":
            window.close()
            close_all_windows()
            main_window = get_main_window()
        elif event == "Skaters":
            window.close()
            close_all_windows()
            skaters_window = get_skaters_window()
        elif event == "Goalies":
            window.close()
            close_all_windows()
            goalies_window = get_goalies_window()
        elif event == "Roster":
            window.close()
            close_all_windows()
            roster_window = get_roster_window()
        elif event == "Games":
            window.close()
            close_all_windows()
            game_window = get_game_window()
        elif event == "Schedule":
            window.close()
            close_all_windows()
            schedule_window = get_schedule_window()
        elif event == "Seasons":
            window.close()
            close_all_windows()
            seasons_window = get_seasons_window()

    window.close()
