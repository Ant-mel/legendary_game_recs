# The World Best Game Recommendation Engine

## Intro
Gaming has expanded rapidly over the last 5 years, and trying to find something that fits your niche can be tough. 

We found many recommendation platforms, we even tried Bard and ChatGPT... but their agendas mainly lie around blockbuster games. Our mission was to beat the blockbuster bias. 

## The Data
**Backloggd.com**

Backloggd is a listing site for games from all eras, where players gather to review, list and search for their next adventure. 90% of our data is scraped from Backloggd. 

**IGDB.com** 

IGDB is the API that feeds Backloggd, and we used it to further supliment our data. We also use it to source information on our front end. 

## The Approach
**Natural Language Processing**
Games have genres, but they can be repetative, e.g 'Turn based strategy', 'Strategy' & 'Tactical'. We wanted to supliment these genres by using NLP models to create 'new' genres. This NLP model was trained off the game descriptions, and created 25 'new genres' -  we call them Nuances. 

**Yeo-Johnson scaling**


KNeirestNeighbours
