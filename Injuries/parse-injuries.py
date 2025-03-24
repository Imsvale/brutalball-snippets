import re

in_file = "injuries.txt"
out_file = "injuries parsed.txt"
current_season = 4

try:
    with open(in_file) as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: Input file \"{in_file}\" not found.")
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
content = re.sub("W([\\d+])", f"{current_season},\\1", content)

# INJURY
content = re.sub(
    # Input: [DUR xx] [Blah] [BRU xx] SR Drops from [SR0] to [SR1] [Bounty]
    " DUR.(\\d+) (.+) BRU (\\d+) SR Drops from (\\d+) to (\\d+) *",
    # Output: SR0,SR1,DUR,Type,Offender Team,Offender,BRU,Bounty
    ",\\4,\\5,\\1,\\2,\\3,", content)

# KILL
content = re.sub(
    # Input: [SR0] DUR xx KILLED by by [Offender Team] [Offender] [BRU xx] [Bounty]
    " SR (\\d+) DUR (\\d+) (.+) BRU (\\d+) *",
    # Output: SR0,SR1,DUR,Type,Offender Team,Offender,BRU,Bounty
    ",\\1,0,\\2,\\3,\\4,", content)

# Isolate teams
for team in teams:
    content = re.sub(f" *({team}) *", f",{team},", content)

# Split at DUR, BRU, and injury type
content = re.sub(" *(INJURED|KILLED|SEASON ENDING INJURY)( by)+", "\\1", content)

# Bounty
#content = re.sub("BOUNTY COLLECTED", "True", content)

headers = "Season,Week,Victim Team,Victim,SR0,SR1,DUR,Type,Offender Team,Offender,BRU,Bounty\n"
with open(out_file, "w+") as f:
    f.write(headers+content)
