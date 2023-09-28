# The World Best Game Recommendation Engine

## Intro

Gaming has expanded rapidly over the last 5 years, and trying to find something that fits your niche can be tough.

We found many recommendation platforms, we even tried Bard and ChatGPT... but their agendas mainly lie around blockbuster games. Our mission was to beat the blockbuster bias.

## The Data

**[Backloggd.com](http://backloggd.com/)**

Backloggd is a listing site for games from all eras, where players gather to review, list and search for their next adventure. 90% of our data is scraped from Backloggd.

**[IGDB.com](http://igdb.com/)**

IGDB is the API that feeds Backloggd, and we used it to further supplement our data. We also use it to source information on our front end.

## The Approach

**Natural Language Processing**
Games have genres, but they can be repetitive, e.g 'Turn based strategy', 'Strategy' & 'Tactical'. We wanted to supplement these genres by using NLP models to create 'new' genres. This NLP model was trained off the game descriptions, and created 25 'new genres' -  we call them Nuances.

**Yeo-Johnson scaling**
The data has insanely right skewed. And it was biasing our model quite a lot. We employed both Yeo and Johnson for their expert scaling abilities, and they proved to be effective. Although difficult to gauge, we believe it improved the model by 10%, over traditional MinMax Scaling. 

**KNearestNeighbours**
We chose to run a KNN model as it brings back multiple Neighbours. This was essential in allowing gamers to filter their recommendations. 

Like Breath of the Wild, but want a racing game? Try it out! 

## Front End
We build all of this on Streamlit. 

## The Future
Our data gets old, quickly. We aim to automate scraping, processing and retraining to keep the model fresh. 
We also have data on upcoming games, and are still working out how to recommend those - perhaps another model?

# Try it out
[legendary-game-recs-test.streamlit.app](legendary-game-recs-test.streamlit.app)
