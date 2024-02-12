import streamlit as st
import numpy as np
import pandas as pd
from skyfield.api import load, Star, wgs84, N, S, W, E
from skyfield.data import hipparcos, stellarium
from skyfield.magnitudelib import planetary_magnitude
from skyfield.projections import build_stereographic_projection
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import io
from PIL import Image, ImageOps, ImageFont, ImageDraw

# Function to load star and constellation data
def load_data(filename):
    data = pd.read_csv(filename)
    stars = []
    for i, row in data.iterrows():
        stars.append(Star(hipparcos=row['HIP'], ra=row['RA'], dec=row['Dec']))
    return stars

# Function to plot constellations
def plot_constellations(ax, constellations):
    for constellation in constellations:
        lines = []
        for i in range(len(constellation) - 1):
            lines.append([constellation[i], constellation[i + 1]])
        lc = LineCollection(lines, color='yellow', linewidth=0.5)
        ax.add_collection(lc)

# Function to label major constellations
def label_major_constellations(ax, constellations, scale=0.04):
    label_positions = {
        'Ursa Major': (0.7, 0.4),
        'Ursa Minor': (0.4, 0.8),
        'Cassiopeia': (0.1, 0.7),
        'Orion': (0.4, 0.2),
        'Canis Major': (-0.3, -0.4),
        'Leo': (-0.6, 0.3),
        'Bootes': (-0.8, 0.5),
        'Hercules': (-0.5, 0.8),
        'Cygnus': (0.3, 0.9),
    }
    for name, pos in label_positions.items():
        if name in constellations:
            star = constellations[name]
            ax.text(star.ra.degrees, star.dec.degrees, name, ha='center', va='center',
                    transform=ax.transData, fontsize=8, bbox={'facecolor': 'white', 'edgecolor': 'none'})

# Function to calculate planet positions
def get_planet_positions(date, planets=['Mars', 'Jupiter', 'Saturn']):
    planets_dict = {}
    for planet_name in planets:
        planet = load(planet_name).at(date)
        planets_dict[planet_name] = (planet.ra.degrees, planet.dec.degrees)
    return planets_dict

# Function to plot planets
def plot_planets(ax, planets, colors):
    for name, (ra, dec) in planets.items():
        color = colors.get(name, 'yellow')
        ax.scatter(ra, dec, marker='o', color=color, s=60)

# Function to create planet key
def create_planet_key(planets, colors):
    image = Image.new('RGB', (200, 100), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('arial.ttf', 12)
    y = 10
    for name, color in zip(planets, colors):
        draw.text((10, y), name + ':', font=font, fill='black')
        draw.rectangle((30, y - 5, 40, y + 5), fill=color)
        y += 20
    return image

# Function to generate star map image
def generate_star_map(location, date, time, limiting_mag, include_planets=False, planet_labeling='key'):
    # Set up projection and figure
    eph = load('de421.dat')
    ts = load.timescale()
    t = ts.utc(date.year, date.month, date.day, time.hour, time.minute, time.second)
    site = wgs84.latlon(location['latitude'], location['longitude'])

    # Load stars and constellations
    stars = load_data('stars.csv')
    constellations = stellarium.constellations

    
