# config.py

# Factory geographical coordinates
FACTORIES = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371},
    "Sugar Shack": {"lat": 48.11914, "lon": -96.18115},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487},
    "The Other Factory": {"lat": 35.1175, "lon": -89.971107}
}

# Current product-to-factory assignments based on legacy static rules
PRODUCT_MAPPING = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory"
}

# Approximated geographic centers for US Regions (matching dataset regions)
REGION_CENTERS = {
    "Interior": {"lat": 39.8, "lon": -98.5},
    "Atlantic": {"lat": 38.9, "lon": -77.0},
    "Gulf": {"lat": 30.0, "lon": -90.0},
    "Pacific": {"lat": 37.8, "lon": -122.4}
}

# KPI Definitions for the dashboard
KPI_DEFINITIONS = {
    "Lead Time Reduction (%)": "Operational gain",
    "Profit Impact Stability": "Financial safety",
    "Scenario Confidence Score": "Reliability",
    "Recommendation Coverage": "Scalability"
}

# Division mapping for products
DIVISION_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Chocolate",
    "Wonka Bar - Fudge Mallows": "Chocolate",
    "Wonka Bar -Scrumdiddlyumptious": "Chocolate",
    "Wonka Bar - Milk Chocolate": "Chocolate",
    "Wonka Bar - Triple Dazzle Caramel": "Chocolate",
    "Laffy Taffy": "Sugar",
    "SweeTARTS": "Sugar",
    "Nerds": "Sugar",
    "Fun Dip": "Sugar",
    "Fizzy Lifting Drinks": "Sugar",
    "Everlasting Gobstopper": "Other",
    "Hair Toffee": "Other",
    "Lickable Wallpaper": "Other",
    "Wonka Gum": "Other",
    "Kazookles": "Other"
}