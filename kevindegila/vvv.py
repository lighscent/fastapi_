TEST_COUNT = 3
total_videos = 16

print(
    f"{total_videos} vidéos trouvées dans la playlist"
    + f" (limité à {TEST_COUNT} pour les tests)."
    if TEST_COUNT
    else ""
)
