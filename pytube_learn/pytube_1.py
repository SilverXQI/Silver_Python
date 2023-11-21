import pytube

download_loc = './'
video_url = input("Enter the video url: ")
video_instance = pytube.YouTube(video_url)
stream = video_instance.streams.get_highest_resolution()
stream.download()
print("Downloaded successfully")