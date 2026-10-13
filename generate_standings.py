import requests
import csv
import re

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from io import BytesIO

# -- Classes --------------------------------------------------------------------------------------
class Pokemon:
    name: str
    image: str
    item: str
    ability: str
    stat_alignment: str
    moves: list[str]

    def __init__(self, name):
        self.name = name
        self.image = ""
        self.item = ""
        self.ability = ""
        self.stat_alignment = ""
        self.moves = []

    def print_pokemon(self):
        print(f"{self.name} @ {self.item}\nAbility: {self.ability}\nStat Alignment: {self.stat_alignment}\nMoves: [{", ".join(self.moves)}]")


class Trainer:
    name: str
    local: str
    handle: str
    pokemon: list[Pokemon]

    def __init__(self, name, local, handle=""):
        self.name = name
        self.handle = handle
        self.local = local
        self.pokemon = []

    def print_trainer(self):
        trainer_name = self.name
        if self.handle:
            trainer_name += f" {self.handle}"
        print(f"Trainer: {trainer_name}\nLocal: {self.local}\nPokemon:")
        for pokemon in self.pokemon:
            pokemon.print_pokemon()

class Theme:
    header: str
    background: str
    local_icon: str
    color_1: str
    color_2: str

    def __init__(self, header, background, local_icon, color_1, color_2):
        self.header = f"{ASSET_PATH}{header}"
        self.background = f"{ASSET_PATH}{background}"
        self.local_icon = f"{ASSET_PATH}{local_icon}"
        self.color_1 = color_1
        self.color_2 = color_2

class Local:
    challenge: bool
    cup: bool
    date: str
    location: str
    regulation: str
    player_count: int

    def __init__(self, challenge, cup, location, date, regulation, player_count):
        self.challenge = challenge
        self.cup = cup
        self.location = location
        self.date = date
        self.regulation = regulation
        self.player_count = player_count

    def print_standings_location(self):
        if self.challenge and not self.cup:
            event_type = "CHALLENGE"
        elif self.cup and not self.challenge:
            event_type = "CUP"
        else:
            event_type = "LOCAL"
        return f"VG LEAGUE {event_type} • {self.location.upper()}"

    def print_standings_info(self):
        return f"{self.date} • Regulation {self.regulation} • {self.player_count} Players"


# -- Globals --------------------------------------------------------------------------------------

POKEAPI_URL = "https://pokeapi.co/api/v2"
CWD = str(Path.cwd())
ASSET_PATH = f"{CWD}\\assets\\"
VGC_ICON_PATH = f"{ASSET_PATH}Pokemon VGC Icon.png"
NON_MEGA_STONE_ITE_ITEMS = ["White Herb", "Eviolite"]
SPECIAL_POKEMON_URL_ADJUSTMENTS = {
    "Pikachu-Original": "pikachu-original-cap",
    "Pikachu-Partner": "pikachu-partner-cap",
    "Pikachu-World": "pikachu-world-cap",
    "Pikachu-Hoenn": "pikachu-hoenn-cap",
    "Pikachu-Sinnoh": "pikachu-sinnoh-cap",
    "Pikachu-Unova": "pikachu-unova-cap",
    "Pikachu-Kalos": "pikachu-kalos-cap",
    "Pikachu-Alola": "pikachu-alola-cap",
    "Tauros-Paldea-Combat": "tauros-paldea-combat-breed",
    "Tauros-Paldea-Blaze": "tauros-paldea-blaze-breed",
    "Tauros-Paldea-Aqua": "tauros-paldea-aqua-breed",
    "Deoxys": "deoxys-normal",
    "Wormadam": "wormadam-plant",
    "Cherrim-Sunshine": "cherrim",
    "Shellos-East": "shellos",
    "Gastrodon-East": "gastrodon",
    "Giratina": "giratina-altered",
    "Shaymin": "shaymin-land",
    "Arceus-Fighting": "arceus",
    "Arceus-Flying": "arceus",
    "Arceus-Poisona": "arceus",
    "Arceus-Ground": "arceus",
    "Arceus-Rock": "arceus",
    "Arceus-Bug": "arceus",
    "Arceus-Ghost": "arceus",
    "Arceus-Steel": "arceus",
    "Arceus-Fire": "arceus",
    "Arceus-Water": "arceus",
    "Arceus-Grass": "arceus",
    "Arceus-Electric": "arceus",
    "Arceus-Psychic": "arceus",
    "Arceus-Ice": "arceus",
    "Arceus-Dragon": "arceus",
    "Arceus-Dark": "arceus",
    "Arceus-Fairy": "arceus",
    "Darmanitan": "darmanitan-standard",
    "Darmanitan-Galar": "darmanitan-galar-standard",
    "Deerling-Winter": "deerling",
    "Deerling-Summer": "deerling",
    "Deerling-Autumn": "deerling",
    "Sawsbuck-Winter": "sawsbuck",
    "Sawsbuck-Summer": "sawsbuck",
    "Sawsbuck-Autumn": "sawsbuck",
    "Tornadus": "tornadus-incarnate",
    "Thundurus": "thundurus-incarnate",
    "Landorus": "landorus-incarnate",
    "Keldeo": "keldeo-ordinary",
    "Genesect-Douse": "genesect",
    "Genesect-Shock": "genesect",
    "Genesect-Burn": "genesect",
    "Genesect-Chill": "genesect",
    "Vivillon-Icy-Snow": "vivillon",
    "Vivillon-Polar": "vivillon",
    "Vivillon-Tundra": "vivillon",
    "Vivillon-Continental": "vivillon",
    "Vivillon-Garden": "vivillon",
    "Vivillon-Elegant": "vivillon",
    "Vivillon-Modern": "vivillon",
    "Vivillon-Marine": "vivillon",
    "Vivillon-Archipelago": "vivillon",
    "Vivillon-High Plains": "vivillon",
    "Vivillon-Sandstorm": "vivillon",
    "Vivillon-River": "vivillon",
    "Vivillon-Monsoon": "vivillon",
    "Vivillon-Savanna": "vivillon",
    "Vivillon-Sun": "vivillon",
    "Vivillon-Ocean": "vivillon",
    "Vivillon-Jungle": "vivillon",
    "Vivillon-Fancy": "vivillon",
    "Vivillon-Pokeball": "vivillon",
    "Flabébé": "flabebe",
    "Flabébé-Blue": "flabebe",
    "Flabébé-Orange": "flabebe",
    "Flabébé-White": "flabebe",
    "Flabébé-Yellow": "flabebe",
    "Floette-Blue": "floette",
    "Floette-Orange": "floette",
    "Floette-White": "floette",
    "Floette-Yellow": "floette",
    "Florges-Blue": "florges",
    "Florges-Orange": "florges",
    "Florges-White": "florges",
    "Florges-Yellow": "florges",
    "Furfrou-Heart": "furfrou",
    "Furfrou-Star": "furfrou",
    "Furfrou-Diamond": "furfrou",
    "Furfrou-Debutanta": "furfrou",
    "Furfrou-Matron": "furfrou",
    "Furfrou-Dandy": "furfrou",
    "Furfrou-La Reine": "furfrou",
    "Furfrou-Kabuki": "furfrou",
    "Furfrou-Pharaoh": "furfrou",
    "Meowstic": "meowstic-male",
    "Meowstic-F": "meowstic-female",
    "Pumpkaboo-Large": "pumpkaboo",
    "Pumpkaboo-Small": "pumpkaboo",
    "Pumpkaboo-Super": "pumpkaboo",
    "Gourgeist-Large": "gourgeist",
    "Gourgeist-Small": "gourgeist",
    "Gourgeist-Super": "gourgeist",
    "Xerneas-Neutral": "xerneas",
    "Zygarde-10%": "zygarde",
    "Zygarde-Complete": "zygarde",
    "Oricorio": "oricorio-baile",
    "Oricorio-Pa'u": "oricorio-pau",
    "Lycanroc": "lycanroc-midday",
    "Silvally-Fighting": "silvally",
    "Silvally-Flying": "silvally",
    "Silvally-Poisona": "silvally",
    "Silvally-Ground": "silvally",
    "Silvally-Rock": "silvally",
    "Silvally-Bug": "silvally",
    "Silvally-Ghost": "silvally",
    "Silvally-Steel": "silvally",
    "Silvally-Fire": "silvally",
    "Silvally-Water": "silvally",
    "Silvally-Grass": "silvally",
    "Silvally-Electric": "silvally",
    "Silvally-Psychic": "silvally",
    "Silvally-Ice": "silvally",
    "Silvally-Dragon": "silvally",
    "Silvally-Dark": "silvally",
    "Silvally-Fairy": "silvally",
    "Minior-Orange": "minior",
    "Minior-Yellow": "minior",
    "Minior-Green": "minior",
    "Minior-Blue": "minior",
    "Minior-Indigo": "minior",
    "Minior-Violet": "minior",
    "Necrozma-Dawn-Wings": "necrozma-dawn",
    "Necrozma-Dusk-Mane": "necrozma-dusk",
    "Toxtricity": "toxtricity-amped",
    "Toxtricity-Low-Key": "toxtricity-low-key",
    "Sinistea-Antique": "sinistea",
    "Polteageist-Antique": "polteageist",
    "Alcremie-Ruby-Cream": "alcremie",
    "Alcremie-Matcha-Cream": "alcremie",
    "Alcremie-Mint-Cream": "alcremie",
    "Alcremie-Lemon-Cream": "alcremie",
    "Alcremie-Salted-Cream": "alcremie",
    "Alcremie-Ruby-Swirl": "alcremie",
    "Alcremie-Caramel-Swirl": "alcremie",
    "Alcremie-Rainbow-Swirl": "alcremie",
    "Eiscue": "eiscue-ice",
    "Indeedee": "indeedee-male",
    "Indeedee-F": "indeedee-female",
    "Morpeko": "morpeko-full-belly",
    "Urshifu": "urshifu-single-strike",
    "Basculegion": "basculegion-male",
    "Basculegion-F": "basculegion-female",
    "Enamorus": "enamorus-incarnate",
    "Oinkologne": "oinkologne-male",
    "Oinkologne-F": "oinkologne-female",
    "Maushold": "maushold-family-of-three",
    "Maushold-Four": "maushold-family-of-four",
    "Squawkabilly": "squawkabilly-green-plumage", 
    "Squawkabilly-Blue": "squawkabilly-blue-plumage", 
    "Squawkabilly-White": "squawkabilly-white-plumage", 
    "Squawkabilly-Yellow": "squawkabilly-yellow-plumage", 
    "Palafin": "palafin-hero",
    "Tatsugiri": "tatsugiri-curly",
    "Dudunsparce": "dudunsparce-two-segment",
    "Great Tusk": "great-tusk",
    "Scream Tail": "scream-tail",
    "Brute Bonnet": "brute-bonnet",
    "Flutter Mane": "flutter-mane",
    "Silther Wing": "slither-wing",
    "Sandy Shocks": "sandy-shocks",
    "Roaring Moon": "roaring-moon",
    "Walking Wake": "walking-wake",
    "Gouging Fire": "gouging-fire",
    "Raging Bolt": "raging-bolt",
    "Iron Treads": "iron-treads",
    "Iron Bundle": "iron-bundle",
    "Iron Hands": "iron-hands",
    "Iron Jugulis": "iron-jugulis",
    "Iron Moth": "iron-moth",
    "Iron Thorns": "iron-thorns",
    "Iron Valiant": "iron-valiant",
    "Iron Leaves": "iron-leaves",
    "Iron Boulder": "iron-boulder",
    "Iron Crown": "iron-crown",
    "Poltchageist-Artisan": "poltchageist",
    "Sinistcha-Masterpiece": "sinistcha",
    "Ogerpon-Wellspring": "ogerpon-wellspring-mask",
    "Ogerpon-Hearthflame": "ogerpon-hearthflame-mask",
    "Ogerpon-Cornerstone": "ogerpon-cornerstone-mask",
    "Terapagos": "terapagos-terastal",
}

THEMES = {
    "Portland - Dark": 
    Theme(
        header="Portland VGC Header.jpg",
        background="Background DB.png", 
        local_icon="Portland VGC Icon.png",
        color_1="#278EF5", 
        color_2="#060344",
    ),
    "Portland - Light": 
    Theme(
        header="Portland VGC Header.jpg",
        background="Background B.png", 
        local_icon="Portland VGC Icon.png",
        color_1="#0B51F4",
        color_2="#8FFAF8",
    ),
    "Portland - Black and White": 
    Theme(
        header="Portland VGC Header.jpg",
        background="Background BW.png", 
        local_icon="Portland VGC Icon.png",
        color_1="#FFFFFF", 
        color_2="#000000",
    ),
}

SEPERATOR_HEIGHT = 50
BORDER_WIDTH = 10
ICON_SIZE_DIVIDER = 5

RHOMBUS_DRAG_DOWN = 30
RHOMBUS_HEIGHT = 125
RHOMBUS_WIDTH_DIFFERENCE = 100
RHOMBUS_WIDTH_RATIO = 3/4
RHOMBUS_TEXT_SIDE_BORDER = 50
RHOMBUS_TEXT_VERTICAL_BORDER = 5
RHOMBUS_BORDER_WIDTH = 7

STANDINGS_GAP = 50
STANDINGS_MAX_CARD_HEIGHT = 200
STANDINGS_CARD_RADIUS = 20
STANDINGS_CARD_BORDER = 5
STANDINGS_PLACING_BADGE_SIZE = 50
STANDINGS_PLACING_BADGE_BORDER = 15
STANDINGS_PLACING_BADGE_RADIUS = 10
STANDINGS_INFO_DROP = 2

TRAINER_NAME_WITH_HANDLE_SIZE = 28
TRAINER_HANDLE_SIZE = 18
TRAINER_NAME_AND_HANDLE_BORDER = 7
TRAINER_NAME_NO_HANDLE_SIZE = 40
TRAINER_NAME_BORDER = 4
TRAINER_POKEMON_SPRITE_SIZE = 100
TRAINER_POKEMON_SPRITE_BORDER = 7

SIGNATURE_LIFT = 5
SIGNATURE_PLATE_RADIUS = 15
SIGNATURE_PLATE_BORDER = 5
SIGNATURE_PADDING = [20, 10] # [x, y]
SIGNATURE = "Created by JoshBell302 on GitHub"

CARD_COLOR = "#202B40"
TEXT_COLOR = "#FFFFFF"
MUTED_COLOR = "#C3D0E5"
SIGNATURE_BORDER_COLOR = "#D8B45A"
PLACEMENT_COLORS = {
    1: {
        "border": "#D8B45A",
        "badge": "#D8B45A",
        "text": "#172033",
    },
    2: {
        "border": "#AEBCCD",
        "badge": "#C8D3E0",
        "text": "#172033",
    },
    3: {
        "border": "#CD875B",
        "badge": "#CD875B",
        "text": "#172033",
    },
    "default": {
        "border": "#526078",
        "badge": "#526078",
        "text": "#FFFFFF",
    },
}

# -- Trainier & Pokemon Helpers -------------------------------------------------------------------

def build_trainer(name, handle, local, pokepaste):
    trainer = Trainer(
        name=name,
        local=local,
        handle=handle,
    )
    print(f"Creating Trainer '{trainer.name}'...")
    trainer.pokemon = deconstruct_pokepaste(pokepaste=pokepaste)
    return trainer

def deconstruct_pokepaste(pokepaste):
    # Pull the Pokepastes raw data
    response = get_online_request(f"{pokepaste.rstrip("/") + "/raw"}")

    # Seperate the paste to be deciphered in the Pokemon class creation
    pokemon_team = (response.text).strip().split("\n\n")

    # Go through each Pokemon and decipher the information into a Class
    team = []
    for block in pokemon_team[0].split("\r\n\r\n"):
        lines = block.splitlines()

        # Get the first line from a Pokemon
        first_line = lines[0]

        # If there is an item with the Pokemon add the name and item
        if "@" in first_line:
            name, item = first_line.split("@", 1)
            name = name.strip()
            item = item.strip()
        else:
            name = first_line.strip()
            item = "None"

        # Adjust the name if needed for PokeAPI Image request
        name = re.sub(r"\s+\([FM]\)$", "", name)
        if name in SPECIAL_POKEMON_URL_ADJUSTMENTS.keys():
            print(f"Special name found! Adjusting '{name}' to '{SPECIAL_POKEMON_URL_ADJUSTMENTS[name]}'")
            name = SPECIAL_POKEMON_URL_ADJUSTMENTS[name]

        # Begin creating the Pokemon class
        pokemon = Pokemon(name)
        pokemon.image = get_pokemon_image(name, item)
        pokemon.item = item

        # Decipher the rest of the lines in the Pokemon 
        for line in lines[1:]:
            line = line.strip()
            if line.startswith("Ability:"):
                pokemon.ability = line.split(":", 1)[1].strip()
            elif "Nature" in line:
                pokemon.stat_alignment = line.split(' ', 1)[0].strip()
            elif line.startswith("-"):
                move = line[1:].strip()
                pokemon.moves.append(move)

        team.append(pokemon)
    return team

"""
This function is to pull the image used for the standings from PokeAPI.
The sprite pulled will by default will be the official front_default artwork.
"""
def get_pokemon_image(name, item, sprite_origin="official-artwork", shiny=False):
    # TODO: ADD MEGA POKEMON AS IMAGE 
    
    # Pull the Pokemon's data from PokeAPI using their name
    response = get_online_request(f"{POKEAPI_URL}/pokemon/{name.lower()}")

    # Check to see if we want the shiny artwork or not
    if shiny: sprite_name = "front_shiny"
    else: sprite_name = "front_default"

    # Pull the Sprites information and return it
    return (response.json())["sprites"]["other"][sprite_origin][sprite_name]

"""
This helper is to simplify the call and verification of the request in one spot.
"""
def get_online_request(url):
    # Calling the Request
    print(f"Calling a Request to '{url}'")
    response = requests.get(url)
    
    # Verify the Request
    response.raise_for_status()

    # Return the Response
    return response

# -- Drawing Helpers ------------------------------------------------------------------------------

"""
Given two different colors, this function calculates the pixel RBG value needed and loads them on
to the given image at the given location
"""
def draw_horizontal_gradient(image, y, height, color1, color2):
    # Prepare the Image
    width = image.width
    gradient = Image.new("RGB", (width, height))

    # Get access to the pixels of the Image
    pixels = gradient.load()

    # Convert the hexcolors given to the RGB values
    c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))

    # Loop through the pixels from left to right and adjust them depending on the new RBG values
    for x in range(width):
        # Get the ratio of each color
        ratio = x / (width - 1)
        
        # Calculate the color needed for the location based on the ratio from left to right
        color = tuple(
            int(c1[i] + (c2[i] - c1[i]) * ratio)
            for i in range(3)
        )

        # Apply the color
        for yy in range(height):
            pixels[x, yy] = color

    # Once the gradient is made paste it onto the image given
    image.paste(gradient, (0, y))

def draw_title(image: Image, header_height, local: Local):
    # Get the dimensions of the main standings image
    image_width = image.width

    # Set the dimensions and position of the rhombus
    rhombus_width = int(image_width * RHOMBUS_WIDTH_RATIO)

    # Create a transparent overlay the same size as the main image
    title = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(title)

    title_border = (image_width - rhombus_width) / 2
    rhombus_top_y = header_height-(RHOMBUS_HEIGHT * 0.5) + RHOMBUS_DRAG_DOWN
    rhombus_bottom_y = header_height+(RHOMBUS_HEIGHT * 0.5) + RHOMBUS_DRAG_DOWN

    # Define the four corners of the rhombus
    points = [
        (title_border, rhombus_top_y), 
        (image_width-(title_border+RHOMBUS_WIDTH_DIFFERENCE), rhombus_top_y), 
        (image_width-title_border, rhombus_bottom_y), 
        (title_border+RHOMBUS_WIDTH_DIFFERENCE, rhombus_bottom_y)
    ]

    # Draw the rhombus with a white fill and black outline
    draw.polygon(
        points,
        fill="white",
        outline="black",
        width=RHOMBUS_BORDER_WIDTH
    )

    # Gather the starting info for the title
    location_font_size = 50
    location_verification = True

    # Loop to find a size that fits the Rhombus
    while(location_verification):
        # Prepare the textbox to add
        location_font = ImageFont.truetype("arialbd.ttf", location_font_size)
        textbox_location = draw.textbbox((0,0), local.print_standings_location(), font=location_font)

        # Check to see if the location portion will fit confetably in the rhombus
        if ((textbox_location[2] - textbox_location[0]) >= (rhombus_width-(RHOMBUS_WIDTH_DIFFERENCE * 2) - RHOMBUS_TEXT_SIDE_BORDER)):
            print(f"The Location text is too large for the given font scaling down from '{location_font_size}' to '{location_font_size-1}'...")
            location_font_size -= 1
        else:
            location_verification = False

    # Once the size is found fill out the information before drawing
    location_text_width = textbox_location[2] - textbox_location[0]
    location_text_height = textbox_location[3] - textbox_location[1]
    location_text_x = (image.width - location_text_width) // 2
    location_text_y = int(header_height - location_text_height / 2 - textbox_location[1])

    # Draw the Location text in the Rhombus
    draw.text(
        (location_text_x, location_text_y + RHOMBUS_TEXT_VERTICAL_BORDER),
        local.print_standings_location(),
        font=location_font,
        fill="black"
    )

    # Draw a line to seperate the location and info
    draw.line(
        [
            (location_text_x, (location_text_y + (RHOMBUS_HEIGHT * 0.5))),
            (location_text_x + location_text_width, (location_text_y + (RHOMBUS_HEIGHT * 0.5)))
        ],
        fill="black",
        width=3
    )

    # Gather the starting info for the title
    info_font_size = 40
    info_verification = True
    
    # Loop to find a size that fits the Rhombus
    while(info_verification):
        # Prepare the textbox to add
        info_font = ImageFont.truetype("arialbd.ttf", info_font_size)
        textbox_info = draw.textbbox((0,0), local.print_standings_info(), font=info_font)
    
        # Check to see if the info portion will fit confetably in the rhombus
        if ((textbox_info[2] - textbox_info[0]) >= (rhombus_width-(RHOMBUS_WIDTH_DIFFERENCE * 2) - RHOMBUS_TEXT_SIDE_BORDER)):
            print(f"The Info text is too large for the given font scaling down from '{info_font_size}' to '{info_font_size-1}'...")
            info_font_size -= 1
        else:
            info_verification = False
    
    # Once the size is found fill out the information before drawing
    info_text_width = textbox_info[2] - textbox_info[0]
    info_text_height = textbox_info[3] - textbox_info[1]
    info_text_x = (image.width - info_text_width) // 2
    info_text_y = int(header_height + info_text_height / 2 + textbox_info[1])
    
    # Draw the Info text in the Rhombus
    draw.text(
        (info_text_x, info_text_y + (RHOMBUS_TEXT_VERTICAL_BORDER * 2) + STANDINGS_INFO_DROP),
        local.print_standings_info(),
        font=info_font,
        fill="black"
    )

    # Paste the rhombus overlay onto the main image
    image.paste(title, (0, 0), title)

def draw_theme(theme: Theme):
    # Create the main image 
    header = Image.open(theme.header).convert("RGBA") 
    header_width = int(header.width)
    header_height = int(header.height)
    print(f"Making the standings image ({header_width}x{header_width})")
    image = Image.new("RGB", (header_width, header_width), "#111827")

    # Create the Icon size
    icon_width = int(header_width / ICON_SIZE_DIVIDER)
    icon_height = int(header_width / ICON_SIZE_DIVIDER)

    # Create the Header with Icons then add it to the standings image
    local_icon = Image.open(theme.local_icon).convert("RGBA")
    local_icon = local_icon.resize((icon_width, icon_height), Image.Resampling.LANCZOS)
    vgc_icon = Image.open(VGC_ICON_PATH).convert("RGBA")
    vgc_icon = vgc_icon.resize((icon_width, icon_height), Image.Resampling.LANCZOS)
    image.paste(header, (0,0), header)
    image.paste(local_icon, ((header_width-icon_width-BORDER_WIDTH),0), local_icon)
    image.paste(vgc_icon, (BORDER_WIDTH,0), vgc_icon)
    
    # Now create the Bottom portions background
    background = Image.open(theme.background).convert("RGBA")
    background_aspect_ratio = background.height / background.width
    background = background.resize((header_width, int(header_width * background_aspect_ratio)), Image.Resampling.LANCZOS)
    image.paste(background, (0, header_height), background)
    
    # Add a border inbetween the header and background
    draw_horizontal_gradient(
        image=image,
        y=header_height,
        height=SEPERATOR_HEIGHT,
        color1=theme.color_1,
        color2=theme.color_2
    )

    return image, header_height

def draw_trainer_card(image, trainer, placing, bounds):
    # Get the card's coordinates
    left, top, right, bottom = bounds
    card_width = right - left
    card_height = bottom - top
    placing_colors = PLACEMENT_COLORS.get(int(placing), PLACEMENT_COLORS["default"])
    
    # Create the draw object 
    draw = ImageDraw.Draw(image)

    # Draw the card background
    draw.rounded_rectangle(
        bounds,
        radius=STANDINGS_CARD_RADIUS,
        fill=CARD_COLOR,
        outline=placing_colors.get("border"),
        width=STANDINGS_CARD_BORDER
    )

    # Draw the placing badge
    badge_x = left + STANDINGS_PLACING_BADGE_BORDER
    badge_y = top + STANDINGS_PLACING_BADGE_BORDER
    draw.rounded_rectangle(
        (
            badge_x,
            badge_y,
            badge_x + STANDINGS_PLACING_BADGE_SIZE,
            badge_y + STANDINGS_PLACING_BADGE_SIZE
        ),
        radius=STANDINGS_PLACING_BADGE_RADIUS,
        fill=placing_colors.get("badge")
    )

    # Center the placing number
    placing_text = str(placing)
    placing_font = ImageFont.truetype("arialbd.ttf", 30)
    textbox_placing = draw.textbbox((0, 0), placing_text, font=placing_font)
    placing_width = textbox_placing[2] - textbox_placing[0]
    placing_height = textbox_placing[3] - textbox_placing[1]

    draw.text(
        (
            badge_x + (STANDINGS_PLACING_BADGE_SIZE - placing_width) / 2,
            badge_y + (STANDINGS_PLACING_BADGE_SIZE - placing_height) / 2 - textbox_placing[1]
        ),
        placing_text,
        font=placing_font,
        fill=placing_colors.get("text")
    )

    # Draw the trainers name and handle otherwise just fill the space with the name
    text_x = badge_x + STANDINGS_PLACING_BADGE_SIZE + STANDINGS_PLACING_BADGE_BORDER
    text_y = top + STANDINGS_PLACING_BADGE_BORDER
    if trainer.handle:
        name_font = ImageFont.truetype("arialbd.ttf", TRAINER_NAME_WITH_HANDLE_SIZE)
        handle_font = ImageFont.truetype("arial.ttf", TRAINER_HANDLE_SIZE)
        draw.text(
            (text_x, text_y),
            trainer.name,
            font=name_font,
            fill=TEXT_COLOR
        )
        draw.text(
            (text_x, text_y + TRAINER_NAME_WITH_HANDLE_SIZE + TRAINER_NAME_AND_HANDLE_BORDER),
            trainer.handle,
            font=handle_font,
            fill=MUTED_COLOR
        )
    else:
        name_font = ImageFont.truetype("arialbd.ttf", TRAINER_NAME_NO_HANDLE_SIZE)
        draw.text(
            (text_x, text_y + TRAINER_NAME_BORDER),
            trainer.name,
            font=name_font,
            fill=TEXT_COLOR
        )


    # Draw a divider below the trainer information
    top_slot_height = STANDINGS_PLACING_BADGE_SIZE + (STANDINGS_PLACING_BADGE_BORDER * 2)
    divider_y = top + top_slot_height
    draw.line(
        (left + STANDINGS_PLACING_BADGE_BORDER, divider_y, right - STANDINGS_PLACING_BADGE_BORDER, divider_y),
        fill=MUTED_COLOR,
        width=2
    )

    # Calculate the space available for each Pokemon
    slot_width = card_width / len(trainer.pokemon)
    sprite_y = divider_y + TRAINER_POKEMON_SPRITE_BORDER
    sprite_size = card_height - top_slot_height - (2 * TRAINER_POKEMON_SPRITE_BORDER)

    # Draw each Pokemon sprite
    for i, pokemon in enumerate(trainer.pokemon):
        center_x = left + slot_width * (i + 0.5)

        # Download and open the Pokemon artwork
        if pokemon.image:
            try:
                response = get_online_request(pokemon.image)
                with Image.open(BytesIO(response.content)) as source:
                    sprite = source.convert("RGBA")
                sprite.thumbnail(
                    (sprite_size, sprite_size),
                    Image.Resampling.LANCZOS
                )

                # Center the sprite within its slot
                sprite_x = int(center_x - sprite.width / 2)
                image.paste(
                    sprite,
                    (sprite_x, sprite_y),
                    sprite
                )

            except (requests.RequestException, OSError) as error:
                print(f"Could not load artwork for '{pokemon.name}': {error}")

def get_card_positions(image_width, image_height, count, top):
    # Calculate the columns and rows needed based on given standings
    columns = 2 if count > 2 else 1
    rows = (count + columns - 1) // columns

    # Calculate available space for the cards
    card_width = (image_width - (3 * STANDINGS_GAP)) // columns

    # Grab the available space for each card and adjust if needed
    available_height = image_height - top  - STANDINGS_GAP
    full_available_card_height = (available_height - STANDINGS_GAP * (rows - 1)) // rows
    card_height = min(full_available_card_height, STANDINGS_MAX_CARD_HEIGHT)

    available_area_height = image_height - top - STANDINGS_GAP
    total_cards_height = rows * card_height + (rows - 1) * STANDINGS_GAP
    start_y = top + (available_area_height - total_cards_height) // 2

    # Fill out the number of cards needed and their positions then return the list
    positions = []
    for i in range(count):
        x = STANDINGS_GAP + (i % columns) * (card_width + STANDINGS_GAP)
        y = start_y + (i // columns) * (card_height + STANDINGS_GAP)
        positions.append((x, y, x + card_width, y + card_height))
    return positions

def draw_signature(image):
    # Create the draw object and Font
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arialbd.ttf", 25)

    # Create the textbox for text calculations
    textbox_signature = draw.textbbox((0, 0), SIGNATURE, font=font)
    text_width = textbox_signature[2] - textbox_signature[0]
    text_height = textbox_signature[3] - textbox_signature[1]

    # Calculate plate dimensions
    plate_width = text_width + SIGNATURE_PADDING[0] * 2
    plate_height = text_height + SIGNATURE_PADDING[1] * 2

    # Center horizontally at the bottom of the image
    x = (image.width - plate_width) // 2
    y = image.height - plate_height - SIGNATURE_LIFT

    # Draw rounded rectangle with border
    draw.rounded_rectangle(
        (x, y, x + plate_width, y + plate_height),
        radius=SIGNATURE_PLATE_RADIUS,
        fill=CARD_COLOR,
        outline=SIGNATURE_BORDER_COLOR,
        width=SIGNATURE_PLATE_BORDER
    )

    # Center the text inside the plate and draw it
    text_x = x + (plate_width - text_width) // 2 - textbox_signature[0]
    text_y = y + (plate_height - text_height) // 2 - textbox_signature[1]
    draw.text(
        (text_x, text_y),
        SIGNATURE,
        font=font,
        fill=TEXT_COLOR
    )

"""
This will take the Standings of the players from the given CSV file and then draw them to the Standings image
"""
def draw_standings(image, filename="standings.csv"):
    # Create the Trainers class for each given in the csv
    local_standings = {}
    with open(filename, mode="r", encoding="utf-8") as file:
        # Create the reader for the csv file
        reader = csv.reader(file)

        # Loop through each row skipping the headers and build a Trainer class for the standings
        _ = next(reader)
        for trainer_data in reader:
            if trainer_data[0] == "":
                break
            local_standings[trainer_data[0]] = build_trainer(
                name=trainer_data[1],
                handle=trainer_data[2],
                local=trainer_data[3],
                pokepaste=trainer_data[4]
            )

    # With the standings create the box for each
    positions = get_card_positions(
        image_width=image.width,
        image_height=image.height,
        count=len(local_standings),
        top=header_height + RHOMBUS_HEIGHT
    )

    for (placing, trainer), bounds in zip(local_standings.items(), positions):
        draw_trainer_card(
            image=image,
            trainer=trainer,
            placing=placing,
            bounds=bounds
        )



# -- Main -----------------------------------------------------------------------------------------

if __name__ == "__main__":
    filename="standings.png"
    standings_image, header_height = draw_theme(theme=THEMES["Portland - Dark"])
    local_object = Local(
        challenge=True, 
        cup=False,
        location="wayward",
        date="September 14th",
        regulation="M-C",
        player_count=25
    )
    draw_title(
        image=standings_image, 
        header_height=header_height,
        local=local_object
    )
    draw_standings(standings_image)
    draw_signature(standings_image)
    standings_image.save(filename)