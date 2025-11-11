import numpy as np
import pandas as pd
import math, os
from tabulate import tabulate
import urllib.request

from subs.get_json import get_movies

if __name__ == "__main__":
    movie = get_movies()

print("Movie info", movie.info())
print(movie.head(3))
print(movie.tail(3))
print(movie)
print(movie.ndim, movie.shape, movie.size)

# movie_reduced = movie.drop(0, inplace=True)
movie_reduced = movie.drop(0)

percentages = movie_reduced["language"].value_counts(normalize=True) * 100
percentages = percentages.apply(lambda x: f"{x:.2f} %")
print(percentages)

print(movie.movie_title)
print(movie.gross.describe())
