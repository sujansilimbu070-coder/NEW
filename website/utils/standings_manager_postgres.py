from database_postgres import get_connection


def get_group_standings(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    # -----------------------------
    # Get all teams with group
    # -----------------------------
    cursor.execute("""
        SELECT
            g.group_name,
            t.id,
            t.team_name
        FROM groups g
        JOIN teams t
            ON g.team_id = t.id
        WHERE g.tournament_id = %s
    """, (tournament_id,))

    teams = cursor.fetchall()

    standings = {}

    for team in teams:

        group = team["group_name"]

        if group not in standings:
            standings[group] = {}

        standings[group][team["id"]] = {
            "Team ID": team["id"],
            "Team": team["team_name"],
            "P": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "Pts": 0
        }

    # -----------------------------
    # Get played fixtures
    # -----------------------------
    cursor.execute("""
        SELECT *
        FROM fixtures
        WHERE tournament_id = %s
        AND stage = 'Group'
        AND match_status = 'Played'
    """, (tournament_id,))

    matches = cursor.fetchall()

    conn.close()

    # -----------------------------
    # Calculate standings
    # -----------------------------
    for match in matches:

        home = standings[match["group_name"]][match["home_team"]]
        away = standings[match["group_name"]][match["away_team"]]

        hs = match["home_score"]
        aw = match["away_score"]

        home["P"] += 1
        away["P"] += 1

        home["GF"] += hs
        home["GA"] += aw

        away["GF"] += aw
        away["GA"] += hs

        if hs > aw:

            home["W"] += 1
            home["Pts"] += 3

            away["L"] += 1

        elif aw > hs:

            away["W"] += 1
            away["Pts"] += 3

            home["L"] += 1

        else:

            home["D"] += 1
            away["D"] += 1

            home["Pts"] += 1
            away["Pts"] += 1

    # -----------------------------
    # Goal Difference
    # -----------------------------
    result = {}

    for group in standings:

        table = list(standings[group].values())

        for team in table:
            team["GD"] = team["GF"] - team["GA"]

        table.sort(
            key=lambda x: (
                x["Pts"],
                x["GD"],
                x["GF"]
            ),
            reverse=True
        )

        for position, team in enumerate(table, start=1):
            team["Pos"] = position

        result[group] = table

    return result