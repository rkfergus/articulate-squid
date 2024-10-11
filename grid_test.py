import unittest
import json
from itertools import combinations

# List of all 30 MLB team abbreviations
TEAM_ABBREVIATIONS = [
    "ARI", "ATL", "BAL", "BOS", "CHC", "CHW", "CIN", "CLE", "COL", "DET", 
    "HOU", "KCR", "LAA", "LAD", "MIA", "MIL", "MIN", "NYM", "NYY", "OAK", 
    "PHI", "PIT", "SDP", "SEA", "SFG", "STL", "TBR", "TEX", "TOR", "WSN"
]

class TestImmaculateGrid(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test environment before each test.

        This method initializes the `filename` attribute with the path to the JSON file
        containing player data. It then loads the JSON file and assigns its content to
        the `players_data` attribute.

        Attributes:
            filename (str): The path to the JSON file containing player data.
            players_data (dict): The dictionary containing player data loaded from the JSON file.
        """
        # This function will be executed before each test
        self.filename = "ex/src/players.json"  # Replace with actual file path if needed

        # Load the JSON file
        with open(self.filename, 'r') as file:
            raw_file = json.load(file)

        # Unwrap the list of dictionaries into a single dictionary
        # self.players_data = {list(entry.keys())[0]: list(entry.values())[0] for entry in raw_file}
        self.players_data = raw_file

    def test_team_names_three_letters(self):
        """
        Test that all team names in the players_data attribute are exactly three letters long.

        This method iterates through the values of the players_data dictionary, which are lists of team names,
        and asserts that each team name has a length of three characters. If a team name does not meet this 
        criterion, an assertion error is raised with a message indicating the specific team name that failed 
        the check.
        """
        # Verify that all team names are three letters
        for teams in self.players_data.values():
            for team in teams:
                self.assertEqual(len(team), 3, f"Team name {team} is not three letters long")

    def test_team_names_in_abbreviations(self):
        """
        Test that all team names in the players_data are present in the TEAM_ABBREVIATIONS list.

        This test iterates through the team names in the players_data and checks if each team name
        is included in the TEAM_ABBREVIATIONS list. If a team name is not found in the list, the test
        will fail and provide an appropriate error message indicating which team name is missing.

        Raises:
            AssertionError: If any team name in players_data is not found in TEAM_ABBREVIATIONS.
        """
        # Verify that all team names are in the TEAM_ABBREVIATIONS list
        for teams in self.players_data.values():
            for team in teams:
                self.assertIn(team, TEAM_ABBREVIATIONS, f"Team name {team} is not in the TEAM_ABBREVIATIONS list")


    def test_players_alphabetical(self):
        """
        Test that the player names are in alphabetical order.

        This method extracts the player names from the `players_data` attribute
        and checks if they are sorted in alphabetical order. If the names are not
        in alphabetical order, the test will fail with an appropriate message.
        """
        # Extract the player names and check if they are in alphabetical order
        player_names = list(self.players_data.keys())
        self.assertEqual(player_names, sorted(player_names), "Players are not in alphabetical order")

    def test_teams_alphabetical(self):
        """
        Test that each player's team list is in alphabetical order.

        This test iterates through the players' data and checks if the list of teams
        for each player is sorted in alphabetical order. If any player's team list
        is not in alphabetical order, the test will fail with an appropriate message.

        Raises:
            AssertionError: If any player's team list is not in alphabetical order.
        """
        # Check that each player's team list is in alphabetical order
        for player, teams in self.players_data.items():
            self.assertEqual(teams, sorted(teams), f"Teams for {player} are not in alphabetical order")

    def test_combinations_satisfied(self):
        """
        Test that all possible team combinations (two-team pairs) are satisfied by the players' data.
        This test performs the following steps:
        1. Generates all possible team combinations from TEAM_ABBREVIATIONS.
        2. Collects the actual team pairs from the players' data.
        3. Identifies any missing combinations that are not satisfied by the players' data.
        4. Creates a dictionary to store missing combinations by team.
        5. Prints the missing combinations dictionary with each team on its own line.
        6. Asserts that there are no missing combinations, and if there are, prints the number of unique combinations missing.
        Raises:
            AssertionError: If there are any missing team combinations.
        """
        # Generate all possible team combinations (two-team pairs)
        all_team_combinations = list(combinations(TEAM_ABBREVIATIONS, 2))

        # Collect the actual team pairs from the players' data
        satisfied_combinations = set()

        for teams in self.players_data.values():
            for combo in combinations(teams, 2):
                satisfied_combinations.add(tuple(sorted(combo)))

        # Find missing combinations
        missing_combinations = [
            combo for combo in all_team_combinations if combo not in satisfied_combinations
        ]

        

        # Create a dictionary to store missing combinations by team
        missing_combinations_dict = {}
        for team1, team2 in missing_combinations:
            if team1 not in missing_combinations_dict:
                missing_combinations_dict[team1] = []
            if team2 not in missing_combinations_dict:
                missing_combinations_dict[team2] = []
            missing_combinations_dict[team1].append(team2)
            missing_combinations_dict[team2].append(team1)

        # Print the missing combinations dictionary with each team on its own line
        print("Missing combinations:")
        for team, missing in missing_combinations_dict.items():
            print(f"{team}: {missing}")
        # Check if there are any missing combinations and print the number of unique combinations missing if the assertion fails
        self.assertEqual(
            len(missing_combinations), 
            0, 
            f"Some team combinations are missing! Number of unique combinations missing: {len(missing_combinations)}"
        )

    def get_team_combinations(self, player_data):
        """
        Generate all possible 2-team combinations from player data.

        Args:
            player_data (dict): A dictionary where keys are player identifiers and values are lists of teams the player is part of.

        Returns:
            set: A set of tuples, each containing a unique combination of two teams.
        """
        teams = set()
        for teams_list in player_data.values():
            teams.update(teams_list)
        return set(combinations(sorted(teams), 2))

    def test_find_redundant_players(self):
        """
        Test method to identify and remove redundant players from the players_data.
        This method iterates through the players in reverse order and temporarily removes each player
        to check if the remaining players can still satisfy the combinations test. If the test passes
        without a player, that player is considered redundant and is removed from the players_data.
        Steps:
        1. Iterate through the players in reverse order.
        2. Temporarily remove each player and run the combinations test.
        3. If the test passes, add the player to the redundant_players list.
        4. Restore the original players_data if the test fails.
        5. Remove all redundant players from the original players_data.
        6. Confirm that the remaining players still satisfy the combinations test.
        7. Optionally, check and print any missing combinations after removing redundant players.
        Raises:
            AssertionError: If any players are found to be redundant after the process.
        """
        redundant_players = []
        non_redundant_players = list(self.players_data.keys())
        original_data = self.players_data


        for player in reversed(non_redundant_players):  # Iterate in reverse order
            # Create a copy of the data without the current player
            temp_data = self.players_data.copy()
            temp_data.pop(player)

            # Temporarily replace the players_data with the modified data
            last_change = self.players_data
            self.players_data = temp_data

            # Try to run the combinations test
            try:
                print(f"Checking player {player}...")
                self.test_combinations_satisfied()  # Call the existing test method
                # If it passes, we can consider this player redundant
                redundant_players.append(player)
            except AssertionError:
                # If it fails, we need to revert to the original data
                self.players_data = last_change  # Restore the original data
                continue

        # Restore the original data
        self.players_data = original_data

        # Remove redundant players from the original players_data
        for player in redundant_players:
            self.players_data.pop(player)

        print("Redundant players:", redundant_players)
        print("Remaining players after removing redundant players:", list(self.players_data.keys()))

        # Run the combinations check again to confirm remaining players cover all combinations
        self.test_combinations_satisfied()  # This should still pass with the remaining players

       
        # Optionally, recheck the missing combinations and print them
        remaining_combinations = self.get_team_combinations(self.players_data)
        all_team_combinations = set(combinations(TEAM_ABBREVIATIONS, 2))

        missing_combinations = all_team_combinations - remaining_combinations
        if missing_combinations:
            print("Missing combinations after removing redundant players:")
            for team1, team2 in sorted(missing_combinations):
                print(f"{team1}: {team2}")
        else:
            print("No missing combinations after removing redundant players.")

        self.assertEqual(len(redundant_players), 0, "Some players are redundant")


if __name__ == '__main__':
    unittest.main()