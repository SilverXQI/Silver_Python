import yt_dlp


def download_video(url, quality='1080p'):
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # 或者 youtube_dl.YoutubeDL
        ydl.download([url])


if __name__ == "__main__":
    video_url = input("Enter the video url: ")  # 替换为你想下载的YouTube视频URL
    download_video(video_url, '1080p')  # 你可以修改 '1080p' 为其他清晰度，如 '720p'
    print("Downloaded successfully")