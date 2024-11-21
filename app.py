import os
import sys
import api_pull as a
import database as d
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QHBoxLayout, QLineEdit,
    QLabel, QListWidget, QPlainTextEdit, QPushButton,
    QSpacerItem, QSizePolicy, QVBoxLayout, QWidget
)

CAPS_ICON = "assets/caps_icon.ico"
CURRENT_SEASON = "2425"

# Alignments and fonts
LEFT = Qt.AlignmentFlag.AlignLeft
CENTER = Qt.AlignmentFlag.AlignCenter
RIGHT = Qt.AlignmentFlag.AlignRight
HEADER_FONT = QFont("Segoe UI Semibold", 20)
LABEL_FONT = QFont("Segoe UI Semibold", 10)
FIELD_FONT = QFont("Segoue UI", 9)
BTN_FONT = QFont("Segoe UI", 14)
BTN_SIZE = QSize(90, 30)


class MainWindow(QWidget):
    """Class for building the main menu window
    """

    def __init__(self) -> None:
        super().__init__()
        self.skater_window = None
        self.goalie_window = None
        self.roster_window = None
        self.game_window = None
        self.schedule_window = None
        self.seasons_window = None

        # Create widgets
        self.header = QLabel("Please select an option")
        self.skaters_button = QPushButton("Skaters")
        self.goalies_button = QPushButton("Goalies")
        self.roster_button = QPushButton("Roster")
        self.games_button = QPushButton("Games")
        self.schedule_button = QPushButton("Schedule")
        self.seasons_button = QPushButton("Seasons")
        self.update_button = QPushButton("Update")
        self.exit_button = QPushButton("Exit")

        # Widget groups
        btns = [
            self.skaters_button, self.goalies_button, self.roster_button,
            self.games_button, self.schedule_button, self.seasons_button,
            self.exit_button, self.update_button
        ]

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
        self.update_button.clicked.connect(
            lambda: a.bulk_update(f"data/stats_{CURRENT_SEASON}.db"))
        self.exit_button.clicked.connect(self.exit)

        # Set layout
        main_layout = QVBoxLayout()
        btn_row1 = QHBoxLayout()
        btn_row2 = QHBoxLayout()
        btn_row3 = QHBoxLayout()

        btn_row1.addWidget(self.skaters_button, alignment=CENTER)
        btn_row1.addWidget(self.goalies_button, alignment=CENTER)
        btn_row1.addWidget(self.roster_button, alignment=CENTER)
        btn_row2.addWidget(self.games_button, alignment=CENTER)
        btn_row2.addWidget(self.schedule_button, alignment=CENTER)
        btn_row2.addWidget(self.seasons_button, alignment=CENTER)
        btn_row3.addWidget(self.update_button, alignment=CENTER)
        btn_row3.addWidget(self.exit_button, alignment=CENTER)

        main_layout.addWidget(self.header, alignment=CENTER)
        main_layout.addLayout(btn_row1)
        main_layout.addLayout(btn_row2)
        main_layout.addLayout(btn_row3)

        self.setWindowTitle("Washington Capitals Stats")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(main_layout)
        self.setFixedSize(400, 300)

    def show_skater_window(self) -> None:
        if self.skater_window is None:
            self.skater_window = SkaterWindow()
        self.skater_window.show()
        self.hide()

    def show_goalie_window(self) -> None:
        if self.goalie_window is None:
            self.goalie_window = GoalieWindow()
        self.goalie_window.show()
        self.hide()

    def show_roster_window(self) -> None:
        if self.roster_window is None:
            self.roster_window = RosterWindow()
        self.roster_window.show()
        self.hide()

    def show_game_window(self) -> None:
        if self.game_window is None:
            self.game_window = GameWindow()
        self.game_window.show()
        self.hide()

    def show_schedule_window(self) -> None:
        if self.schedule_window is None:
            self.schedule_window = ScheduleWindow()
        self.schedule_window.show()
        self.hide()

    def show_seasons_window(self) -> None:
        if self.seasons_window is None:
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
        self.season_list = QComboBox()
        self.player_list = QListWidget()
        # Col2
        self.headshot = QLabel()
        self.headshot_pixmap = QPixmap("assets/team_logos/WSH.png")
        self.headshot.setPixmap(self.headshot_pixmap.scaledToWidth(200))
        # Col 3
        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.goals_label = QLabel("G")
        self.goals_input = QLineEdit()
        self.pts_per_game_label = QLabel("P/GP")
        self.pts_per_game_input = QLineEdit()
        self.shg_label = QLabel("SHG")
        self.shg_input = QLineEdit()
        # Col 4
        self.jersey_label = QLabel("#")
        self.jersey_input = QLineEdit()
        self.assists_label = QLabel("A")
        self.assists_input = QLineEdit()
        self.evg_label = QLabel("EVG")
        self.evg_input = QLineEdit()
        self.shp_label = QLabel("SHP")
        self.shp_input = QLineEdit()
        self.shots_label = QLabel("S")
        self.shots_input = QLineEdit()
        # Col 5
        self.position_label = QLabel("Pos")
        self.position_input = QLineEdit()
        self.points_label = QLabel("P")
        self.points_input = QLineEdit()
        self.evp_label = QLabel("EVP")
        self.evp_input = QLineEdit()
        self.otg_label = QLabel("OTG")
        self.otg_input = QLineEdit()
        self.shot_pctg_label = QLabel("S%")
        self.shot_pctg_input = QLineEdit()
        # Col 6
        self.shoots_label = QLabel("Sh")
        self.shoots_input = QLineEdit()
        self.plus_minus_label = QLabel("+/-")
        self.plus_minus_input = QLineEdit()
        self.ppg_label = QLabel("PPG")
        self.ppg_input = QLineEdit()
        self.gwg_label = QLabel("GWG")
        self.gwg_input = QLineEdit()
        self.fow_label = QLabel("FOW%")
        self.fow_input = QLineEdit()
        # Col 7
        self.gp_label = QLabel("GP")
        self.gp_input = QLineEdit()
        self.pim_label = QLabel("PIM")
        self.pim_input = QLineEdit()
        self.ppp_label = QLabel("PPP")
        self.ppp_input = QLineEdit()
        self.toi_label = QLabel("TOI/GP")
        self.toi_input = QLineEdit()

        self.btm_row_spacer = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.back_btn = QPushButton("Back")

        # Widget Groups
        labels = [self.name_label, self.jersey_label, self.position_label, self.shoots_label, self.gp_label,
                  self.goals_label, self.assists_label, self.points_label, self.plus_minus_label, self.pim_label,
                  self.pts_per_game_label, self.evg_label, self.evp_label, self.ppg_label, self.ppp_label,
                  self.shg_label, self.shp_label, self.otg_label, self.gwg_label, self.toi_label,
                  self.shots_label, self.shot_pctg_label, self.fow_label]
        inputs = [self.name_input, self.jersey_input, self.position_input, self.shoots_input, self.gp_input,
                  self.goals_input, self.assists_input, self.points_input, self.plus_minus_input, self.pim_input,
                  self.pts_per_game_input, self.evg_input, self.evp_input, self.ppg_input, self.ppp_input,
                  self.shg_input, self.shp_input, self.otg_input, self.gwg_input, self.toi_input,
                  self.shots_input, self.shot_pctg_input, self.fow_input]
        lists = [self.season_list, self.player_list]
        btns = [self.back_btn]

        # Configure Widgets
        for lbl in labels:
            lbl.setFont(LABEL_FONT)

        for i in inputs:
            i.setFont(FIELD_FONT)
            i.setAlignment(CENTER)
            i.setReadOnly(True)

        for l in lists:
            l.setMaximumWidth(150)
        self.player_list.addItem("Please select a season")
        self.populate_seasons_combobox()

        for b in btns:
            b.setFont(BTN_FONT)
            b.setFixedSize(BTN_SIZE)

        # Connect events
        self.back_btn.clicked.connect(self.go_back)
        self.player_list.currentItemChanged.connect(self.load_player_from_list)
        self.season_list.currentIndexChanged.connect(self.populate_player_list)

        # Set layout
        layout = QVBoxLayout()
        horiz_layout = QHBoxLayout()

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.season_list)
        list_layout.addWidget(self.player_list)

        col3 = QVBoxLayout()  # name, goals, p/gp, shg
        col3.addWidget(self.name_label, alignment=CENTER)
        col3.addWidget(self.name_input)
        col3.addWidget(self.goals_label, alignment=CENTER)
        col3.addWidget(self.goals_input)
        col3.addWidget(self.pts_per_game_label, alignment=CENTER)
        col3.addWidget(self.pts_per_game_input)
        col3.addWidget(self.shg_label, alignment=CENTER)
        col3.addWidget(self.shg_input)
        col3.addSpacerItem(self.btm_row_spacer)
        col4 = QVBoxLayout()  # jersey, assists, evg, shp, shots
        col4.addWidget(self.jersey_label, alignment=CENTER)
        col4.addWidget(self.jersey_input)
        col4.addWidget(self.assists_label, alignment=CENTER)
        col4.addWidget(self.assists_input)
        col4.addWidget(self.evg_label, alignment=CENTER)
        col4.addWidget(self.evg_input)
        col4.addWidget(self.shp_label, alignment=CENTER)
        col4.addWidget(self.shp_input)
        col4.addWidget(self.shots_label, alignment=CENTER)
        col4.addWidget(self.shots_input)
        col5 = QVBoxLayout()  # pos, points, evp, otg, s%
        col5.addWidget(self.position_label, alignment=CENTER)
        col5.addWidget(self.position_input)
        col5.addWidget(self.points_label, alignment=CENTER)
        col5.addWidget(self.points_input)
        col5.addWidget(self.evp_label, alignment=CENTER)
        col5.addWidget(self.evp_input)
        col5.addWidget(self.otg_label, alignment=CENTER)
        col5.addWidget(self.otg_input)
        col5.addWidget(self.shot_pctg_label, alignment=CENTER)
        col5.addWidget(self.shot_pctg_input)
        col6 = QVBoxLayout()  # sh, +/-, ppg, gwg, fow%
        col6.addWidget(self.shoots_label, alignment=CENTER)
        col6.addWidget(self.shoots_input)
        col6.addWidget(self.plus_minus_label, alignment=CENTER)
        col6.addWidget(self.plus_minus_input)
        col6.addWidget(self.ppg_label, alignment=CENTER)
        col6.addWidget(self.ppg_input)
        col6.addWidget(self.gwg_label, alignment=CENTER)
        col6.addWidget(self.gwg_input)
        col6.addWidget(self.fow_label, alignment=CENTER)
        col6.addWidget(self.fow_input)
        col7 = QVBoxLayout()  # gp, pim, ppp, toi/gp
        col7.addWidget(self.gp_label, alignment=CENTER)
        col7.addWidget(self.gp_input)
        col7.addWidget(self.pim_label, alignment=CENTER)
        col7.addWidget(self.pim_input)
        col7.addWidget(self.ppp_label, alignment=CENTER)
        col7.addWidget(self.ppp_input)
        col7.addWidget(self.toi_label, alignment=CENTER)
        col7.addWidget(self.toi_input)
        col7.addSpacerItem(self.btm_row_spacer)

        horiz_layout.addLayout(list_layout)
        horiz_layout.addWidget(self.headshot)
        horiz_layout.addLayout(col3)
        horiz_layout.addLayout(col4)
        horiz_layout.addLayout(col5)
        horiz_layout.addLayout(col6)
        horiz_layout.addLayout(col7)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.back_btn)

        layout.addLayout(horiz_layout)
        layout.addSpacerItem(self.btm_row_spacer)
        layout.addLayout(btn_row)
        self.setWindowTitle("Washington Capitals Skaters")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)
        self.setFixedSize(910, 320)

    def go_back(self) -> None:
        self.hide()
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
            self.name_input.setText(player_data[2])
            self.jersey_input.setText(str(player_data[3]))
            self.shoots_input.setText(player_data[4])
            self.position_input.setText(player_data[5])
            self.gp_input.setText(str(player_data[6]))
            self.goals_input.setText(str(player_data[7]))
            self.assists_input.setText(str(player_data[8]))
            self.points_input.setText(str(player_data[9]))
            self.plus_minus_input.setText(str(player_data[10]))
            self.pim_input.setText(str(player_data[11]))
            self.pts_per_game_input.setText(str(player_data[12]))
            self.evg_input.setText(str(player_data[13]))
            self.evp_input.setText(str(player_data[14]))
            self.ppg_input.setText(str(player_data[15]))
            self.ppp_input.setText(str(player_data[16]))
            self.shg_input.setText(str(player_data[17]))
            self.shp_input.setText(str(player_data[18]))
            self.otg_input.setText(str(player_data[19]))
            self.gwg_input.setText(str(player_data[20]))
            self.shots_input.setText(str(player_data[21]))
            self.shot_pctg_input.setText(str(player_data[22]))
            self.toi_input.setText(str(player_data[23]))
            self.fow_input.setText(str(player_data[24]))
        except AttributeError as e:
            print(e)


class GoalieWindow(QWidget):
    """Class for building the goalie menu window
    """

    def __init__(self) -> None:
        super().__init__()

        # Create widgets
        # Col 1
        self.season_list = QComboBox()
        self.player_list = QListWidget()
        # Col 2
        self.headshot = QLabel()
        self.headshot_pixmap = QPixmap("assets/team_logos/WSH.png")
        self.headshot.setPixmap(self.headshot_pixmap.scaledToWidth(200))
        # Col 3
        self.name_label = QLabel("Name")
        self.name_input = QLineEdit()
        self.gp_label = QLabel("GP")
        self.gp_input = QLineEdit()
        self.sa_label = QLabel("SA")
        self.sa_input = QLineEdit()
        self.so_label = QLabel("SO")
        self.so_input = QLineEdit()
        # Col 4
        self.jersey_label = QLabel("#")
        self.jersey_input = QLineEdit()
        self.gs_label = QLabel("GS")
        self.gs_input = QLineEdit()
        self.svs_label = QLabel("SVS")
        self.svs_input = QLineEdit()
        self.goals_label = QLabel("G")
        self.goals_input = QLineEdit()
        # Col 5
        self.position_label = QLabel("Pos")
        self.position_input = QLineEdit()
        self.wins_label = QLabel("W")
        self.wins_input = QLineEdit()
        self.ga_label = QLabel("GA")
        self.ga_input = QLineEdit()
        self.assists_label = QLabel("A")
        self.assists_input = QLineEdit()
        # Col 6
        self.catches_label = QLabel("C")
        self.catches_input = QLineEdit()
        self.losses_label = QLabel("L")
        self.losses_input = QLineEdit()
        self.sv_pctg_label = QLabel("SV%")
        self.sv_pctg_input = QLineEdit()
        self.points_label = QLabel("P")
        self.points_input = QLineEdit()
        # Col 7
        self.toi_label = QLabel("TOI")
        self.toi_input = QLineEdit()
        self.otl_label = QLabel("OTL")
        self.otl_input = QLineEdit()
        self.gaa_label = QLabel("GAA")
        self.gaa_input = QLineEdit()
        self.pim_label = QLabel("PIM")
        self.pim_input = QLineEdit()
        # Btns
        self.back_btn = QPushButton("Back")
        # Spacer
        self.vert_spacer = QSpacerItem(
            20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Widget groups
        labels = [self.name_label, self.jersey_label, self.position_label, self.catches_label, self.toi_label,
                  self.gp_label, self.gs_label, self.wins_label, self.losses_label, self.otl_label,
                  self.sa_label, self.svs_label, self.ga_label, self.sv_pctg_label, self.gaa_label,
                  self.so_label, self.goals_label, self.assists_label, self.points_label, self.pim_label]
        inputs = [self.name_input, self.jersey_input, self.position_input, self.catches_input, self.toi_input,
                  self.gp_input, self.gs_input, self.wins_input, self.losses_input, self.otl_input,
                  self.sa_input, self.svs_input, self.ga_input, self.sv_pctg_input, self.gaa_input,
                  self.so_input, self.goals_input, self.assists_input, self.points_input, self.pim_input]
        lists = [self.season_list, self.player_list]
        btns = [self.back_btn]

        # Configure widgets
        for lbl in labels:
            lbl.setFont(LABEL_FONT)

        for i in inputs:
            i.setFont(FIELD_FONT)
            i.setAlignment(CENTER)
            i.setReadOnly(True)

        for l in lists:
            l.setMaximumWidth(150)
        self.player_list.addItem("Please select a season")
        self.populate_seasons_combobox()

        for b in btns:
            b.setFont(BTN_FONT)
            b.setFixedSize(BTN_SIZE)

        # Connect events
        self.back_btn.clicked.connect(self.go_back)
        self.player_list.currentItemChanged.connect(self.load_goalie_from_list)
        self.season_list.currentIndexChanged.connect(self.populate_goalie_list)

        # Set layout
        layout = QVBoxLayout()
        horiz_layout = QHBoxLayout()

        list_layout = QVBoxLayout()
        list_layout.addWidget(self.season_list)
        list_layout.addWidget(self.player_list)

        col3 = QVBoxLayout()
        col3.addWidget(self.name_label, alignment=CENTER)
        col3.addWidget(self.name_input)
        col3.addWidget(self.gp_label, alignment=CENTER)
        col3.addWidget(self.gp_input)
        col3.addWidget(self.sa_label, alignment=CENTER)
        col3.addWidget(self.sa_input)
        col3.addWidget(self.so_label, alignment=CENTER)
        col3.addWidget(self.so_input)
        col4 = QVBoxLayout()
        col4.addWidget(self.jersey_label, alignment=CENTER)
        col4.addWidget(self.jersey_input)
        col4.addWidget(self.gs_label, alignment=CENTER)
        col4.addWidget(self.gs_input)
        col4.addWidget(self.svs_label, alignment=CENTER)
        col4.addWidget(self.svs_input)
        col4.addWidget(self.goals_label, alignment=CENTER)
        col4.addWidget(self.goals_input)
        col5 = QVBoxLayout()
        col5.addWidget(self.position_label, alignment=CENTER)
        col5.addWidget(self.position_input)
        col5.addWidget(self.wins_label, alignment=CENTER)
        col5.addWidget(self.wins_input)
        col5.addWidget(self.ga_label, alignment=CENTER)
        col5.addWidget(self.ga_input)
        col5.addWidget(self.assists_label, alignment=CENTER)
        col5.addWidget(self.assists_input)
        col6 = QVBoxLayout()
        col6.addWidget(self.catches_label, alignment=CENTER)
        col6.addWidget(self.catches_input)
        col6.addWidget(self.losses_label, alignment=CENTER)
        col6.addWidget(self.losses_input)
        col6.addWidget(self.sv_pctg_label, alignment=CENTER)
        col6.addWidget(self.sv_pctg_input)
        col6.addWidget(self.points_label, alignment=CENTER)
        col6.addWidget(self.points_input)
        col7 = QVBoxLayout()
        col7.addWidget(self.toi_label, alignment=CENTER)
        col7.addWidget(self.toi_input)
        col7.addWidget(self.otl_label, alignment=CENTER)
        col7.addWidget(self.otl_input)
        col7.addWidget(self.gaa_label, alignment=CENTER)
        col7.addWidget(self.gaa_input)
        col7.addWidget(self.pim_label, alignment=CENTER)
        col7.addWidget(self.pim_input)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.back_btn)

        horiz_layout.addLayout(list_layout)
        horiz_layout.addWidget(self.headshot)
        horiz_layout.addLayout(col3)
        horiz_layout.addLayout(col4)
        horiz_layout.addLayout(col5)
        horiz_layout.addLayout(col6)
        horiz_layout.addLayout(col7)

        layout.addLayout(horiz_layout)
        layout.addSpacerItem(self.vert_spacer)
        layout.addLayout(btn_row)

        self.setWindowTitle("Washington Capitals Goalies")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)
        self.setFixedSize(1073, 300)

    def go_back(self) -> None:
        self.hide()
        global w
        w.show()

    def load_goalie_from_list(self) -> None:
        try:
            curr_season = self.season_list.currentText()
            if curr_season == "-Seasons-":
                return
            name = self.player_list.currentItem().text()
            player_data = d.fetch_one(
                "goalies", "name = '" + name + "'", f"data/{self.season_dict[curr_season]}")

            # Insert data into correct fields
            player_headshot = QPixmap(
                f"assets/headshots/{player_data[2].lower().replace(" ", "_")}.png")
            self.headshot.setPixmap(player_headshot.scaledToWidth(200))
            self.name_input.setText(player_data[2])
            self.jersey_input.setText(str(player_data[3]))
            self.catches_input.setText(player_data[4])
            self.gp_input.setText(str(player_data[5]))
            self.gs_input.setText(str(player_data[6]))
            self.wins_input.setText(str(player_data[7]))
            self.losses_input.setText(str(player_data[8]))
            self.otl_input.setText(str(player_data[9]))
            self.sa_input.setText(str(player_data[10]))
            self.svs_input.setText(str(player_data[11]))
            self.ga_input.setText(str(player_data[12]))
            self.sv_pctg_input.setText(str(player_data[13]))
            self.gaa_input.setText(str(player_data[14]))
            self.toi_input.setText(player_data[15])
            self.so_input.setText(str(player_data[16]))
            self.goals_input.setText(str(player_data[17]))
            self.assists_input.setText(str(player_data[18]))
            self.points_input.setText(str(player_data[19]))
            self.pim_input.setText(str(player_data[20]))
            self.position_input.setText("G")
        except AttributeError as e:
            print(e)

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

    def populate_goalie_list(self) -> None:
        self.player_list.clear()
        curr_season = self.season_list.currentText()
        if curr_season == "-Seasons-":
            self.player_list.addItem("Please select a season")
            return
        goalies = d.fetch_all(
            "goalies", f"data/{self.season_dict[curr_season]}")
        names = []
        for goalie in goalies:
            names.append(goalie[2])
        self.player_list.addItems(names)


class RosterWindow(QWidget):
    """Class for building the roster menu window
    """

    def __init__(self) -> None:
        super().__init__()
        # Create widgets
        self.season_list = QComboBox()
        self.name_label = QLabel("Name")
        self.jersey_label = QLabel("#")
        self.sc_label = QLabel("S/C")
        self.pos_label = QLabel("Pos")
        self.ht_label = QLabel("Ht")
        self.wt_label = QLabel("Wt")
        self.born_label = QLabel("Born")
        self.bp_label = QLabel("Birthplace")
        self.back_btn = QPushButton("Back")

        # Widget groups
        labels = [
            self.name_label, self.jersey_label, self.sc_label, self.pos_label,
            self.ht_label, self.wt_label, self.born_label, self.bp_label]
        btns = [self.back_btn]

        # Configure widgets
        for lbl in labels:
            lbl.setFont(LABEL_FONT)

        self.season_list.setMaximumWidth(125)
        self.populate_seasons_combobox()

        for b in btns:
            b.setFont(BTN_FONT)
            b.setFixedSize(BTN_SIZE)

        # Connect events
        self.back_btn.clicked.connect(self.go_back)
        self.season_list.currentIndexChanged.connect(self.show_roster)

        # Set layout
        layout = QVBoxLayout()

        self.name_col = QVBoxLayout()
        self.jersey_col = QVBoxLayout()
        self.sc_col = QVBoxLayout()
        self.pos_col = QVBoxLayout()
        self.ht_col = QVBoxLayout()
        self.wt_col = QVBoxLayout()
        self.bday_col = QVBoxLayout()
        self.bplace_col = QVBoxLayout()

        self.name_col.addWidget(self.name_label)
        self.jersey_col.addWidget(self.jersey_label)
        self.sc_col.addWidget(self.sc_label)
        self.pos_col.addWidget(self.pos_label)
        self.ht_col.addWidget(self.ht_label)
        self.wt_col.addWidget(self.wt_label)
        self.bday_col.addWidget(self.born_label)
        self.bplace_col.addWidget(self.bp_label)

        table_layout = QHBoxLayout()
        table_layout.addLayout(self.name_col)
        table_layout.addLayout(self.jersey_col)
        table_layout.addLayout(self.sc_col)
        table_layout.addLayout(self.pos_col)
        table_layout.addLayout(self.ht_col)
        table_layout.addLayout(self.wt_col)
        table_layout.addLayout(self.bday_col)
        table_layout.addLayout(self.bplace_col)

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.back_btn)

        layout.addWidget(self.season_list, alignment=LEFT)
        layout.addLayout(table_layout)
        layout.addLayout(btn_row)
        self.setWindowTitle("Washington Capitals Roster")
        self.setWindowIcon(QIcon(CAPS_ICON))
        self.setLayout(layout)
        self.setMinimumSize(610, 650)

    def go_back(self) -> None:
        self.hide()
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

    def show_roster(self) -> None:
        self.clear_roster()
        try:
            curr_season = self.season_list.currentText()
            if curr_season == "-Seasons-":
                return
            roster_data = d.fetch_all(
                "roster", f"data/{self.season_dict[curr_season]}")

            # Insert the data into new fields
            names = []
            jerseys = []
            shoots_catches = []
            positions = []
            hts = []
            wts = []
            bdays = []
            bplaces = []
            for player in roster_data:
                names.append(player[2])
                jerseys.append(player[3])
                shoots_catches.append(player[4])
                positions.append(player[5])
                hts.append(player[6])
                wts.append(player[7])
                bdays.append(player[8])
                bplaces.append(player[9])

            for i in range(len(names)):
                self.name_col.insertWidget(-1, QLabel(names[i]))
                self.jersey_col.insertWidget(-1, QLabel(str(jerseys[i])))
                self.sc_col.insertWidget(-1, QLabel(shoots_catches[i]))
                self.pos_col.insertWidget(-1, QLabel(positions[i]))
                self.ht_col.insertWidget(-1, QLabel(hts[i]))
                self.wt_col.insertWidget(-1, QLabel(str(wts[i])))
                self.bday_col.insertWidget(-1, QLabel(bdays[i]))
                self.bplace_col.insertWidget(-1, QLabel(bplaces[i]))
        except AttributeError as e:
            print(e)

    def clear_roster(self) -> None:
        cols = [
            self.name_col, self.jersey_col, self.sc_col, self.pos_col,
            self.ht_col, self.wt_col, self.bday_col, self.bplace_col
        ]
        for col in cols:
            while col.count():
                item = col.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    self.clear_roster(item.layout())

        self.name_label = QLabel("Name")
        self.jersey_label = QLabel("#")
        self.sc_label = QLabel("S/C")
        self.pos_label = QLabel("Pos")
        self.ht_label = QLabel("Ht")
        self.wt_label = QLabel("Wt")
        self.born_label = QLabel("Born")
        self.bp_label = QLabel("Birthplace")

        labels = [
            self.name_label, self.jersey_label, self.sc_label, self.pos_label,
            self.ht_label, self.wt_label, self.born_label, self.bp_label
        ]
        for lbl in labels:
            lbl.setFont(LABEL_FONT)

        self.name_col.addWidget(self.name_label)
        self.jersey_col.addWidget(self.jersey_label)
        self.sc_col.addWidget(self.sc_label)
        self.pos_col.addWidget(self.pos_label)
        self.ht_col.addWidget(self.ht_label)
        self.wt_col.addWidget(self.wt_label)
        self.bday_col.addWidget(self.born_label)
        self.bplace_col.addWidget(self.bp_label)


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
        self.hide()
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
        self.hide()
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
        self.hide()
        global w
        w.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
