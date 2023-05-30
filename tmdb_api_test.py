import requests
import json

url = "https://api.themoviedb.org/3/movie/upcoming"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZjQzZjc1YmUwYmI5OGY1MDAxYWQyYzEyY2MzZDRmMyIsInN1YiI6IjY0NzRhOWYzNWNkMTZlMDBhNjU2ZmExYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.vacAr_9iPf-EMaq4XpHRBAoLViRO16GCic9Qb-ZjZuE"
}

proxies = {
    'https': 'http://158.69.48.228:3128',
}

response = requests.get(url, headers=headers, proxies=proxies)

f = open('upcoming.json', 'w')
json.dump(response.json(), f)
