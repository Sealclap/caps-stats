import requests as r
import pandas as pd
import database as d

roster_api: str = "https://api-web.nhle.com/v1/club-stats/WSH/now"
player_api_head: str = "https://api-web.nhle.com/v1/player/"
player_api_tail: str = "/landing"
game_api_head: str = "https://api-web.nhle.com/v1/score/"
schedule_api: str = "https://api-web.nhle.com/v1/club-schedule-season/WSH/now"
landing_api_head: str = "https://api-web.nhle.com/v1/gamecenter/"
landing_api_tail: str = "/landing"
box_score_api_head: str = "https://api-web.nhle.com/v1/gamecenter/"
box_score_api_tail: str = "/boxscore"


def pull_roster() -> None:
    """Pulls the current Roster from the NHL API and saves to .csv file
    """
    team = r.get(roster_api).json()
    skaters = team["skaters"]
    goalies = team["goalies"]
    roster_data = []

    for sk in skaters:
        data = r.get(f"{player_api_head}{sk["playerId"]}{
                     player_api_tail}").json()
        player_id = data["playerId"]
        name = f"{data["firstName"]["default"]} {data["lastName"]["default"]}"
        jersey = data["sweaterNumber"]
        s_c = data["shootsCatches"]
        pos = data["position"]
        headshot = data["headshot"]
        height_in_inches = data["heightInInches"]
        height_in_feet = height_in_inches // 12
        height_str = f"{height_in_feet}'{
            height_in_inches-(height_in_feet*12)}\""
        weight = data["weightInPounds"]
        birth_date = d.reformat_date(data["birthDate"])
        if "birthStateProvince" in data:
            birthplace = f"{data["birthCity"]["default"]}, {
                data["birthStateProvince"]["default"]}, {data["birthCountry"]}"
        else:
            birthplace = f"{data["birthCity"]["default"]}, {
                data["birthCountry"]}"

        roster_data.append((player_id, headshot, name, jersey,
                            s_c, pos, height_str, weight, birth_date, birthplace))

    for go in goalies:
        data = r.get(f"{player_api_head}{go["playerId"]}{
                     player_api_tail}").json()
        player_id = data["playerId"]
        name = f"{data["firstName"]["default"]} {data["lastName"]["default"]}"
        headshot = data["headshot"]
        jersey = data["sweaterNumber"]
        s_c = data["shootsCatches"]
        pos = data["position"]
        height_in_inches = data["heightInInches"]
        height_in_feet = height_in_inches // 12
        height_str = f"{height_in_feet}'{
            height_in_inches-(height_in_feet*12)}\""
        weight = data["weightInPounds"]
        birth_date = d.reformat_date(data["birthDate"])
        if "birthStateProvince" in data:
            birthplace = f"{data["birthCity"]["default"]}, {
                data["birthStateProvince"]["default"]}, {data["birthCountry"]}"
        else:
            birthplace = f"{data["birthCity"]["default"]}, {
                data["birthCountry"]}"

        roster_data.append((player_id, headshot, name, jersey,
                            s_c, pos, height_str, weight, birth_date, birthplace))

    roster_cols = ["player_id", "headshot", "name", "jersey", "s/c", "pos", "ht", "wt",
                   "born", "birthplace"]
    roster_df = pd.DataFrame(roster_data, columns=roster_cols)
    roster_df.to_csv("to_load/roster_from_api.csv", index=False)


def pull_skaters() -> None:
    """Pulls all Washington Skaters stats from the NHL API and saves to .csv file
    """
    team = r.get(roster_api).json()
    skaters = team["skaters"]
    skater_data = []
    for sk in skaters:
        data = r.get(f"{player_api_head}{sk["playerId"]}{
                     player_api_tail}").json()
        player_id = data["playerId"]
        name = f"{data["firstName"]["default"]} {data["lastName"]["default"]}"
        jersey = data["sweaterNumber"]
        s_c = data["shootsCatches"]
        pos = data["position"]
        gp = data["featuredStats"]["regularSeason"]["subSeason"]["gamesPlayed"]
        goals = data["featuredStats"]["regularSeason"]["subSeason"]["goals"]
        assists = data["featuredStats"]["regularSeason"]["subSeason"]["assists"]
        points = data["featuredStats"]["regularSeason"]["subSeason"]["points"]
        plus_minus = data["featuredStats"]["regularSeason"]["subSeason"]["plusMinus"]
        pim = data["featuredStats"]["regularSeason"]["subSeason"]["pim"]
        pts_per_game = "{:.2f}".format(round(points/gp, 2))
        ppg = data["featuredStats"]["regularSeason"]["subSeason"]["powerPlayGoals"]
        ppp = data["featuredStats"]["regularSeason"]["subSeason"]["powerPlayPoints"]
        shg = data["featuredStats"]["regularSeason"]["subSeason"]["shorthandedGoals"]
        shp = data["featuredStats"]["regularSeason"]["subSeason"]["shorthandedPoints"]
        evg = goals - (ppg + shg)
        evp = points - (ppp + shp)
        otg = data["featuredStats"]["regularSeason"]["subSeason"]["otGoals"]
        gwg = data["featuredStats"]["regularSeason"]["subSeason"]["gameWinningGoals"]
        shots = data["featuredStats"]["regularSeason"]["subSeason"]["shots"]
        shot_p = data["featuredStats"]["regularSeason"]["subSeason"]["shootingPctg"]
        shot_p = "{:.1f}".format(round(shot_p*100, 1))
        fow = "{:.1f}".format(round(sk["faceoffWinPctg"]*100, 1))
        toipg_in_secs = sk["avgTimeOnIcePerGame"]
        toipg_mins = int(toipg_in_secs // 60)
        toipg_secs = int(toipg_in_secs - (toipg_mins * 60))
        toipg = f"{toipg_mins}:{toipg_secs:02}"
        headshot = data["headshot"]

        skater_data.append((player_id, headshot, name, jersey, s_c, pos, gp, goals, assists, points,
                            plus_minus, pim, pts_per_game, evg, evp, ppg, ppp, shg, shp, otg, gwg, shots, shot_p, toipg, fow))

    skater_cols = ["player_id", "headshot", "name", "jersey", "s/c", "pos", "gp", "g",
                   "a", "p", "+/-", "pim", "p/gp", "evg", "evp", "ppg", "ppp",
                   "shg", "shp", "otg", "gwg", "s", "s%", "toi/gp", "fow%"]
    skater_df = pd.DataFrame(skater_data, columns=skater_cols)
    skater_df.to_csv("to_load/skaters_from_api.csv", index=False)


def pull_goalies() -> None:
    """Pulls all Washington Goalies stats from the NHL API and saves to .csv file
    """
    team = r.get(roster_api).json()
    goalies = team["goalies"]

    goalie_data = []
    for go in goalies:
        data = r.get(f"{player_api_head}{go["playerId"]}{
                     player_api_tail}").json()
        player_id = data["playerId"]
        name = f"{data["firstName"]["default"]} {data["lastName"]["default"]}"
        headshot = data["headshot"]
        jersey = data["sweaterNumber"]
        s_c = data["shootsCatches"]
        gp = data["featuredStats"]["regularSeason"]["subSeason"]["gamesPlayed"]
        gs = go["gamesStarted"]
        wins = data["featuredStats"]["regularSeason"]["subSeason"]["wins"]
        losses = data["featuredStats"]["regularSeason"]["subSeason"]["losses"]
        ot_losses = data["featuredStats"]["regularSeason"]["subSeason"]["otLosses"]
        sa = go["shotsAgainst"]
        svs = go["saves"]
        ga = go["goalsAgainst"]
        svp = "{:.3f}".format(
            round(data["featuredStats"]["regularSeason"]["subSeason"]["savePctg"], 3))
        gaa = "{:.2f}".format(
            round(data["featuredStats"]["regularSeason"]["subSeason"]["goalsAgainstAvg"], 2))
        toi_in_secs = go["timeOnIce"]
        toi_mins = toi_in_secs // 60
        toi_secs = toi_in_secs - (toi_mins * 60)
        toi = f"{toi_mins}:{toi_secs}"
        so = go["shutouts"]
        goals = go["goals"]
        assists = go["assists"]
        points = go["points"]
        pim = go["penaltyMinutes"]

        goalie_data.append((player_id, headshot, name, jersey, s_c, gp, gs, wins,
                            losses, ot_losses, sa, svs, ga, svp, gaa, toi, so, goals, assists, points, pim))

    goalie_cols = ["player_id", "headshot", "name", "jersey", "s/c", "gp", "gs", "w",
                   "l", "otl", "sa", "svs", "ga", "sv%", "gaa", "toi", "so", "g", "a",
                   "p", "pim"]
    goalie_df = pd.DataFrame(goalie_data, columns=goalie_cols)
    goalie_df.to_csv("to_load/goalies_from_api.csv", index=False)


def pull_all_player_data() -> None:
    """Pulls goalie, skater, and roster data from the NHL API and saves to .csv files
    """
    pull_roster()
    pull_skaters()
    pull_goalies()


def bulk_update(db_path: str) -> None:
    """Updates all tables using the NHL API except `games` and `seasons`

    Args:
        db_path (str): path to desired db (ex. 'data/stats_2425.db')
    """
    pull_all_player_data()
    pull_current_schedule()
    d.load_file("to_load/skaters_from_api.csv",
                "skaters", [], "replace", db_path)
    d.load_file("to_load/goalies_from_api.csv",
                "goalies", [], "replace", db_path)
    d.load_file("to_load/roster_from_api.csv", "roster",
                [], "replace", db_path)
    d.load_file("to_load/schedule_from_api.csv",
                "schedule", [], "replace", db_path)


def pull_game_by_id(game_id: str | int) -> None:
    data = r.get(f"{landing_api_head}{game_id}{landing_api_tail}").json()

    if data["awayTeam"]["id"] == 15:
        home_away = "away"
        opp_home_away = "home"
    else:
        home_away = "home"
        opp_home_away = "away"

    caps_data = data[f"{home_away}Team"]
    opponent_data = data[f"{opp_home_away}Team"]
    summary_data = data["summary"]
    scoring_data = summary_data["scoring"]

    # Get goals
    caps_goals = []
    opp_goals = []
    for period in scoring_data:
        period_descriptor = period["periodDescriptor"]["number"]
        period_goals_data = period["goals"]

        for goal in period_goals_data:
            scorer = f"{goal["firstName"]["default"]} {
                goal["lastName"]["default"]} ({goal["goalsToDate"]})"

            if goal["strength"] != "ev":
                scorer += f" {goal["strength"].upper()}"

            if goal["goalModifier"] == "empty-net":
                scorer += " EN"

            time_in_period = goal["timeInPeriod"]

            assists = []
            for assist in goal["assists"]:
                assister = f"{assist["name"]["default"]
                              } ({assist["assistsToDate"]})"
                assists.append(assister)

            if len(assists) == 0:
                assists.append("Unassisted")

            goal_str = f"{
                scorer} - P{period_descriptor} {time_in_period} ({", ".join(assists)})"

            if goal["teamAbbrev"]["default"] == "WSH":
                caps_goals.append(goal_str)
            else:
                opp_goals.append(goal_str)

    if len(caps_goals) == 0:
        caps_goals.append("None")
    if len(opp_goals) == 0:
        opp_goals.append("None")

    # Get penalties
    if "penalties" in summary_data:
        penalty_data = summary_data["penalties"]

        caps_penalties = []
        opp_penalties = []
        for period in penalty_data:
            period_descriptor = period["periodDescriptor"]["number"]
            period_penalties_data = period["penalties"]

            for penalty in period_penalties_data:
                duration = f"{penalty["duration"]}min"
                infraction = penalty["descKey"]
                committed_by = penalty["committedByPlayer"] if penalty["type"] != "BEN" else "Bench"
                time_in_period = penalty["timeInPeriod"]

                penalty_str = f"{
                    committed_by} - {infraction} ({duration}) P{period_descriptor} {time_in_period}"

                if penalty["teamAbbrev"]["default"] == "WSH":
                    caps_penalties.append(penalty_str)
                else:
                    opp_penalties.append(penalty_str)

        if len(caps_penalties) == 0:
            caps_penalties.append("None")
        if len(opp_penalties) == 0:
            opp_penalties.append("None")

    # Get three stars
    stars_data = summary_data["threeStars"]

    stars = []
    for star in stars_data:
        stars.append(f"{star["name"]["default"]} {star["position"]}{
                     star["sweaterNo"]} ({star["teamAbbrev"]})")

    # Get team stats
    game_story = r.get(
        f"https://api-web.nhle.com/v1/wsc/game-story/{game_id}").json()
    game_date = game_story["gameDate"]
    team_stats_data = game_story["summary"]["teamGameStats"]

    is_home = home_away == "home"
    home_stats = {}
    away_stats = {}
    for cat in team_stats_data:
        category = cat["category"]

        home_stats[category] = cat["homeValue"]
        away_stats[category] = cat["awayValue"]

    opponent = f"{opponent_data["placeName"]["default"]} {
        opponent_data["name"]["default"]}"
    # Used to fix "Utah Utah Hockey Club" error from API
    new_opponent = []
    for word in opponent.split():
        if word in new_opponent:
            continue
        new_opponent.append(word)
    opponent = " ".join(new_opponent)

    opp_score = opponent_data["score"]
    opp_sog = opponent_data["sog"]
    opp_fop = round(away_stats["faceoffWinningPctg"]*100,
                    1) if is_home else round(home_stats["faceoffWinningPctg"]*100, 1)
    opp_ppn = away_stats["powerPlay"] if is_home else home_stats["powerPlay"]
    opp_ppp = round(away_stats["powerPlayPctg"]*100,
                    1) if is_home else round(home_stats["powerPlayPctg"]*100, 1)
    opp_pim = away_stats["pim"] if is_home else home_stats["pim"]
    opp_hits = away_stats["hits"] if is_home else home_stats["hits"]
    opp_bs = away_stats["blockedShots"] if is_home else home_stats["blockedShots"]
    opp_gv = away_stats["giveaways"] if is_home else home_stats["giveaways"]
    opp_tk = away_stats["takeaways"] if is_home else home_stats["takeaways"]

    caps_score = caps_data["score"]
    caps_sog = caps_data["sog"]
    caps_fop = round(home_stats["faceoffWinningPctg"]*100,
                     1) if is_home else round(away_stats["faceoffWinningPctg"]*100, 1)
    caps_ppn = home_stats["powerPlay"] if is_home else away_stats["powerPlay"]
    caps_ppp = round(home_stats["powerPlayPctg"]*100,
                     1) if is_home else round(away_stats["powerPlayPctg"]*100, 1)
    caps_pim = home_stats["pim"] if is_home else away_stats["pim"]
    caps_hits = home_stats["hits"] if is_home else away_stats["hits"]
    caps_bs = home_stats["blockedShots"] if is_home else away_stats["blockedShots"]
    caps_gv = home_stats["giveaways"] if is_home else away_stats["giveaways"]
    caps_tk = home_stats["takeaways"] if is_home else away_stats["takeaways"]

    result = "Win" if caps_score > opp_score else "Loss"
    if len(scoring_data) == 4:
        result += " (OT)"
    elif len(scoring_data) > 4:
        result += " (OT+)"

    box_score_data = r.get(f"{box_score_api_head}{game_id}{
                           box_score_api_tail}").json()
    caps_goalie = ""
    opp_goalie = ""

    all_goalies = [box_score_data["playerByGameStats"]["homeTeam"]
                   ["goalies"], box_score_data["playerByGameStats"]["awayTeam"]["goalies"]]
    starting_goalies = {}

    for i in range(2):
        for j in range(len(all_goalies[i])):
            if all_goalies[i][j]["starter"] == False:
                continue

            goalie_name = all_goalies[i][j]["name"]["default"]
            if i == 0:
                starting_goalies["home"] = goalie_name
            else:
                starting_goalies["away"] = goalie_name

    if is_home:
        caps_goalie = starting_goalies["home"]
        opp_goalie = starting_goalies["away"]
    else:
        caps_goalie = starting_goalies["away"]
        opp_goalie = starting_goalies["home"]

    game_columns = ["opponent", "home_away", "date", "date_str", "goalie", "opp_goalie", "sog", "opp_sog",
                    "fop", "opp_fop", "pp", "ppp", "opp_pp", "opp_ppp", "pim", "opp_pim", "hits", "opp_hits",
                    "bs", "opp_bs", "gv", "opp_gv", "tk", "opp_tk", "goals", "opp_goals", "penalties",
                    "opp_penalties", "stars", "result"]

    game_df = pd.DataFrame([(opponent, home_away, game_date, game_date, caps_goalie, opp_goalie, caps_sog, opp_sog,
                            caps_fop, opp_fop, caps_ppn, caps_ppp, opp_ppn, opp_ppp, caps_pim, opp_pim, caps_hits,
                            opp_hits, caps_bs, opp_bs, caps_gv, opp_gv, caps_tk, opp_tk, caps_goals, opp_goals,
                            caps_penalties, opp_penalties, stars, result)], columns=game_columns)
    game_df.to_csv(f"to_load/game_{game_date}.csv", index=False)


def pull_game_by_date(date: str = "now") -> None:
    data = r.get(f"{game_api_head}{date}").json()
    for game in data["games"]:
        if game["awayTeam"]["id"] == 15 or game["homeTeam"]["id"] == 15:
            pull_game_by_id(game["id"])


def pull_current_schedule() -> None:
    """Pulls the current schedule from the NHL API and saves to .csv file
    """
    data = r.get(schedule_api).json()
    game_data = data["games"]

    season_games = []
    for game in game_data:
        if game["gameType"] == 1:
            continue
        date = game["gameDate"]
        start_time_utc_split = game["startTimeUTC"].split("T")
        year, month, day = start_time_utc_split[0].split("-")
        start_time_str = start_time_utc_split[1][:-1]
        hour, min, _ = start_time_str.split(":")
        start_timestamp_utc = pd.Timestamp(
            year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(min), tz="UTC")
        start_timestamp_est = start_timestamp_utc.tz_convert("US/Eastern")
        home_team = f"{game["homeTeam"]["placeName"]["default"]} {
            game["homeTeam"]["commonName"]["default"]}"
        away_team = f"{game["awayTeam"]["placeName"]["default"]} {
            game["awayTeam"]["commonName"]["default"]}"
        is_home = home_team == "Washington Capitals"
        season_games.append(
            (date, start_timestamp_est.strftime("%I:%M %p"), home_team, away_team, is_home))

    schedule_columns = ["date", "time", "home_team", "away_team", "is_home"]
    schedule_df = pd.DataFrame(season_games, columns=schedule_columns)
    schedule_df.to_csv("to_load/schedule_from_api.csv", index=False)


if __name__ == '__main__':
    pull_game_by_date("2024-11-18")
    d.load_file("to_load/game_2024-11-18.csv", "games",
                [], "append", "data/stats_2425.db")
