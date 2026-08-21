
from utils.knockout_rules import RULES
from utils.qualification_manager_postgres import get_qualified_teams
from database_postgres import get_connection
def generate_knockout_fixtures(tournament_id):
    """
    Generate the first knockout stage fixtures automatically.
    Supports:
        - 8 qualified teams  -> Quarter Final
        - 16 qualified teams -> Round of 16
    """

    qualified = get_qualified_teams(
        tournament_id,
        top_qualifiers=2,
        best_third=0
    )

    if not qualified:
        return []

    # Detect tournament format
    if len(qualified) == 8:
        knockout_format = "WORLD_CUP_16"

    elif len(qualified) == 16:
        knockout_format = "WORLD_CUP_32"

    else:
        return []

    rules = RULES[knockout_format]

    first_round = list(rules.keys())[0]

    # Create slot lookup
    slots = {}

    for team in qualified:

        group = team["Group"].replace("Group ", "")

        slot = f"{group}{team['Pos']}"

        slots[slot] = team

    fixtures = []

    for match_no, (home_slot, away_slot) in enumerate(
        rules[first_round],
        start=1
    ):

        if home_slot not in slots:
            return []

        if away_slot not in slots:
            return []

        home = slots[home_slot]
        away = slots[away_slot]

        fixtures.append({

            "stage": first_round,

            "match_no": match_no,

            "home_slot": home_slot,
            "away_slot": away_slot,

            "home_team_id": home["Team ID"],
            "away_team_id": away["Team ID"],

            "home_team_name": home["Team"],
            "away_team_name": away["Team"]

        })

    return fixtures


def save_knockout_fixtures(
    tournament_id,
    fixtures
):
    """
    Save the initial knockout fixtures.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM fixtures
        WHERE tournament_id = %s
          AND stage != 'Group'
    """, (tournament_id,))

    already = cursor.fetchone()["total"]

    if already > 0:

        conn.close()

        return (
            False,
            "Knockout fixtures already exist."
        )

    for match in fixtures:

        cursor.execute("""
            INSERT INTO fixtures(

                tournament_id,

                stage,

                match_no,

                home_team,

                away_team,

                home_slot,

                away_slot,

                match_status

            )
            VALUES(
                %s,%s,%s,%s,%s,%s,%s,%s
            )
        """, (

            tournament_id,

            match["stage"],

            match["match_no"],

            match["home_team_id"],

            match["away_team_id"],

            match["home_slot"],

            match["away_slot"],

            "Pending"

        ))

    conn.commit()

    conn.close()

    return (
        True,
        "Knockout fixtures generated successfully."
    )

def save_knockout_result(
    fixture_id,
    home_score,
    away_score,
    penalty_home=None,
    penalty_away=None
):
    """
    Save knockout result and winner.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            home_team,
            away_team
        FROM fixtures
        WHERE id = %s
    """, (fixture_id,))

    fixture = cursor.fetchone()

    if fixture is None:

        conn.close()

        return (
            False,
            "Fixture not found."
        )

    # Normal win

    if home_score > away_score:

        winner = fixture["home_team"]

    elif away_score > home_score:

        winner = fixture["away_team"]

    else:

        if penalty_home is None:
            conn.close()
            return (
                False,
                "Penalty required."
            )

        if penalty_away is None:
            conn.close()
            return (
                False,
                "Penalty required."
            )

        if penalty_home == penalty_away:

            conn.close()

            return (
                False,
                "Penalty cannot end in draw."
            )

        if penalty_home > penalty_away:

            winner = fixture["home_team"]

        else:

            winner = fixture["away_team"]

    cursor.execute("""

        UPDATE fixtures

        SET

            home_score = %s,

            away_score = %s,

            penalty_home = %s,

            penalty_away = %s,

            winner = %s,

            match_status = 'Played'

        WHERE id = %s

    """, (

        home_score,

        away_score,

        penalty_home,

        penalty_away,

        winner,

        fixture_id

    ))

    conn.commit()

    conn.close()

    return (
        True,
        "Result saved successfully."
    )


def all_matches_played(
    tournament_id,
    stage
):
    """
    True if every match
    in a stage has been played.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

        SELECT COUNT(*) AS remaining

        FROM fixtures

        WHERE

            tournament_id = %s

            AND stage = %s

            AND match_status != 'Played'

    """, (tournament_id, stage))

    remaining = cursor.fetchone()["remaining"]

    conn.close()

    return remaining == 0

def get_slot_index(slot):
    """
    Convert rule slots into winner index.

    Examples:
        R16-1 -> 0
        R16-8 -> 7
        QF1   -> 0
        QF4   -> 3
        SF1   -> 0
    """

    if "-" in slot:
        return int(slot.split("-")[1]) - 1

    digits = ""

    for ch in slot:
        if ch.isdigit():
            digits += ch

    return int(digits) - 1


def generate_next_stage(
    tournament_id,
    current_stage,
    next_stage
):
    """
    Generate the next knockout stage.
    """

    if not all_matches_played(
        tournament_id,
        current_stage
    ):
        return (
            False,
            f"{current_stage} is not completed."
        )

    conn = get_connection()
    cursor = conn.cursor()

    # Already exists?
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM fixtures
        WHERE tournament_id = %s
        AND stage = %s
    """, (
        tournament_id,
        next_stage
    ))

    if cursor.fetchone()["total"] > 0:
        conn.close()
        return (
            False,
            f"{next_stage} already exists."
        )

    # Load winners
    cursor.execute("""
        SELECT winner
        FROM fixtures
        WHERE tournament_id = %s
        AND stage = %s
        ORDER BY match_no
    """, (
        tournament_id,
        current_stage
    ))

    winners = [
        row["winner"]
        for row in cursor.fetchall()
    ]

    # Every match must have winner
    if None in winners:
        conn.close()
        return (
            False,
            "Some matches do not have winners."
        )

    # Select correct rule
    if current_stage == "Round of 16":

        rules = RULES["WORLD_CUP_32"]["Quarter Final"]

    elif current_stage == "Quarter Final":

        if len(winners) == 4:
            rules = RULES["WORLD_CUP_16"]["Semi Final"]

        elif len(winners) == 8:
            rules = RULES["WORLD_CUP_32"]["Semi Final"]

        else:
            conn.close()
            return (
                False,
                "Invalid Quarter Final."
            )

    elif current_stage == "Semi Final":

        if len(winners) == 2:
            rules = RULES["WORLD_CUP_16"]["Final"]

        elif len(winners) == 4:
            rules = RULES["WORLD_CUP_32"]["Final"]

        else:
            conn.close()
            return (
                False,
                "Invalid Semi Final."
            )

    else:
        conn.close()
        return (
            False,
            "Invalid stage."
        )

    # Create fixtures
    for match_no, (slot1, slot2) in enumerate(
        rules,
        start=1
    ):

        idx1 = get_slot_index(slot1)
        idx2 = get_slot_index(slot2)

        cursor.execute("""
            INSERT INTO fixtures(

                tournament_id,

                stage,

                match_no,

                home_team,

                away_team,

                match_status

            )
            VALUES(
                %s,%s,%s,%s,%s,%s
            )
        """, (

            tournament_id,

            next_stage,

            match_no,

            winners[idx1],

            winners[idx2],

            "Pending"

        ))

    conn.commit()
    conn.close()

    return (
        True,
        f"{next_stage} generated successfully."
    )

def get_knockout_fixtures(tournament_id):
    """
    Load all knockout fixtures.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            f.id,

            f.stage,

            f.match_no,

            f.home_team,

            ht.team_name AS home_team_name,

            f.away_team,

            at.team_name AS away_team_name,

            f.home_slot,

            f.away_slot,

            f.home_score,

            f.away_score,

            f.penalty_home,

            f.penalty_away,

            f.winner,

            f.match_status,
                   
            f.match_datetime

        FROM fixtures f

        LEFT JOIN teams ht
            ON f.home_team=ht.id

        LEFT JOIN teams at
            ON f.away_team=at.id

        WHERE
            f.tournament_id = %s
            AND f.stage != 'Group'

        ORDER BY

        CASE f.stage

            WHEN 'Round of 16' THEN 1

            WHEN 'Quarter Final' THEN 2

            WHEN 'Semi Final' THEN 3

            WHEN 'Third Place' THEN 4

            WHEN 'Final' THEN 5

        END,

        f.match_no

    """,(tournament_id,))

    fixtures=[
        dict(row)
        for row in cursor.fetchall()
    ]

    conn.close()

    return fixtures

def get_champion(tournament_id):
    """
    Return champion team name if the Final
    has been completed.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.team_name
        FROM fixtures f

        JOIN teams t
            ON f.winner = t.id

        WHERE
            f.tournament_id = %s
            AND f.stage = 'Final'
            AND f.match_status = 'Played'

        LIMIT 1
    """, (tournament_id,))

    champion = cursor.fetchone()

    conn.close()

    if champion is None:
        return None

    return champion["team_name"]