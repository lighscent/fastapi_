from tools import *
import numpy as np
import pandas as pd
import math, os
from tabulate import tabulate
import urllib.request

from subs.get_json import get_movies


if __name__ == "__main__":
    movie = get_movies()

cls()
print("Movie info :")
print(movie.info())

# exit()
sl()
print(movie.shape)
print('head(3) :', movie.head(3), sep='\n')

sl()
print('tail(3) :', movie.tail(3), sep='\n')

sl()
print(movie)

sl()
print(movie.ndim, movie.shape, movie.size)

# movie_reduced = movie.drop(0, inplace=True)
movie_reduced = movie.drop(0)
print("movie.drop(0)...")
print(movie_reduced.ndim, movie_reduced.shape, movie_reduced.size)

sl()
percentages = movie_reduced["language"].value_counts(normalize=True) * 100
percentages = percentages.apply(lambda x: f"{x:.2f} %")
print(percentages)

sl()
print(movie.movie_title)
sl()
print(movie.gross.describe())
