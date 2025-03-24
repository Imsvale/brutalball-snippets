import re

in_file = "injuries.txt"
out_file = "injuries parsed.txt"

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

for team in teams:
    content = re.sub(f"{team} ", f"{team},", content)

with open(out_file, "w+") as f:
    f.write(content)
