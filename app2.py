import numpy as np
import math
import streamlit as st
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection, PolyCollection
from astropy import units as u

from skyfield.api import Star, load, wgs84, N, S, W, E
from skyfield.data import hipparcos, mpc, stellarium
from skyfield.projections import build_stereographic_projection
from datetime import datetime
from pytz import timezone

# Load city coordinates dataset
city_coordinates = {
    "Delhi": (28.704060, 77.102493),
    "New York": (40.712776, -74.005974),
    "Los Angeles": (34.052235, -118.243683),
    "Chicago": (41.878113, -87.629799),
    "Houston": (29.760427, -95.369804),
    "Phoenix": (33.448376, -112.074036),
    "Philadelphia": (39.952583, -75.165222),
    "San Antonio": (29.424122, -98.493629),
    "San Diego": (32.715736, -117.161087),
    "Dallas": (32.776665, -96.796989),
    "San Jose": (37.338207, -121.886330),
    "Austin": (30.267153, -97.743057),
    "Jacksonville": (30.332184, -81.655647),
    "San Francisco": (37.774929, -122.419418),
    "Columbus": (39.961178, -82.998795),
    "Indianapolis": (39.768333, -86.158043),
    "Fort Worth": (32.755489, -97.330765),
    "Charlotte": (35.227085, -80.843124),
    "Seattle": (47.606209, -122.332069),
    "Denver": (39.739235, -104.990250),
    "Washington": (38.895111, -77.036369),
    "Boston": (42.360081, -71.058884),
    "El Paso": (31.761877, -106.485023),
    "Nashville": (36.162663, -86.781601),
    "Detroit": (42.331429, -83.045753),
    "Oklahoma City": (35.467560, -97.516428),
    "Portland": (45.505106, -122.675026),
    "Las Vegas": (36.169941, -115.139830),
    "Memphis": (35.149532, -90.048981),
    "Louisville": (38.252663, -85.758456),
    "Baltimore": (39.290386, -76.612190),
    "Milwaukee": (43.038902, -87.906471),
    "Albuquerque": (35.084492, -106.651138),
    "Tucson": (32.222607, -110.974709),
    "Fresno": (36.737230, -119.787133),
    "Sacramento": (38.581573, -121.494400),
    "Mesa": (33.415184, -111.831472),
    "Kansas City": (39.099724, -94.578331),
    "Atlanta": (33.749001, -84.387978),
    "Long Beach": (33.770050, -118.193741),
    "Colorado Springs": (38.833881, -104.821365),
    "Raleigh": (35.779591, -78.638176),
    "Miami": (25.761681, -80.191788),
    "Virginia Beach": (36.852531, -75.977985),
    "Omaha": (41.256535, -95.934502),
    "Oakland": (37.804363, -122.271111),
    "Minneapolis": (44.977753, -93.265015),
    "Tulsa": (36.154762, -95.993286),
    "Wichita": (37.686981, -97.335579),
    "Mumbai": (19.076090, 72.877426),
    "Bangalore": (12.971599, 77.594566),
    "Kolkata": (22.572645, 88.363892),
    "Chennai": (13.082680, 80.270721),
    "Hyderabad": (17.385044, 78.486671),
    "Pune": (18.520430, 73.856743),
    "Ahmedabad": (23.022505, 72.571365),
    "Surat": (21.170240, 72.831062),
    "Jaipur": (26.912434, 75.787271),
    "Lucknow": (26.846694, 80.946166),
    "Kanpur": (26.449923, 80.331871),
    "Nagpur": (21.146633, 79.088860),
    "Patna": (25.594095, 85.137566),
    "Indore": (22.719569, 75.857726),
    "Thane": (19.218330, 72.978088),
    "Bhopal": (23.259933, 77.412613),
    "Visakhapatnam": (17.686815, 83.218483),
    "Vadodara": (22.307159, 73.181219),
    "Firozabad": (27.150921, 78.394775),
    "Ludhiana": (30.901000, 75.857300),
    "Rajkot": (22.303894, 70.802160),
    "Agra": (27.176670, 78.008072),
    "Siliguri": (26.727100, 88.395300),
    "Nashik": (19.997454, 73.789803),
    "Faridabad": (28.408913, 77.317787),
    "Patiala": (30.339780, 76.386880),
    "Meerut": (28.984461, 77.706413),
    "Kalyan-Dombivali": (19.221512, 73.164513),
    "Vasai-Virar": (19.405023, 72.839660),
    "Varanasi": (25.317645, 82.973915),
    "Srinagar": (34.083656, 74.797371),
    "Dhanbad": (23.795653, 86.430386),
    "Jodhpur": (26.263863, 73.008957),
    "Amritsar": (31.633979, 74.872264),
    "Raipur": (21.251384, 81.629639),
    "Allahabad": (25.435801, 81.846311),
    "Coimbatore": (11.016844, 76.955832),
    "Jabalpur": (23.181467, 79.986407),
    "Gwalior": (26.218287, 78.182831),
    "Vijayawada": (16.506174, 80.648018),
    "Madurai": (9.925201, 78.119774),
    "Guwahati": (26.144516, 91.736237),
    "Chandigarh": (30.733315, 76.779419),
    "Hubli-Dharwad": (15.364708, 75.123955),
    "Amroha": (28.903492, 78.469849),
    "Moradabad": (28.838931, 78.776840),
    "Gurgaon": (28.459497, 77.026638),
    "Aligarh": (27.897394, 78.088013),
    "Bhilai": (21.194739, 81.350852),
    "Jamshedpur": (22.804567, 86.202875),
    "Gorakhpur": (26.760555, 83.373177),
    "Noida": (28.535517, 77.391029),
    "Warangal": (17.980609, 79.598038),
    "Cuttack": (20.462521, 85.882988),
    "Firozpur": (30.933052, 74.622498),
    "Kochi": (9.931233, 76.267303),
    "Bhavnagar": (21.762946, 72.153212),
    "Dehradun": (30.316496, 78.032188),
    "Durgapur": (23.520444, 87.311923),
    "Asansol": (23.673944, 86.952393),
    "Nanded": (19.138314, 77.321819),
    "Kolhapur": (16.705032, 74.243293),
    "Ajmer": (26.449895, 74.639916),
    "Gulbarga": (17.329251, 76.834655),
    "Jamnagar": (22.470702, 70.057730),
    "Ujjain": (23.179301, 75.784910),
    "Loni": (28.751429, 77.288071),
    "Jhansi": (25.448450, 78.568459),
    "Silchar": (24.827330, 92.797859),
    "Ulhasnagar": (19.218330, 73.163175),
    "Nellore": (14.442598, 79.986457),
    "Jammu": (32.726602, 74.857027),
    "Sangli-Miraj & Kupwad": (16.851170, 74.581900),
    "Mangalore": (12.914141, 74.855956),
    "Erode": (11.341036, 77.717165),
    "Belgaum": (15.849695, 74.497673),
    "Ambattur": (13.114308, 80.149595),
    "Tirunelveli": (8.713892, 77.756651),
    "Malegaon": (20.560027, 74.525322),
    "Gaya": (24.780737, 84.981827),
    "Jalgaon": (21.007657, 75.562606),
    "Udaipur": (24.585445, 73.712479),
    "Maheshtala": (22.506933, 88.251968),
    "Tirupur": (11.005547, 77.007744),
    "Davanagere": (14.464388, 75.921867),
    "Kozhikode": (11.258753, 75.780410),
    "Akola": (20.703768, 77.021921),
    "Kurnool": (15.828126, 78.037279),
    "Rajpur Sonarpur": (22.412959, 88.446152),
    "Bokaro Steel City": (23.669297, 86.151115),
    "South Dumdum": (22.614308, 88.389862),
    "Bellary": (15.139393, 76.921440),
    "Patiala": (30.339780, 76.386880),
    "Gopalpur": (19.268597, 84.590088),
    "Agartala": (23.831457, 91.286148),
    "Bhagalpur": (25.258170, 86.983849),
    "Muzaffarnagar": (29.472360, 77.708817),
    "Ajmer": (26.449895, 74.639916),
    "Aligarh": (27.897394, 78.088013),
    "Bhilwara": (25.347071, 74.640381),
    "Guntur": (16.306652, 80.436539),
    "Bhatpara": (22.871124, 88.408012),
    "Saharanpur": (29.966793, 77.549942),
    "Gorakhpur": (26.760555, 83.373177),
    "Bikaner": (28.022943, 73.311890),
    "Kharagpur": (22.346010, 87.231972),
    "Bally": (22.648548, 88.341950),
    "Bhilai": (21.194739, 81.350852),
    "Brahmapur": (19.314175, 84.794090),
    "Muzaffarpur": (26.120891, 85.364723),
    "Ahmednagar": (19.095207, 74.749588),
    "Mathura": (27.492413, 77.673676),
    "Kollam": (8.893212, 76.614143),
    "Avadi": (13.114342, 80.109375),
    "Kadapa": (14.477234, 78.823753),
    "Anantapur": (14.681897, 77.600594),
    "Kamarhati": (22.671868, 88.374519),
    "Sambalpur": (21.470663, 83.970459),
    "Bilaspur": (22.080440, 82.159957),
    "Shahjahanpur": (27.880491, 79.910942),
    "Satara": (17.680416, 73.683037),
    "Bijapur": (16.824421, 75.715691),
    "Rampur": (28.815354, 79.025749),
    "Shivamogga": (13.929930, 75.568100),
    "Chandrapur": (19.959141, 79.296555),
    "Junagadh": (21.522180, 70.457932),
    "Thrissur": (10.527642, 76.214432),
    "Alwar": (27.553286, 76.634361),
    "Bardhaman": (23.232511, 87.861473),
    "Kulti": (23.731651, 86.843735),
    "Kakinada": (16.989100, 82.247467),
    "Nizamabad": (18.671540, 78.098804),
    "Parbhani": (19.270329, 76.772652),
    "Tumkur": (13.340880, 77.100096),
    "Khammam": (17.247253, 80.151443),
    "Ozhukarai": (11.942636, 79.830387),
    "Bihar Sharif": (25.197200, 85.521256),
    "Panipat": (29.390047, 76.963486),
    "Darbhanga": (26.152010, 85.897141),
    "Bally": (22.648548, 88.341950),
    "Aizawl": (23.727106, 92.717636),
    "Dewas": (22.965896, 76.056504),
    "Ichalkaranji": (16.693251, 74.459915),
    "Karnal": (29.685693, 76.990482),
    "Bathinda": (30.211525, 74.945473),
    "Jalna": (19.842831, 75.885780),
    "Ghaziabad": (28.669156, 77.453758),
    "Gurgaon": (28.459497, 77.026638),
    "Noida": (28.535517, 77.391029),
    "Faridabad": (28.408913, 77.317787),
    "Greater Noida": (28.474388, 77.503990),
    "Meerut": (28.984461, 77.706413),
    "Panipat": (29.390047, 76.963486),
    "Karnal": (29.685693, 76.990482),
    "Sonipat": (28.995968, 77.011272),
    "Rohtak": (28.895515, 76.606613),
    "Bhiwani": (28.793600, 76.139807),
}

def generate_starmap(date, hour, minute, second, place):
    latitude, longitude = city_coordinates.get(place, (0, 0))
    ye, mo, da = date.year, date.month, date.day
    
    # Changeable params
    limiting_magnitude = 5
    
    # time `t` we use for everything else.
    GMT = timezone('Asia/kolkata')
    ts = load.timescale()
    t = ts.from_datetime(GMT.localize(datetime(ye, mo, da, hour, minute, second)))
    
    # Location
    north_south = S if latitude < 0 else N
    west_east = W if longitude < 0 else E
    lat = abs(latitude)
    long = abs(longitude)
    
    location = wgs84.latlon(lat * north_south, long * west_east, elevation_m=0)
    position = location.at(t).from_altaz(alt_degrees=90, az_degrees=0)

    # An ephemeris from the JPL provides Sun and Earth positions.
    eph = load('de421.bsp')
    earth = eph['earth']

    # The Hipparcos mission provides our star catalog.
    with load.open(hipparcos.URL) as f:
        stardata = hipparcos.load_dataframe(f)

    # And the constellation outlines come from Stellarium.
    url = ('https://raw.githubusercontent.com/Stellarium/stellarium/master'
       '/skycultures/western_SnT/constellationship.fab')

    with load.open(url) as f:
        consdata = stellarium.parse_constellations(f)

    url2 = ('https://raw.githubusercontent.com/Stellarium/stellarium/master'
            '/skycultures/western_SnT/star_names.fab')

    with load.open(url2) as f2:
        star_names = stellarium.parse_star_names(f2)


    def generate_constellation_lines(data, polygon=False):
        edges = [edge for name, edges in data for edge in edges]
        edges_star1 = [star1 for star1, star2 in edges]
        edges_star2 = [star2 for star1, star2 in edges]
        xy1 = stardata[['x', 'y']].loc[edges_star1].values
        xy2 = stardata[['x', 'y']].loc[edges_star2].values

        if polygon:
            return [xy1]
        else:
            return np.rollaxis(np.array([xy1, xy2]), 1)

    # We will center the chart on position.
    projection = build_stereographic_projection(position)
    field_of_view_degrees = 180.0

    # Now that we have constructed our projection, compute the x and y
    # coordinates that each star will have on the plot.
    star_positions = earth.at(t).observe(Star.from_dataframe(stardata))
    stardata['x'], stardata['y'] = projection(star_positions)

    # Create a True/False mask marking the stars bright enough to be
    # included in our plot.  And go ahead and compute how large their
    # markers will be on the plot.
    bright_stars = stardata[stardata['magnitude'] <= limiting_magnitude]
    bright_stars = bright_stars[(bright_stars['x'] ** 2 + bright_stars['y'] ** 2) ** 0.5 <= 1]
    magnitude = bright_stars['magnitude']
    marker_size = (0.7 + limiting_magnitude - magnitude) ** 2.0

    # get the altitude and azimuth for filtered stars
    alts = []
    azs = []
    for star, row in bright_stars.iterrows():
        alt_temp, az_temp, distance = (earth + location).at(t).observe(Star.from_dataframe(stardata.loc[star])).apparent().altaz()
        alts.append(1 - (alt_temp.to(u.rad) / (u.radian * math.pi * 0.5)))
        azs.append(az_temp.to(u.rad) / u.radian)

    bright_stars['alt'], bright_stars['az'] = alts, azs

    fig = plt.figure(figsize=[12, 12])
    ax = fig.add_subplot(projection='polar')
    c = ax.scatter(bright_stars['az'], bright_stars['alt'], s=marker_size, c='white', alpha=0.75)

    # Draw the constellation lines.
    constellations = LineCollection(generate_constellation_lines(consdata),
                                    colors='#00f2', linewidths=1, zorder=-1, alpha=0.5)
    ax.add_collection(constellations)

    for row in consdata:
        name = row[0]
        hip = row[1][0][0]
        if hip in bright_stars.index:
            bsrow = bright_stars.loc[[hip]]
            ax.text(bsrow['az'], bsrow['alt'], str(name), c='white', fontsize=9, weight='bold', ha='center')

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(1)
    ax.xaxis.set_visible(False)
    ax.set_yticklabels([])
    ax.grid(False)
    ax.set_facecolor('#000000')

    

    return fig

def main():
    st.title('Starmap Generator')
    st.write("Generate StarMaps for your favorite dates ❤️")
    
    # Date input
    min_date = datetime(1900, 1, 1)
    max_date = datetime(2100, 12, 31)
    date = st.date_input('Select date:', datetime.now(), min_value=min_date, max_value=max_date)
    
    # Time input
    col1, col2, col3 = st.columns(3)
    with col1:
        hour = st.number_input('Hour', min_value=0, max_value=23)
    with col2:
        minute = st.number_input('Minute', min_value=0, max_value=59)
    with col3:
        second = st.number_input('Second', min_value=0, max_value=59)

    place = st.selectbox('Place:', list(city_coordinates.keys()))
    
    if st.button('Generate Starmap'):
        fig = generate_starmap(date, hour, minute, second,place)
        st.pyplot(fig)
if __name__ == "__main__":
    main()
