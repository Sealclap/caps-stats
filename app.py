import sys
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget)
import database as d

CAPS_ICON = "assets/caps_icon.ico"


class MainWindow(QWidget):
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

        # Connect buttons
        self.skaters_button.clicked.connect(self.show_skater_window)
        self.goalies_button.clicked.connect(self.show_goalie_window)
        self.roster_button.clicked.connect(self.show_roster_window)
        self.games_button.clicked.connect(self.show_game_window)
        self.schedule_button.clicked.connect(self.show_schedule_window)
        self.seasons_button.clicked.connect(self.show_seasons_window)

        # Set layout
        main_layout = QVBoxLayout()
        btn_row1 = QHBoxLayout()
        btn_row2 = QHBoxLayout()

        btn_row1.addWidget(self.skaters_button)
        btn_row1.addWidget(self.goalies_button)
        btn_row1.addWidget(self.roster_button)
        btn_row2.addWidget(self.games_button)
        btn_row2.addWidget(self.schedule_button)
        btn_row2.addWidget(self.seasons_button)

        main_layout.addWidget(self.header)
        main_layout.addLayout(btn_row1)
        main_layout.addLayout(btn_row2)

        self.setWindowTitle("Washington Capitals Stats")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(main_layout)

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


class SkaterWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        # Create widgets
        self.label = QLabel()
        self.headshot = QPixmap("assets/headshots/alex_ovechkin.png")
        self.label.setPixmap(self.headshot.scaledToWidth(200))
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)

        layout = QHBoxLayout()
        layout.addWidget(self.back_btn)
        layout.addWidget(self.label)
        self.setWindowTitle("Washington Capitals Skaters")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)

    def go_back(self) -> None:
        self.close()
        global w
        w.show()


class GoalieWindow(QWidget):
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
