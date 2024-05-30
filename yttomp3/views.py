from django.shortcuts import render, redirect
import os
from pytube import YouTube
from django.core.cache import cache


def home(request):
    if request.method == 'POST':
        return convert(request)
    return render(request, 'index.html')


def convert(request):
    if request.method == 'POST':
        try:
            yturl = request.POST.get('url')
            yt = YouTube(yturl)
            Title = yt.title
            print(yt.title)
            print("downloading...")
            stream = yt.streams.filter(only_audio=True).first()

            # Download and save the audio file in the same directory as the script
            output_path = os.path.join(os.getcwd(), Title + ".mp3")
            download_path = stream.download(filename=Title + ".mp3")

            # Rename the temporary file to the desired output file
            os.rename(download_path, output_path)
            print(f"Audio file created: {output_path}")
            cache.clear()

            # Redirect to avoid form resubmission
            return redirect('home')

        except Exception as e:
            print(f"An error occurred: {e}")
            cache.clear()
            return render(request, 'index.html', {'error': str(e)})

    return redirect('home')
