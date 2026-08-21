from utils.standings_manager_postgres import get_group_standings


def get_qualified_teams(
    tournament_id,
    top_qualifiers=2,
    best_third=0
):
    """
    Returns qualified teams.

    top_qualifiers = number of automatic qualifiers from each group.
    best_third = number of best 3rd-placed teams to qualify.
    """

    standings = get_group_standings(tournament_id)

    qualified = []
    third_place = []

    for group_name, table in standings.items():

        # Automatic qualifiers
        for team in table:
            if team["Pos"] <= top_qualifiers:

                qualified.append({
                    "Group": group_name,
                    **team
                })

        # Collect third-place teams
        if best_third > 0:

            for team in table:
                if team["Pos"] == 3:

                    third_place.append({
                        "Group": group_name,
                        **team
                    })

    # Rank third-place teams
    if best_third > 0:

        third_place.sort(
            key=lambda x: (
                x["Pts"],
                x["GD"],
                x["GF"]
            ),
            reverse=True
        )

        qualified.extend(third_place[:best_third])

    return qualified