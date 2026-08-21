from database_postgres import get_connection
from utils.tournament_manager_postgres import update_tournament_status


# =====================================================
# Check if Fixtures Exist
# =====================================================

def fixtures_exist(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM fixtures
        WHERE tournament_id = %s
    """, (tournament_id,))

    total = cursor.fetchone()["total"]

    conn.close()

    return total > 0


# =====================================================
# Delete Fixtures
# =====================================================

def delete_fixtures(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM fixtures
        WHERE tournament_id = %s
    """, (tournament_id,))

    conn.commit()
    conn.close()


# =====================================================
# Get Single Fixture
# =====================================================

def get_fixture(fixture_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM fixtures
        WHERE id = %s
    """, (fixture_id,))

    fixture = cursor.fetchone()

    conn.close()

    return fixture


# =====================================================
# Generate Group Fixtures
# =====================================================

def generate_group_fixtures(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    # Prevent duplicate generation
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM fixtures
        WHERE tournament_id = %s
    """, (tournament_id,))

    if cursor.fetchone()["total"] > 0:
        conn.close()
        return False, "Fixtures have already been generated."

    cursor.execute("""
        SELECT DISTINCT group_name
        FROM groups
        WHERE tournament_id = %s
        ORDER BY group_name
    """, (tournament_id,))

    groups = cursor.fetchall()

    if not groups:
        conn.close()
        return False, "Please generate groups first."

    total_matches = 0

    for group in groups:

        group_name = group["group_name"]

        cursor.execute("""
            SELECT
                t.id,
                t.team_name
            FROM groups g
            JOIN teams t
                ON g.team_id = t.id
            WHERE g.tournament_id = %s
            AND g.group_name = %s
            ORDER BY t.team_name
        """, (tournament_id, group_name))

        teams = cursor.fetchall()

        match_no = 1

        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):

                cursor.execute("""
                    INSERT INTO fixtures (
                        tournament_id,
                        stage,
                        round_no,
                        group_name,
                        match_no,
                        home_team,
                        away_team,
                        match_status
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    tournament_id,
                    "Group",
                    1,
                    group_name,
                    match_no,
                    teams[i]["id"],
                    teams[j]["id"],
                    "Pending"
                ))

                match_no += 1
                total_matches += 1

    conn.commit()
    conn.close()

    return True, f"{total_matches} fixtures generated successfully."

# =====================================================
# Get Group Fixtures
# =====================================================

def get_group_fixtures(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT

            f.id,
            f.group_name,
            f.match_no,

            ht.team_name AS home_team,
            at.team_name AS away_team,

            f.home_score,
            f.away_score,

            f.match_status,
            f.match_datetime

        FROM fixtures f

        JOIN teams ht
            ON f.home_team = ht.id

        JOIN teams at
            ON f.away_team = at.id

        WHERE
            f.tournament_id = %s
            AND f.stage = 'Group'

        ORDER BY
            f.group_name,
            f.match_no
    """, (tournament_id,))

    fixtures = cursor.fetchall()

    conn.close()

    return fixtures
# =====================================================
# Save / Update Match Result
# =====================================================

def save_match_result(fixture_id, home_score, away_score):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM fixtures
        WHERE id = %s
    """, (fixture_id,))

    fixture = cursor.fetchone()

    if fixture is None:

        conn.close()
        return False, "Fixture not found."

    winner = None

    if home_score > away_score:
        winner = fixture["home_team"]

    elif away_score > home_score:
        winner = fixture["away_team"]

    cursor.execute("""
        UPDATE fixtures
        SET
            home_score = %s,
            away_score = %s,
            winner = %s,
            match_status = 'Played'
        WHERE id = %s
    """, (
        home_score,
        away_score,
        winner,
        fixture_id
    ))

    conn.commit()

    # ---------------------------------------
    # Check if Group Stage is Complete
    # ---------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM fixtures
        WHERE tournament_id = %s
        AND stage = 'Group'
        AND match_status = 'Pending'
    """, (fixture["tournament_id"],))

    pending = cursor.fetchone()["total"]

    conn.close()

    if pending == 0:

        print("✅ ALL GROUP MATCHES COMPLETED")

        result = update_tournament_status(
            fixture["tournament_id"],
            "Group Stage Complete"
        )

        print("Status Updated:", result)

    return True, "Result saved successfully."


# =====================================================
# Check Group Stage Completion
# =====================================================

def is_group_stage_complete(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS pending
        FROM fixtures
        WHERE tournament_id = %s
        AND stage = 'Group'
        AND match_status = 'Pending'
    """, (tournament_id,))

    pending = cursor.fetchone()["pending"]

    conn.close()

    return pending == 0


# =====================================================
# Get Top Scorers
# =====================================================

def get_top_scorers(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            t.team_name,
            COALESCE(SUM(goals), 0) AS goals
        FROM (

            SELECT
                home_team AS team_id,
                home_score AS goals
            FROM fixtures
            WHERE tournament_id = %s
            AND home_score IS NOT NULL

            UNION ALL

            SELECT
                away_team AS team_id,
                away_score AS goals
            FROM fixtures
            WHERE tournament_id = %s
            AND away_score IS NOT NULL

        ) scores

        JOIN teams t
            ON scores.team_id = t.id

        GROUP BY t.team_name

        ORDER BY goals DESC, t.team_name ASC

    """, (tournament_id, tournament_id))

    scorers = cursor.fetchall()

    conn.close()

    return scorers