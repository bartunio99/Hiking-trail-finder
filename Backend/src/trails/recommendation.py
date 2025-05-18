#recommends trails based on user preferences
#preferences:
#   - difficulty
#   - length
#   - location

from db import database as db
from visualization import visualization


def recommend_trails(difficulty, length, location):
    #get trails from location
    trails = db.return_hikes_by_difficulty(location, difficulty)

    #length in km

    recommend_trails = []

    for trail in trails:
        if trail["length"] <= length * 1.02 and trail["length"] >= length * 0.98:
            recommend_trails.append(trail)

    return recommend_trails