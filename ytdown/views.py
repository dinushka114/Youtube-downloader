import os
import subprocess
import sys  
from django.shortcuts import render
import pafy
import pytube
from pytube import YouTube
import youtube_dl
import ffmpeg
from moviepy.editor import *

from .forms import LinkForm , ConvertLink
from django.template.defaultfilters import filesizeformat
from django.contrib import messages
def index(request):
    form = LinkForm(request.POST or None)
    if(form.is_valid()):
        url = form.cleaned_data.get('link')
        video = pafy.new(url)

        ##convert to best
        bstv = video.getbestvideo(preftype='mp4')
        bsta = video.getbestaudio(preftype = 'm4a')
        # print(bstv.url)
        # print(bsta.url)
        # print(bstv.resolution)

        # input_video = ffmpeg.input(bstv.url)
        # added_audio = ffmpeg.input(bsta.url).audio.filter('adelay', "1500|1500")
        # merged_audio = ffmpeg.filter([input_video.audio, added_audio], 'amix')

        # ffmpeg.concat(input_video, added_audio, v=1, a=1).output('finished_video.mp4').run()

        embed_link = url.replace('watch?v=' , 'embed/')
        allstreams = video.streams #all streams
        VideoAndAudioStreams = []
        for stream in allstreams:
            VideoAndAudioStreams.append({
                'resolution':stream.resolution,
                'extension':stream.extension,
                'filesize':filesizeformat(stream.get_filesize()),
                'video_url':stream.url + "&title"+stream.title
            })
        AudioStreams = []
        allaudiostreams = video.audiostreams
        for stream in allaudiostreams:
            AudioStreams.append({
                'resolution':stream.resolution,
                'extension':stream.extension,
                'filesize':filesizeformat(stream.get_filesize()),
                'video_url':stream.url + "&title"+stream.title
            })

        return render(request , 'index.html' ,{'all_streams':VideoAndAudioStreams ,
                                                'audio_streams':AudioStreams,
                                'form':form , 'video':embed_link , 'info':video} )
    return render(request , 'index.html' , {'form':form})

def converter(request):
    # home = os.path.expanduser("~")

    form = ConvertLink(request.POST or None)
    if(form.is_valid()):
        url = form.cleaned_data.get('ConvertLink')
        video = pafy.new(url)
        # title = video.title.replace(' ','_')
        # best_audio = video.getbestaudio()
        # BESTFILE = os.path.join(home, "Downloads") + "/" + str(title) + "." + str(best_audio.extension)
        # MP3FILE = os.path.join(home, "Downloads") + "/" + str(title) + ".mp3"
        # # print(BESTFILE , MP3FILE)
        # messages.success(request , 'Your file is downloadin to your downloads folder')
        # best_audio.download(BESTFILE)
        # print ("You have successfully downloaded the ."+str(best_audio.extension)+" file")
        # command = "ffmpeg -i "+str(BESTFILE)+" -vn -ab 128k -ar 44100 -y "+str(MP3FILE)
        # print ("Command to convert audio file to .mp3 format: ", command)
        # subprocess.call(command, shell=True)
        # os.remove(BESTFILE)
        # print ("Generated mp3 file for "+ str(title))
        # return render(request , 'converter.html' , {'form':form})
        
        # name = pytube.extract.video_id(url)
        # print(name)
        # YouTube(url).streams.filter(only_audio=True).first().download(filename=name)
        ydl_opts = {
            'format':'bestaudio/best',
            'postprocessors':[{
                'key':'FFmpegExtractAudio',
                'preferredcodec':'mp3',
                'preferredquality':'192'
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            filename = url
            ydl.download([filename])

    return render(request , 'converter.html' , {'form':form})