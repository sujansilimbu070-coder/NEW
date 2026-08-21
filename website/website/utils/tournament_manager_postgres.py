import traceback
import streamlit as st
from database_postgres import get_connection


# ==========================================
# Tournament Status Constants
# ==========================================

STATUS_NOT_STARTED = "Not Started"
STATUS_TEAMS_ADDED = "Teams Added"
STATUS_GROUPS_DRAWN = "Groups Drawn"
STATUS_FIXTURES_GENERATED = "Fixtures Generated"
STATUS_GROUP_STAGE_COMPLETE = "Group Stage Complete"
STATUS_KNOCKOUT_GENERATED = "Knockout Generated"
STATUS_COMPLETED = "Completed"


# ==========================================
# Create Tournament
# ==========================================

def create_tournament(
    tournament_name,
    tournament_type,
    total_teams,
    teams_per_group,
    total_groups,
    qualify_per_group,
    best_third_count,
):
    """
    Create a new tournament.
    """

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO tournaments (
                    tournament_name,
                    tournament_type,
                    total_teams,
                    teams_per_group,
                    total_groups,
                    qualify_per_group,
                    best_third_count
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    tournament_name,
                    tournament_type,
                    total_teams,
                    teams_per_group,
                    total_groups,
                    qualify_per_group,
                    best_third_count,
                ),
            )

            new_id = cursor.fetchone()["id"]

            conn.commit()

            return new_id

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        print("====================================")
        print("DATABASE ERROR")
        print(error)
        print("====================================")

        return None
# ==========================================
# Get All Tournaments
# ==========================================

def get_all_tournaments():

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM tournaments
                ORDER BY id DESC
            """)

            return cursor.fetchall()

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        return []


# ==========================================
# Get Tournament By ID
# ==========================================

def get_tournament_by_id(tournament_id):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM tournaments
                WHERE id = %s
                """,
                (tournament_id,),
            )

            return cursor.fetchone()

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        return None


# ==========================================
# Get Tournament Status
# ==========================================

def get_tournament_status(tournament_id):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT status
                FROM tournaments
                WHERE id = %s
                """,
                (tournament_id,),
            )

            row = cursor.fetchone()

            if row:
                return row["status"]

            return None

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        return None




# ==========================================
# Delete Tournament
# ==========================================

def delete_tournament(tournament_id):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM tournaments
                WHERE id = %s
                """,
                (tournament_id,),
            )

            conn.commit()

            return cursor.rowcount > 0

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        return False
    

# ==========================================
# Set Active Tournament
# ==========================================

def set_active_tournament(tournament_id):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Remove active status from all tournaments
            cursor.execute("""
                UPDATE tournaments
                SET is_active = 0
            """)

            # Set selected tournament as active
            cursor.execute("""
                UPDATE tournaments
                SET is_active = 1
                WHERE id = %s
            """, (tournament_id,))

            conn.commit()

            return True

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        return False
    

# ==========================================
# Get Active Tournament
# ==========================================

def get_active_tournament():

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM tournaments
                WHERE is_active = 1
                LIMIT 1
            """)

            return cursor.fetchone()

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        return None
    

# ==========================================
# Update Tournament Status
# ==========================================

def update_tournament_status(tournament_id, status):

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE tournaments
                SET status = %s
                WHERE id = %s
                """,
                (
                    status,
                    tournament_id,
                ),
            )

            conn.commit()

            return cursor.rowcount > 0

    except Exception as error:

        traceback.print_exc()

        st.error(f"Database Error: {error}")

        return False