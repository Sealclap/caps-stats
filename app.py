import os
import sys
import database as d
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QHBoxLayout, QLineEdit,
    QLabel, QListWidget, QPlainTextEdit, QPushButton,
    QVBoxLayout, QWidget
)

CAPS_ICON = "assets/caps_icon.ico"

# Alignments and fonts
LEFT = Qt.AlignmentFlag.AlignLeft
CENTER = Qt.AlignmentFlag.AlignCenter
RIGHT = Qt.AlignmentFlag.AlignRight
HEADER_FONT = QFont("Segoe UI Semibold", 20)
BTN_FONT = QFont("Segoe UI", 14)


class MainWindow(QWidget):
    """Class for building the main menu window
    """

    def __init__(self) -> None:
        super().__init__()
        # Create widgets
        self.header = QLabel("Please select a menu")
        self.skaters_button = QPushButton("Skaters")
        self.goalies_button = QPushButton("Goalies")
        self.roster_button = QPushButton("Roster")
        self.games_button = QPushButton("Games")
        self.schedule_button = QPushButton("Schedule")
        self.seasons_button = QPushButton("Seasons")
        self.exit_button = QPushButton("Exit")

        # Widget groups
        btns = [
            self.skaters_button, self.goalies_button, self.roster_button,
            self.games_button, self.schedule_button, self.seasons_button,
            self.exit_button
        ]
        all_widgets = [self.header] + btns

        # Configure widgets
        self.header.setFont(HEADER_FONT)
        self.header.setContentsMargins(20, 20, 20, 20)
        for btn in btns:
            btn.setFont(BTN_FONT)
            btn.setFixedSize(120, 50)

        # Connect buttons
        self.skaters_button.clicked.connect(self.show_skater_window)
        self.goalies_button.clicked.connect(self.show_goalie_window)
        self.roster_button.clicked.connect(self.show_roster_window)
        self.games_button.clicked.connect(self.show_game_window)
        self.schedule_button.clicked.connect(self.show_schedule_window)
        self.seasons_button.clicked.connect(self.show_seasons_window)
        self.exit_button.clicked.connect(self.exit)

        # Set layout
        main_layout = QVBoxLayout()
        btn_row1 = QHBoxLayout()
        btn_row2 = QHBoxLayout()

        btn_row1.addWidget(self.skaters_button, alignment=CENTER)
        btn_row1.addWidget(self.goalies_button, alignment=CENTER)
        btn_row1.addWidget(self.roster_button, alignment=CENTER)
        btn_row2.addWidget(self.games_button, alignment=CENTER)
        btn_row2.addWidget(self.schedule_button, alignment=CENTER)
        btn_row2.addWidget(self.seasons_button, alignment=CENTER)

        main_layout.addWidget(self.header, alignment=CENTER)
        main_layout.addLayout(btn_row1)
        main_layout.addLayout(btn_row2)
        main_layout.addWidget(self.exit_button, alignment=CENTER)

        self.setWindowTitle("Washington Capitals Stats")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(main_layout)
        self.setFixedSize(400, 300)

    def show_skater_window(self) -> None:
        self.skater_window = SkaterWindow()
        self.skater_window.show()
        self.hide()

    def show_goalie_window(self) -> None:
        self.goalie_window = GoalieWindow()
        self.goalie_window.show()
        self.hide()

    def show_roster_window(self) -> None:
        self.roster_window = RosterWindow()
        self.roster_window.show()
        self.hide()

    def show_game_window(self) -> None:
        self.game_window = GameWindow()
        self.game_window.show()
        self.hide()

    def show_schedule_window(self) -> None:
        self.schedule_window = ScheduleWindow()
        self.schedule_window.show()
        self.hide()

    def show_seasons_window(self) -> None:
        self.seasons_window = SeasonsWindow()
        self.seasons_window.show()
        self.hide()

    def exit(self) -> None:
        self.close()


class SkaterWindow(QWidget):
    """Class for building the skater menu window
    """

    def __init__(self) -> None:
        super().__init__()
        # Create widgets
        # Col 1
        self.player_list = QListWidget()
        self.season_list = QComboBox()
        # Col2
        self.headshot = QLabel()
        self.headshot_pixmap = QPixmap("assets/team_logos/WSH.png")
        self.headshot.setPixmap(self.headshot_pixmap.scaledToWidth(200))
        # Col 3 - G, P/GP, SHG
        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        # Col 4 - A, EVG, SHP, S
        self.jersey_label = QLabel("#")
        self.jersey_input = QLineEdit()
        # Col 5 - P, EVP, OTG, S%
        self.position_label = QLabel("Pos")
        self.position_input = QLineEdit()
        # Col 6 - +/-, PPG, GWG, FOW%
        self.shoots_label = QLabel("Sh")
        self.shoots_input = QLineEdit()
        # Col 7 - PIM, PPP, TOI/GP
        self.gp_label = QLabel("GP")
        self.gp_input = QLineEdit()

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)

        # Widget Groups

        # Configure Widgets
        self.player_list.addItem("Please select a season")
        self.player_list.currentItemChanged.connect(self.load_player_from_list)
        self.populate_seasons_combobox()

        # Connect events
        self.season_list.currentIndexChanged.connect(self.populate_player_list)

        # Set layout
        layout = QHBoxLayout()

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.season_list)
        list_layout.addWidget(self.player_list)

        layout.addLayout(list_layout)
        self.setWindowTitle("Washington Capitals Skaters")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)

    def go_back(self) -> None:
        self.close()
        global w
        w.show()

    def populate_seasons_combobox(self) -> None:
        data_files = os.listdir("data")
        db_files = [db for db in data_files if db.startswith("stats_")]
        seasons_raw = [s[s.index("_")+1:s.index(".db")] for s in db_files]
        seasons_fmt = [f"20{s[:2]}-20{s[2:]}" for s in seasons_raw]
        self.season_list.addItems(["-Seasons-"] + seasons_fmt)
        # Add seasons to dict for easier conversion later
        self.season_dict = {}
        for i in range(len(db_files)):
            self.season_dict[seasons_fmt[i]] = db_files[i]

    def populate_player_list(self) -> None:
        self.player_list.clear()
        curr_season = self.season_list.currentText()
        if curr_season == "-Seasons-":
            self.player_list.addItem("Please select a season")
            return
        players = d.fetch_all(
            "skaters", f"data/{self.season_dict[curr_season]}")
        names = []
        for player in players:
            names.append(player[2])
        self.player_list.addItems(names)

    def load_player_from_list(self) -> None:
        try:
            curr_season = self.season_list.currentText()
            if curr_season == "-Seasons-":
                return
            name = self.player_list.currentItem().text()
            player_data = d.fetch_one(
                "skaters", "name = '" + name + "'", f"data/{self.season_dict[curr_season]}")

            # Insert the data into the correct fields
            player_headshot = QPixmap(
                f"assets/headshots/{player_data[2].lower().replace(" ", "_")}.png")
            self.headshot.setPixmap(player_headshot.scaledToWidth(200))
        except AttributeError as e:
            print(e)


class GoalieWindow(QWidget):
    """Class for building the goalie menu window
    """

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        self.setWindowTitle("Washington Capitals Goalies")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)

    def go_back(self) -> None:
        self.close()
        global w
        w.show()


class RosterWindow(QWidget):
    """Class for building the roster menu window
    """

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        self.setWindowTitle("Washington Capitals Roster")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)

    def go_back(self) -> None:
        self.close()
        global w
        w.show()


class GameWindow(QWidget):
    """Class for building the game menu window
    """

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        self.setWindowTitle("Washington Capitals Games")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)

    def go_back(self) -> None:
        self.close()
        global w
        w.show()


class ScheduleWindow(QWidget):
    """Class for building the schedule window
    """

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        self.setWindowTitle("Washington Capitals Schedule")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)

    def go_back(self) -> None:
        self.close()
        global w
        w.show()


class SeasonsWindow(QWidget):
    """Class for building the season stats window
    """

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)
        layout.addWidget(self.back_btn)

        self.setWindowTitle("Washington Capitals Season Stats")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)

    def go_back(self) -> None:
        self.close()
        global w
        w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
