from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext
from .forms import TextForm, ImageForm, AudioForm
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.decorators import login_required
from .text_encrypt import text_encrypt, text_decrypt
from .audio_encrypt import audio_encrypt, music, audio_decrypt
from django.shortcuts import redirect, render
from .models import PostFile
from django.template import loader
from .forms import DocumentForm
from .forms import FilesForm
from .forms import DecryptForm


import shutil
import os
import numpy as np


# Views

# connaitre le type de fichier d'encodage
def eltOut(file):
    taille = os.path.getsize(file) / (1024 * 1024)

    if taille < 5:
        # image
        return ['media/image/image.jpeg', 'image.jpeg']
    elif 5 < taille < 20:
        # music
        return ['media/son/son.mp3', 'son.mp3']
    elif taille > 20:
        # video
        return ['media/video/video.mp4', 'video.mp4']


def chiffre(file, dossier_int, fileOut):
    shutil.make_archive('media/archive_shutil', format='zip', root_dir=dossier_int)
    cache = eltOut(file)

    test = False
    shutil.copy(cache[0], fileOut)
    with open(fileOut + '/' + cache[1], 'ab') as elt1:
        # write le separarteur
        elt1.write('##'.encode('utf-8'))
        with open(file, 'rb') as elt2:
            # write du flux chriffer
            elt1.write(elt2.read())
            test = True
    return test


# dechiffrer
def dechiffre(filecache):
    with open(filecache, 'rb') as f:
        content = f.read()
        offset = content.index('##'.encode('utf-8'))
        f.seek(offset + 2)
        #  creation du nouveau fichier de sortir

        with open('media/decoder.zip', 'wb') as decode:
            out = decode.write(f.read())


def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FilesForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            newdData = FilesForm(request.POST, request.FILES)

            file_to_crypt = form.cleaned_data["name"]
            choice = form.cleaned_data["type_file_id"]
            newdData.save()

            #  ================================

            file = 'media/archive_shutil.zip'
            client = 'media/client'
            out = 'media/out'
            valEncode = chiffre(file, client, out)
            return render(request, 'audio_steg/welcome.html', {'form': form, 'valEncode': valEncode, 'choice': choice})

    # Si on a pas  de data on genere le form
    else:
        form = FilesForm()
    return render(request, 'audio_steg/welcome.html', {'form': form})


def decrypt(request):
    if request.method == 'POST':
        form = DecryptForm(request.POST, request.FILES)
        if form.is_valid():
            newdData = DecryptForm(request.POST, request.FILES)

            file_to_crypt = form.cleaned_data["name"]
            newdData.save()

            #  ================================

            # filecache = 'media/out/' + str(file_to_crypt)
            filecache = 'media/out/image.jpeg'

            dechiffre(filecache)
            fileDecode = 'media/decoder.zip'
            context = {'form': form, 'fileCache': file_to_crypt, 'fileDecode': fileDecode}
            return render(request, 'audio_steg/decrypt.html', context)

        # Si on a pas  de data on genere le form
    else:
        form = DecryptForm()
    return render(request, 'audio_steg/decrypt.html', {'form': form})


def steg_welcome(request):
    return render(request, 'audio_steg/welcome.html')


class StegAudioView(TemplateView):
    template_name = 'audio_steg/audio_input.html'

    def get(self, request):
        form = AudioForm()
        return render(request, self.template_name, {'form': form})

    def PostFile(self, request):
        form = AudioForm(request.POST)

        if form.is_valid():
            # form.save()
            Type = form.cleaned_data.get('stegtype')
            HiddenText = form.cleaned_data.get('hiddentext')
            choice_field = form.cleaned_data.get('choice_field')

            result = 'Invalid Form Input. Try Again!'
            if choice_field == '1':
                result1 = audio_encrypt(HiddenText)
                result2 = music(HiddenText)
                result = {'octalval': result1, 'notes': result2}

            elif choice_field == '2':
                result1 = audio_decrypt(HiddenText)
                result = {'notes': result1}
                print(result1)
        args = {'form': form, 'result': result, 'choice': choice_field}
        return render(request, self.template_name, args)


class StegTextView(TemplateView):
    template_name = 'audio_steg/text_input.html'

    def get(self, request):
        form = TextForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TextForm(request.POST)

        if form.is_valid():
            # form.save()
            Type = form.cleaned_data.get('stegtype')
            PlainText = form.cleaned_data.get('plaintext')
            HiddenText = form.cleaned_data.get('hiddentext')
            choice_field = form.cleaned_data.get('choice_field')
            result = 'Invalid Form Input. Try Again!'
            if choice_field == '1':
                result = text_encrypt(PlainText, HiddenText)

            elif choice_field == '2':
                result = text_decrypt(PlainText)

        args = {'form': form, 'result': result}
        return render(request, self.template_name, args)


class StegImageView(TemplateView):
    template_name = 'audio_steg/image_input.html'

    def get(self, request):
        form = ImageForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ImageForm(request.POST)

        if form.is_valid():
            # form.save()
            Type = form.cleaned_data.get('stegtype')
            PlainText = form.cleaned_data.get('plaintext')
            HiddenText = form.cleaned_data.get('hiddentext')
            result = text_encrypt(PlainText, HiddenText)
        args = {'form': form, 'result': result}
        return render(request, self.template_name, args)


def about(request):
    return render(request, 'audio_steg/about.html', {'title': 'About'})


def encryptresult(request):
    return render(request, 'audio_steg/encryptresult.html')


class HistoryListView(ListView):
    model = PostFile
    template_name = 'audio_steg/history.html'
    context_object_name = 'posts'
    ordering = ['-date']
