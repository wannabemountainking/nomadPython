
# BLUEPRINT | DONT EDIT

import requests

movie_ids = [
    238, 680, 550, 185, 641, 515042, 152532, 120467, 872585, 906126, 840430
]

# /BLUEPRINT

# 👇🏻 YOUR CODE 👇🏻:

URL = "https://nomad-movies.nomadcoders.workers.dev/movies"

movie_data = []

for movie_id in movie_ids:
	response = requests.get(url=f"{URL}/{movie_id}")
	movie_info = response.json()
	data = dict(title=movie_info.get("title"), overview=movie_info.get("overview"), vote_average=movie_info.get("vote_average"))
	movie_data.append(data)

for item in movie_data:
	print(f"""
	TITLE: {item.get("title")}
	OVERVIEW: {item.get("overview")}
	VOTE AVERAGE: {item.get("vote_average")}
	""")

# /YOUR CODE

