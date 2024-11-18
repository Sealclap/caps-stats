import requests as r
import pandas as pd

game_api_head = "https://api-web.nhle.com/v1/score/"
landing_api_head = "https://api-web.nhle.com/v1/gamecenter/"
landing_api_tail = "/landing"
box_score_api_head = "https://api-web.nhle.com/v1/gamecenter/"
box_score_api_tail = "/boxscore"


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


def pull_multiple_games(dates: list[str]) -> None:
    # TODO: Pull multiple games at once
    ...


if __name__ == '__main__':
    ...
