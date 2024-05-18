from django.shortcuts import render,redirect
import os
from django.http import HttpResponse 
from pytube import YouTube
from django.core.cache import cache
import sys


# Create your views here.


def home(request):

    convert(request)
    
    
    return render(request, 'index.html')



def convert(request):
    if request.method =='POST':
        try:
            yturl = request.POST.get('url')            # Download the audio stream from the YouTube video
            yt = YouTube(yturl)
            Title = yt.title
            print(yt.title)
            print("downloading...")
            stream = yt.streams.filter(only_audio=True).first()
                
                # Download and save the audio file in the same directory as the script
            output_path = os.path.join(os.getcwd(), Title+".mp3")
            download_path = stream.download(filename=Title+".mp3")

                # Rename the temporary file to the desired output file
            os.rename(download_path, output_path)
            print(f"Audio file created: {output_path}")
            cache.clear()
            


        except Exception as e:
            print(f"An error occurred: {e}")
            cache.clear()
    

    



