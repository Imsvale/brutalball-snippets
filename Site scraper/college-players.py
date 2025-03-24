import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def fetch_player_stats(team_id):
    try:
        url = f"https://dozerverse.com/brutalball/ebaa-team.php?i={team_id}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful.
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    # print(response.content, file=open("content.html", "w+"))

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html5lib")

    # Find the specific table
    table = soup.find_all("table", {"class": "teamroster"})

    # Read the table into a DataFrame using pandas
    df = pd.read_html(StringIO(str(table)))[0]

    # Clean up the DataFrame if necessary
    # Clean up any unwanted rows or columns
    # (There shouldn't be any empty rows or columns, so this isn't really necessary.)
    df = df.dropna(how="all")  # Drop rows with all NaN values

    # Adding team name into the player data
    college_team = df.at[0, 0]  # Get the line that contains the team name (college team is easy!)
    df.insert(2, "Team", college_team)  # Insert column before player stats with team name for each player

    return df


def run_scrape():
    num_teams = 24
    file_name = "college_player_stats_raw.csv"
    with open(file_name, "w+"):
        pass

    for team_id in range(num_teams):

        stats_df = fetch_player_stats(team_id)[3:-1]

        if stats_df is not None:
            # Save the DataFrame to a CSV file.
            stats_df.to_csv(file_name, header=False, index=False, mode="a")

        else:
            print(f"Failed to extract the table for team {team_id}.")

    print(f"\nData saved to '{file_name}'.")


def parse():
    import re

    file_in = "college_player_stats_raw.csv"
    file_out = "college_player_stats_parsed.csv"

    with open(file_in) as f:
        content = f.read()

    content = content.strip()
    # Remove [CAPTAIN], [bounty], and [unavailable] tags
    content = re.sub(".?\\[(.*?)]\\s*", "", content)

    # Split race, player number, and name
    # Remaining values are already comma-separated
    # COLLEGE PLAYERS DON'T HAVE NUMBERS

    # Comma between name and race is a bit tricky.
    # Though names have great variety, races do not
    # There is only one three-word race: Old One Illithid
    # The rest are two-word, so from the start of the line,
    # any two words followed by a comma, put a comma in front of that
    content = re.sub("\\s((([A-Za-z]+\\s?){2}|Old One Illithid),)([a-z]+,)", ",\\1\\4", content)

    # regex everything until first comma: (^[^,]+,)

    with open(file_out, "w") as f:
        f.write(content)


if __name__ == "__main__":
    run_scrape()
    parse()
