from pytube import YouTube

video = YouTube("url")
resolution_list = []

print("Mevcut Video Kaliteleri Şu Şekildedir: ")

for stream in video.streams.filter(file_extension="mp4"):
    resolution_list.append(stream.resolution)

print(resolution_list)
