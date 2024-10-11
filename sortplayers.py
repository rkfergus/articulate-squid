import json
import jsbeautifier

def sort_players_teams(input_file):
    # Load the JSON data from the input file
    with open(input_file, 'r') as file:
        player_data = json.load(file)

    # Sort players by last name (alphabetically)
    sorted_data = {}
    for player, teams in player_data.items():
        # Sort the teams alphabetically
        sorted_teams = sorted(teams)
        sorted_data[player] = sorted_teams

    # Sort the entire data by player names
    sorted_data = dict(sorted(sorted_data.items()))

    return sorted_data

def write_sorted_data_to_file(sorted_data, output_file):
    # Write the sorted data to the output file with custom formatting using pprint
    options = jsbeautifier.default_options()
    options.indent_size = 2

    with open(output_file, 'w') as file:
        data = jsbeautifier.beautify(json.dumps(sorted_data), options)
        file.write(data)


if __name__ == "__main__":
    input_file = 'ex/src/players.json'  # Input file with unsorted player data
    output_file = 'ex/out/sorted_players.json'  # Output file for sorted player data
    
    sorted_data = sort_players_teams(input_file)
    write_sorted_data_to_file(sorted_data, output_file)
