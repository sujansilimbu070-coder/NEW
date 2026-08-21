import os
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# ==========================================
# PostgreSQL Configuration
# ==========================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://football_worldcup_user:IK36FZdxNuetmuxyauU1TzGasHGuSTN2@dpg-d9n3uce1egvs73fbhre0-a.oregon-postgres.render.com/football_worldcup"
)


# ==========================================
# PostgreSQL Connection
# ==========================================

import time

def get_connection():

    start = time.perf_counter()

    conn = psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor,
        sslmode="require"
    )

    elapsed = time.perf_counter() - start

    print(f"🔗 Connection: {elapsed:.3f} sec")

    return conn

# ==========================================
# Create Database Tables
# ==========================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================================
    # Tournament Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tournaments (

        id SERIAL PRIMARY KEY,

        tournament_name TEXT NOT NULL,

        tournament_type TEXT NOT NULL,

        total_teams INTEGER NOT NULL,

        teams_per_group INTEGER,

        total_groups INTEGER,

        qualify_per_group INTEGER,

        best_third_count INTEGER,

        knockout_bracket TEXT,

        status TEXT DEFAULT 'Not Started',

        is_active INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );
    """)


    # ==========================================
    # Teams Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teams (

        id SERIAL PRIMARY KEY,

        tournament_id INTEGER NOT NULL,

        team_name TEXT NOT NULL,

        short_name TEXT,

        seed INTEGER,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        UNIQUE (tournament_id, team_name),

        FOREIGN KEY (tournament_id)
            REFERENCES tournaments(id)
            ON DELETE CASCADE

    );
    """)

    # ==========================================
    # Groups Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (

        id SERIAL PRIMARY KEY,

        tournament_id INTEGER NOT NULL,

        group_name TEXT NOT NULL,

        team_id INTEGER NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (tournament_id)
            REFERENCES tournaments(id)
            ON DELETE CASCADE,

        FOREIGN KEY (team_id)
            REFERENCES teams(id)
            ON DELETE CASCADE

    );
    """)

    # ==========================================
    # Fixtures Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fixtures (

        id SERIAL PRIMARY KEY,

        tournament_id INTEGER NOT NULL,

        stage TEXT NOT NULL,

        round_no INTEGER,

        group_name TEXT,

        match_no INTEGER,

        home_team INTEGER,

        away_team INTEGER,

        home_slot TEXT,

        away_slot TEXT,

        home_score INTEGER DEFAULT NULL,

        away_score INTEGER DEFAULT NULL,

        penalty_home INTEGER DEFAULT NULL,

        penalty_away INTEGER DEFAULT NULL,

        winner INTEGER,

        next_match INTEGER,

        match_status TEXT DEFAULT 'Pending',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (tournament_id)
            REFERENCES tournaments(id)
            ON DELETE CASCADE,

        FOREIGN KEY (home_team)
            REFERENCES teams(id)
            ON DELETE CASCADE,

        FOREIGN KEY (away_team)
            REFERENCES teams(id)
            ON DELETE CASCADE,

        FOREIGN KEY (next_match)
            REFERENCES fixtures(id)

    );
    """)


        # ==========================================
    # Standings Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS standings (

        id SERIAL PRIMARY KEY,

        tournament_id INTEGER,

        group_name TEXT,

        team_id INTEGER,

        played INTEGER DEFAULT 0,

        win INTEGER DEFAULT 0,

        draw INTEGER DEFAULT 0,

        loss INTEGER DEFAULT 0,

        goals_for INTEGER DEFAULT 0,

        goals_against INTEGER DEFAULT 0,

        goal_difference INTEGER DEFAULT 0,

        points INTEGER DEFAULT 0,

        rank_position INTEGER,

        qualification_status TEXT,

        FOREIGN KEY (tournament_id)
            REFERENCES tournaments(id)
            ON DELETE CASCADE,

        FOREIGN KEY (team_id)
            REFERENCES teams(id)
            ON DELETE CASCADE

    );
    """)

    # ==========================================
    # Knockout Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knockout (

        id SERIAL PRIMARY KEY,

        tournament_id INTEGER,

        stage TEXT,

        match_no INTEGER,

        home_team INTEGER,

        away_team INTEGER,

        winner INTEGER,

        FOREIGN KEY (tournament_id)
            REFERENCES tournaments(id)
            ON DELETE CASCADE

    );
    """)

    # ==========================================
    # Settings Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (

        id SERIAL PRIMARY KEY,

        theme TEXT DEFAULT 'Light',

        language TEXT DEFAULT 'English'

    );
    """)

    # ==========================================
    # Admin Table
    # ==========================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (

        id SERIAL PRIMARY KEY,

        username TEXT UNIQUE,

        password TEXT

    );
    """)

    # ==========================================
    # Save Changes
    # ==========================================
    conn.commit()
    conn.close()

    print("✅ PostgreSQL Database Created Successfully!")
    print("✅ All Tables Ready!")
# ==========================================
# Main
# ==========================================

if __name__ == "__main__":
    create_tables()