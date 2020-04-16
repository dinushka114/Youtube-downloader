import os
import subprocess
import sys  
from django.shortcuts import render
import pafy
import pytube
from pytube import YouTube
import youtube_dl
import ffmpeg


from .forms import LinkForm , ConvertLink , PlayListForm
from django.template.defaultfilters import filesizeformat
from django.contrib import messages
def index(request):
    form = LinkForm(request.POST or None)
    if(form.is_valid()):
        url = form.cleaned_data.get('link')
        video = pafy.new(url)

        ##convert to best
        # bstv = video.getbestvideo(preftype='mp4')
        # bsta = video.getbestaudio(preftype = 'm4a')
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

def playlist_downloader(request):
    form = PlayListForm(request.POST or None)
    if(form.is_valid()):
        playlist_url = form.cleaned_data.get('PlayLink')
        playlist = pafy.get_playlist(playlist_url)
        PlayListTitle = playlist['title'] ##playlist eke titile eka
        PlayListAuthor = playlist['author']
        length_of_playlist = len(playlist['items']) # playlist eke tiyana videos gaaana
        # print(length_of_playlist)
     
        links = []
        x = 0
        data = []
        while(x<length_of_playlist):
            data.append({
                'link':playlist['items'][x]['pafy'].getbest().url,
                'thumb':playlist['items'][x]['pafy'].bigthumb,
                'title':playlist['items'][x]['pafy'].title
            })
            x+=1

        return render(request , 'playlist.html' , {'form':form , 
                                                    'data':data ,
                                                     'title':PlayListTitle,
                                                     'author':PlayListAuthor })
  

    return render(request , 'playlist.html' , {'form':form})

