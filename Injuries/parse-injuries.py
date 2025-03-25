import re
import argparse
import textwrap

parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent("""\
    Copy from injuries page on Brutalball website.
    https://dozerverse.com/brutalball/injury.php
    Paste into injuries.txt and run parser."""))

parser.add_argument("-f", "--file", help="Path to input file")
parser.add_argument("-o", "--out_file", help="Path to output file")
parser.add_argument("-s", "--season", help="Season number to use", type=int)

args = parser.parse_args()

if args.file:
    print(f"Taking input from {args.file}")

in_file = args.file if args.file else "injuries.txt"
out_file = args.out_file if args.out_file else "injuries parsed.txt"
season = args.season if args.season else 4

try:
    with open(in_file) as f:
        content = f.read()
except FileNotFoundError:
    parser.print_help()
    exit()

content = content.strip()

teams = [
    "Urrgmelonflex",
    "Volcamoose Saints",
    "Blood Pit Bouncers",
    "Bulldozer Power",
    "Failurewood Hills",
    "Vuvu Boys",
    "Grunt Auto Gruppe",
    "Sunshine Funbus",
    "Port Miggins Pirates",
    "Sweaty Marsupials",
    "Kernal Space Agency",
    "Picks Creek Miners",
    "Sportsball Union",
    "Peninsula Transport",
    "Red Star Pathfinders",
    "Fire Chefs",
    "Ov City Axemen",
    "Eduslum Marching Band",
    "Budget Roadies",
    "Nomads",
    "Grazer Ridge",
    "Bongolia Sea Raiders",
    "Bumson Medics",
    "Cheerio Inc",
    "Steggonauts",
    "Shady Palms",
    "Toymasters",
    "Stardozer HR",
    "Wizard Hole Wizards",
    "Beekeepers",
    "Wretched Minstrels",
    "LingoBlend Allstars",
]

# Week number
content = re.sub("W([\\d+])", f"{season},\\1", content)

# INJURY
content = re.sub(
    # Input: [DUR xx] [Blah] [BRU xx] SR Drops from [SR0] to [SR1] [Bounty]
    " DUR.(\\d+) (.+) BRU (\\d+) SR Drops from (\\d+) to (\\d+) *",
    # Output: SR0,SR1,DUR,Blah,Bounty
    ",\\4,\\5,\\1,\\2,\\3,", content)

# KILL
content = re.sub(
    # Input: [SR] DUR xx [Blah] [BRU xx] [Bounty]
    " SR (\\d+) DUR (\\d+) (.+) BRU (\\d+) *",
    # Output: SR,,DUR,Blah,BRU,Bounty
    ",\\1,,\\2,\\3,\\4,", content)

# Isolate teams
for team in teams:
    content = re.sub(f" *({team}) *", f",{team},", content)

# Split at injury type
content = re.sub(" *(INJURED|KILLED|SEASON ENDING INJURY)( by)+", "\\1", content)

headers = "Season,Week,Victim Team,Victim,SR0,SR1,DUR,Type,Offender Team,Offender,BRU,Bounty\n"
with open(out_file, "w+") as f:
    f.write(headers)
with open(out_file, "a") as f:
    f.write(content)
