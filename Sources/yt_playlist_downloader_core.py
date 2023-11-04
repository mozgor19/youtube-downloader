from pytube import Playlist

url = Playlist("url")
print(f"Downloading: {url.title}")

for video in url.videos:
    video.streams.first().download("dosya yolu")

print("İndirme tamamlandı!")
