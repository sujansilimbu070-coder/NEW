import sqlite3
from database import get_connection


# ==========================================
# Add Team
# ==========================================

def add_team(
    tournament_id,
    team_name,
    short_name,
    seed
):
    """
    Add a new team to a tournament.
    Returns:
        True  -> Team added successfully
        False -> Team already exists or another database error occurred
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO teams (
                tournament_id,
                team_name,
                short_name,
                seed
            )
            VALUES (?, ?, ?, ?)
        """, (
            tournament_id,
            team_name,
            short_name,
            seed
        ))

        conn.commit()
        conn.close()

        return True

    except sqlite3.IntegrityError:
        conn.close()
        return False

    except sqlite3.Error as error:
        print(f"Database Error: {error}")
        conn.close()
        return False


# ==========================================
# Get Teams
# ==========================================

def get_teams_by_tournament(tournament_id):
    """
    Return all teams for a tournament.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM teams
        WHERE tournament_id = ?
        ORDER BY seed ASC, id ASC
    """, (tournament_id,))

    teams = cursor.fetchall()

    conn.close()

    return teams

# ==========================================
# Update Team
# ==========================================

def update_team(team_id, team_name, short_name, seed):
    """
    Update an existing team.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE teams
            SET
                team_name = ?,
                short_name = ?,
                seed = ?
            WHERE id = ?
        """, (
            team_name,
            short_name,
            seed,
            team_id
        ))

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error as error:
        print(f"Database Error: {error}")
        conn.close()
        return False
    
# ==========================================
# Delete Team
# ==========================================

def delete_team(team_id):
    """
    Delete a team.
    """

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM teams
            WHERE id = ?
        """, (team_id,))

        conn.commit()
        conn.close()

        return True

    except sqlite3.Error as error:
        print(f"Database Error: {error}")
        conn.close()
        return False