# Pokémon VGC Standings Generator

A Python tool that automates the creation of Pokémon Video Game Championships (VGC) local tournament standings graphics. It takes tournament information and player standings from a CSV file, retrieves Pokémon teams from PokéPaste, and generates a standings image featuring player placements, names, social media handles, and Pokémon team artwork.

## Features

* **CSV-based tournament data**: Store tournament metadata and player standings in one file.
* **PokéPaste integration**: Retrieve each player's Pokémon team from a PokéPaste URL.
* **Pokémon artwork**: Display Pokémon sprites and artwork using image URLs from PokéAPI and other supported sources.
* **Automated standings cards**: Generate player cards containing placement, player name, handle, and Pokémon team.
* **Placement-based styling**: Highlight first, second, and third place with gold, silver, and bronze colors.
* **Customizable graphics**: Configure colors, fonts, backgrounds, headers, borders, and layout.
* **Automated layout**: Arrange and center trainer cards based on the number of participants.

## Requirements

### If you want to just run the script
All that is needed to run the script is to adjust the `data.csv` file within the directory and run the `.eve` to create the standings.

### If you want to iterate on the scripting
* Python 3.10 or later recommended.
* Pillow for image creation and manipulation.
* Requests for retrieving online Pokémon data and artwork.
* A valid PokéPaste URL for each player whose team should appear in the graphic.
* Any image assets and fonts required by your chosen theme.

## Installation

1. Clone or download this repository.

```
git clone <repository-url>
cd <repository-folder>
```

2. Install the dependencies.

```
pip install -r requirements.txt
```

## CSV Format

The generator uses a single CSV file containing two sections:

### Tournament metadata.

The first row contains the metadata column names, and the second row contains the values for the tournament. For example, if you wanted to do a standings for a local that happeneds to be very simillar to the Masters Eight tournament you could do something like this.

|    location    |    date    | challenge | cup | regulation | player count |
| :------------: |:----------:|:---------:|:---:|:----------:|:------------:|
| Wyndon Stadium |  July 8th  |           |  x  |    M-8     |      8       |

### Player standings

After the metadata, include a blank row followed by the player standings header. For example if you wanted to do a top 4 of that cup you would put these down.

| placing |     name    |    handle    |         local          |                paste                 |
|:-------:|:-----------:|:------------:|:----------------------:|:------------------------------------:|
|    1    | Ash Ketchum |  @pikafan25  |  Wyndon-Cup-7-8-2022   | https://pokepast.es/33bbc4f4633968dc |
|    2    |    Leon     |              |  Wyndon-Cup-7-8-2022   | https://pokepast.es/380a942db3548064 |
|    3    |   Cynthia   |              |  Wyndon-Cup-7-8-2022   | https://pokepast.es/0b04ab36eb7d7b89 |
|    4    |   Diantha   |   @mskalos   |  Wyndon-Cup-7-8-2022   | https://pokepast.es/77ac36ad28fa6ea6 |

#### Notes:
* The `handle` is a location to put a players Twitter or X handle, this section can be left blank and the standings will adjust accordingly.
* The `local` is input for a later time and more information can be found in the `Limitations and Future Improvements` in a later section.

## Example Standing
![example](/standings.png "example")

## Usage

1. Create a CSV file with the tournament metadata and player standings.
2. Verify that each player's PokéPaste URL is accessible.
3. Run the main Python script.
```
python generate_standings.py
```
4. The generator processes the event data, builds the trainer and Pokémon objects, draws the standings graphic, and saves the resulting image.

The exact command and output location depend on how the entry point and output path are configured in the current version of the project.

If you are wanting to recreate the `.exe` run
```
 pyinstaller generate_standings.py --onefile --noconsole
 ```
Then inside the `dist` folder pull out the `.exe` and move it into the main directory. You can then remove the `dist` and the `build` folders, as well as the `generate_standings.spec` file.

## Project Structure
A suggested project structure is:

```
vgc_standings/
├── generate_standings.py
├── standings.csv
├── requirements.txt
├── README.md
├── assets/
│   ├── header.png
│   └── background.png
└── output/
    └── standings.png
```

`generate_standings.py` — Main script, data loading, Pokémon retrieval, and image generation.

`standings.csv` — Tournament metadata and player standings.

`requirements.txt` — Python dependencies.

`assets/` — Header images, backgrounds, and other graphics.

`output/` — Generated standings images.

Your actual repository may use different filenames or directories.

## How It Works

The generator follows this general workflow:

1. **Load tournament data**: Read the CSV and create a Local object containing the event metadata.
2. **Build trainers**: Create a dictionary mapping each placement to its corresponding Trainer object.
3. **Retrieve teams**: Fetch and parse the PokéPaste for each trainer.
4. **Create Pokémon objects**: Store Pokémon names, items, abilities, moves, and artwork URLs.
5. **Calculate card positions**: Determine card dimensions and arrange them based on the number of trainers.
6. **Draw the graphic**: Use Pillow's ImageDraw functionality to render the background, title, trainer cards, Pokémon artwork, placement badges, borders, and creator credit.
7. **Save the image**: Export the finished standings graphic.

### Data Sources

* **PokéAPI** — Pokémon data and available sprites.
* **PokéAPI Sprites Repository** — Pokémon sprite and artwork assets.
* **PokéPaste** — Competitive Pokémon team exports.

Some alternate Pokémon forms may not have the desired artwork available through the standard PokéAPI endpoints. These forms may require a separate image URL or a custom mapping. With new Pokemon being created this script may not be able to work with the inital release as it depends on the PokéAPI's data, but should update accordingly in due time.

## Limitations and Future Improvements

### Potential future improvements include:

* Caching downloaded Pokémon artwork to reduce repeated network requests.
* Adding more robust support for alternate forms and variants.
* Validating CSV data and reporting malformed PokéPaste URLs.
* Supporting more flexible layouts for different player counts.
* Creating more themes.
* Adding automated tests for CSV loading, PokéPaste parsing, and card positioning.

# License and Attribution

This project is intended to automate the creation of community Pokémon VGC standings graphics.

Pokémon names, artwork, and related assets belong to their respective owners. Review the relevant asset and API terms before redistributing generated graphics or artwork.