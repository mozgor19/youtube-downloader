from pytube import YouTube

url = YouTube("video linki").streams.get_highest_resolution()


url.download("indirmek istediğin yer")
print("İndirme tamamlandı!")
