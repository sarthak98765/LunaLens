# 🌌 LunaLens

LunaLens is a Python-based project that generates a sky map for a specific date, time, and location. It visualizes constellations, stars, and planets, providing a customized view of the night sky.

---

## 🚀 Features

- Generates a star map for a given date, time, and location.
- Customizable parameters for star magnitude, colors, and background.
- Includes constellations and planets with options to toggle labels and keys.
- Flexible text annotations to describe location, time, and other details.
- Supports export of high-quality images for printing or sharing.

---

## 🔧 Technologies Used

- **Python Libraries**:
  - `numpy`, `pandas`, `matplotlib` for data handling and visualization.
  - `skyfield` for astronomical calculations.
  - `Pillow` for image processing.
- **Datasets**:
  - HIPPARCOS Star Catalog.
  - Constellation and star names from Stellarium.

---

## 📝 Configuration Parameters

| Parameter            | Description                                                                 |
|----------------------|-----------------------------------------------------------------------------|
| `FONT_PATH`          | Path to the font file used for annotations.                                |
| `DIAL_IMAGE_PATH`    | Path to the dial background image.                                         |
| `limiting_magnitude` | Filter stars by brightness (higher values include dimmer stars).           |
| `lat`, `long`        | Latitude and longitude of the location.                                    |
| `include_planets`    | Toggle inclusion of planets in the sky map.                                |
| `data_type`          | Options: `stars`, `starsandlines`, `all`.                                 |
| `text_loc`           | Position of text annotations (`above`, `below`, `none`).                  |
| `background_colour`  | Background color of the sky map (`black`, `blue`, `grey`, etc.).          |

---
