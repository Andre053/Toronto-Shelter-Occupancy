# TODO

## Key tasks
[ ] Make compatible for different screen types
    - Currently developed for desktop

## Visualizations
[ ] Make SVG dependent on screen size
    - Viewbox solution: [Stack Overflow](https://stackoverflow.com/questions/13632169/using-viewbox-to-resize-svg-depending-on-the-window-size), [Observable article](https://observablehq.com/@uw-info474/why-use-viewbox)

## Features
[ ] Geographic heatmap of shelter locations
[ ] Inferential analysis of data

## Data understanding
[ ] Missing data
    - Rows missing location
        37058 rows have no location data
        Related to shelter IDs: [ 3 42 82 30 24 83 40  8 27 20]
            'Seaton House' (3)
            "Fred Victor Women's Hostel" (42)
            'SSHA Etobicoke Hotel Program' (82)
            "St. Simon's Shelter" (30)
            'HFS - Scarborough Shelter' (24)
            'Expansion  Sites' (83)
            'COSTI Reception Centre' (40)
            "Scott Mission Men's Ministry" (8)
            "Nellie's" (27)
            'Covenant House' (20)
[ ] Difference in FSA in dataset vs. map
    Dataset FSA values:
        'M3L' 'M5S' 'M2J' 'M9W' 'M6R' 'M6H' 'M6G' 'M1P' 'M5A' 'M3M' 'M4P' 'M1M'
        'M1E' 'M5V' 'L4L' 'N/A' 'M6N' 'M5T' 'M5H' 'M6J' 'M6C' 'M5B' 'M4C' 'M5J'
        'M5E' 'M1T' 'M3B' 'M3N' 'M4X' 'M4Y' 'M6A' 'M6K' 'M1K' 'M2M' 'M6E' 'M4K'
        'M4W' 'M4M' 'M8Y' 'M6P' 'M5C' 'M1H' 'M9V' 'M5R' 'M4T' 'M4L' 'M1L' 'M1B'
        'M2H' 'M1R' 'M2N' 'M5G' 'M1G' 'M9C' 'M8V'

    Geojson FSA values: 
        'M1B', 'M1C', 'M1E', 'M1G', 'M1H', 'M1J', 'M1K', 'M1L', 'M1M', 'M1N', 'M1P', 
        'M1R', 'M1S', 'M1T', 'M1V', 'M1W', 'M1X', 'M2H', 'M2J', 'M2K', 'M2L', 'M2M', 
        'M2N', 'M2P', 'M2R', 'M3A', 'M3B', 'M3C', 'M3H', 'M3J', 'M3K', 'M3L', 'M3M', 
        'M3N', 'M4A', 'M4B', 'M4C', 'M4E', 'M4G', 'M4H', 'M4J', 'M4K', 'M4L', 'M4M', 
        'M4N', 'M4P', 'M4R', 'M4S', 'M4T', 'M4V', 'M4W', 'M4X', 'M4Y', 'M5A', 'M5B', 
        'M5C', 'M5E', 'M5G', 'M5H', 'M5J', 'M5M', 'M5N', 'M5P', 'M5R', 'M5S', 'M5T', 
        'M5V', 'M6A', 'M6B', 'M6C', 'M6E', 'M6G', 'M6H', 'M6J', 'M6K', 'M6L', 'M6M', 
        'M6N', 'M6P', 'M6R', 'M6S', 'M8V', 'M8W', 'M8X', 'M8Y', 'M8Z', 'M9A', 'M9B', 
        'M9C', 'M9L', 'M9M', 'M9N', 'M9P', 'M9R', 'M9V', 'M9W'
    
    Not shared:
        'M1W', 'M2L', 'M4V', 'M9P', 'M5M', 'M4H', 'M6B', 'M1X', 'M4E', 'M4R', 'M1S', 
        'N/A', 'M6M', 'M5N', 'M1C', 'M8X', 'M4B', 'M3H', 'M5P', 'M4J', 'L4L', 'M1J', 
        'M4G', 'M4N', 'M2P', 'M1N', 'M6S', 'M3A', 'M6L', 'M2R', 'M3J', 'M3C', 'M9N', 
        'M8Z', 'M2K', 'M9R', 'M9L', 'M9M', 'M8W', 'M9B', 'M3K', 'M4A', 'M4S', 'M9A', 
        'M1V'
