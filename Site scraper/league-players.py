import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO


def fetch_player_stats(team_id):
    try:
        url = f"https://dozerverse.com/brutalball/team.php?i={team_id}"
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

    # Remove colspan and rowspan attributes
    for t in table:
        for td in t.find_all("td"):
            td.attrs = {key: value for key, value in td.attrs.items() if key not in ['colspan', 'rowspan']}

    # Read the table into a DataFrame using pandas
    df = pd.read_html(StringIO(str(table)))[0]

    # Clean up the DataFrame if necessary
    # Clean up any unwanted rows or columns
    # (There shouldn't be any empty rows or columns, so this isn't really necessary.)
    df = df.dropna(how="all")  # Drop rows with all NaN values

    # Adding team name into the player data
    team_line = df.at[0, 0]  # Get the line that contains the team name
    team = team_line.split("  Team owner")[0]  # Extract team name, discard the rest
    df.insert(1, "Team", team)  # Insert column before player stats with team name for each player

    return df


def run_scrape():
    num_teams = 32
    file_name = "player_stats_raw.csv"
    with open(file_name, "w+"):
        pass

    for team_id in range(num_teams):

        stats_df = fetch_player_stats(team_id)[3:-2]

        if stats_df is not None:
            # Save the DataFrame to a CSV file.
            stats_df.to_csv(file_name, header=False, index=False, mode="a")

        else:
            print(f"Failed to extract the table for team {team_id}.")

    print(f"\nRaw data saved to '{file_name}'.")


def parse():
    import re

    file_in = "player_stats_raw.csv"
    file_out = "player_stats_parsed.csv"

    with open(file_in) as f:
        content = f.read()

    content = content.strip()
    # Remove [CAPTAIN], [bounty], and [unavailable] tags
    content = re.sub(".?\\[(.*?)]\\s*", "", content)

    # Split race, player number, and name
    # Remaining values are already comma-separated
    content = re.sub("\\s(#[0-9]+)\\s((\\s?[A-Za-z]+\\s?){2,3}),", ",\\1,\\2,", content)

    with open(file_out, "w") as f:
        f.write(content)
    print(f"\nParsed data saved to '{file_out}'.")


if __name__ == "__main__":
    run_scrape()
    parse()
