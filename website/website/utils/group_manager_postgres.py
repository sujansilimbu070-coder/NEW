import random
from database_postgres import get_connection


# ==========================================
# Create Groups
# ==========================================

def create_groups(tournament_id, total_groups):
    """
    Remove previous group assignments.
    Groups will be created when teams are drawn.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM groups
        WHERE tournament_id = %s
    """, (tournament_id,))

    conn.commit()
    conn.close()

    return True


# ==========================================
# Get Groups
# ==========================================

def get_groups(tournament_id):
    """
    Return all groups of a tournament.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM groups
        WHERE tournament_id = %s
        ORDER BY group_name
    """, (tournament_id,))

    groups = cursor.fetchall()

    conn.close()

    return groups


# ==========================================
# Seed Based Group Draw
# ==========================================

def draw_seeded_groups(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    # --------------------------------------
    # Get Tournament
    # --------------------------------------

    cursor.execute("""
        SELECT total_groups
        FROM tournaments
        WHERE id = %s
    """, (tournament_id,))

    tournament = cursor.fetchone()

    if tournament is None:
        conn.close()
        return False, "Tournament not found."

    total_groups = tournament["total_groups"]

    # --------------------------------------
    # Generate Group Names
    # --------------------------------------

    groups = []

    for i in range(total_groups):
        groups.append(f"Group {chr(65 + i)}")

    # --------------------------------------
    # Get Teams
    # --------------------------------------

    cursor.execute("""
        SELECT id, team_name, seed
        FROM teams
        WHERE tournament_id = %s
        ORDER BY seed, team_name
    """, (tournament_id,))

    teams = cursor.fetchall()

    print("Teams used for draw:")
    for team in teams:
        print(team)

    if len(teams) == 0:
        conn.close()
        return False, "No teams found."

    # --------------------------------------
    # Check Seeds
    # --------------------------------------

    for team in teams:

        if team["seed"] is None:
            conn.close()
            return False, f"{team['team_name']} has no seed."

    # --------------------------------------
    # Divide Teams by Seed
    # --------------------------------------

    seed_dict = {}

    for team in teams:

        seed = team["seed"]

        if seed not in seed_dict:
            seed_dict[seed] = []

        seed_dict[seed].append(team)

    # --------------------------------------
    # Validate Seed Counts
    # --------------------------------------

    for seed in sorted(seed_dict.keys()):

        if len(seed_dict[seed]) != total_groups:

            conn.close()

            return (
                False,
                f"Seed {seed} must contain exactly {total_groups} teams."
            )

    # --------------------------------------
    # Remove Previous Draw
    # --------------------------------------

    cursor.execute("""
        DELETE FROM groups
        WHERE tournament_id = %s
    """, (tournament_id,))

    # --------------------------------------
    # Draw Teams
    # --------------------------------------

    for seed in sorted(seed_dict.keys()):

        teams_list = seed_dict[seed]

        random.shuffle(teams_list)

        for index in range(total_groups):

            cursor.execute("""
                INSERT INTO groups (
                    tournament_id,
                    group_name,
                    team_id
                )
                VALUES (%s, %s, %s)
            """, (
                tournament_id,
                groups[index],
                teams_list[index]["id"]
            ))

    conn.commit()
    conn.close()

    return True, "✅ Group draw completed successfully."


# ==========================================
# Get Teams Inside Groups
# ==========================================

def get_group_teams(tournament_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            g.group_name,
            t.team_name,
            t.seed

        FROM groups g

        LEFT JOIN teams t
        ON g.team_id = t.id

        WHERE g.tournament_id = %s
        AND g.team_id IS NOT NULL

        ORDER BY
            g.group_name,
            t.seed
    """, (tournament_id,))

    rows = cursor.fetchall()

    conn.close()

    result = {}

    for row in rows:

        if row["group_name"] not in result:
            result[row["group_name"]] = []

        result[row["group_name"]].append(row)

    return result