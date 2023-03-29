#!/usr/bin/env python3

import os
import shutil
from tkinter import Tk, filedialog
import requests
from PIL import Image, ImageOps
from tqdm import tqdm
from imdb import Cinemagoer
import questionary

banner = (r'''

██████╗  ██████╗ ███████╗████████╗███████╗██████╗ ██████╗ ██╗   ██╗
██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝
██████╔╝██║   ██║███████╗   ██║   █████╗  ██████╔╝██████╔╝ ╚████╔╝ 
██╔═══╝ ██║   ██║╚════██║   ██║   ██╔══╝  ██╔══██╗██╔═══╝   ╚██╔╝  
██║     ╚██████╔╝███████║   ██║   ███████╗██║  ██║██║        ██║   
╚═╝      ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝   
                                                                      
                                                                                    
                                            
''')

print(banner)

def api_key():

    SAMPLE_URL = 'https://api.themoviedb.org/3/movie/76341?api_key={0}'
    try:
        while True:
            if os.path.exists("api.txt") and os.path.getsize("api.txt") > 0:
                f = open("api.txt", "r")
                key = f.read()
                req = requests.get(SAMPLE_URL.format(key))
                if req.status_code == 200:
                    print("\nAPI Key authentication successful.\n")
                    return key
                else:
                    pass

            print("\nTo register for an API key, Visit: https://www.themoviedb.org/account/signup")
            get_key = input("API key required. Please enter the API key: ")
            req = requests.get(SAMPLE_URL.format(get_key))
            if req.status_code == 200:
                f = open("api.txt", "w")
                f.write(get_key)
                f.close()
            else:
                print("\nInvalid API key: You must be granted a valid key.")
    except OSError:
        print("\nUnknown Error")

def search_movie():

    try:
        ia = Cinemagoer()
        user_input = input("Search for a movie: ")
        print("\n", end="")
        movies = ia.search_movie(user_input)

        choices_list = []

        for i in movies:
            get_title = i['title']
            get_id = i.movieID
            try:
                get_year = i['year']
            except KeyError:
                pass
            p = ("{: <10}".format(str(get_id))+ get_title + " " + "(" + str(get_year) + ")")
            choices_list.append(p)

        movie_list = questionary.select("Oh! there's alot. What did you mean? ", choices=choices_list).ask()
        get_id = movie_list.split()
        IMDB_ID = get_id[0]

        return IMDB_ID

    except KeyboardInterrupt:
        print("\nKeyboard Interrupted")
        quit()
    except AttributeError:
        quit()
    except ValueError:
        print("\nUnknown movie name.")
        quit()

def get_image_url():

    for k, v in req.items():
        for i in v:
            for k, v in i.items():
                if k == 'poster_path':
                    image_url = 'http://image.tmdb.org/t/p/w500/' + v
                    return [image_url, v]
                # if i['poster_path'] is None:
                #     print("No Poster Found")
                #     quit()

URL = 'https://api.themoviedb.org/3/find/tt{0}?api_key={1}&language=en-US&external_source=imdb_id'.format(search_movie(), api_key())

req = requests.get(URL).json()

def download_poster():

    if get_image_url() is None:
        print("\nNo poster found")
        quit()
    else:
        returning_list = get_image_url()
        url = returning_list[0]
        filename = returning_list[1]
        _response = requests.get(url).content
        file_size_request = requests.get(url, stream=True)
        file_size = int(file_size_request.headers['Content-Length'])
        block_size = 1024
        t = tqdm(total=file_size, unit='B', unit_scale=True, desc="Downloading", ascii=True)
        with open(filename[1:], 'wb') as f:
            for data in file_size_request.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        print("\nPoster downloaded successfully\n")
        return os.getcwd() + filename

def convert():

    # this discussion helped me a lot: https://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent

    icon = os.getcwd() + "\\poster.ico"
    img = Image.open(download_poster())
    img = ImageOps.expand(img, (69, 0, 69, 0), fill=0)
    img = ImageOps.fit(img, (300, 300)).convert("RGBA")

    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(icon)
    img.close()
    print("Poster icon created successfully.")
    return icon


def tk_get_file_path():

    try:
        root = Tk()
        root.withdraw()
        file_path = filedialog.askdirectory(parent=root, title='Select folder')
        if file_path:
            return file_path
        else:
            print("\nCancelled")
            quit()
    except IOError:
        print("\nError Occurred.")
        quit()


def change_folder_icon():

    get_folder = tk_get_file_path()
    get_poster_icon = convert()

    if os.path.isfile(get_folder + "\\poster.ico"):
        print('\nAn icon is already present. Delete the older icon before applying a new icon.')
        quit()
    else:
        icon_to_folder = shutil.move(get_poster_icon, get_folder)

    if os.path.isfile(get_folder + "\\desktop.ini"):
        print('\nA desktop.ini file is already present. Delete the older one before applying a new one.')
    else:
        with open(get_folder + "\\desktop.ini", "w+") as f:
            f.write("[.ShellClassInfo]\n")
            f.write("IconResource=poster.ico,0")

        os.system('attrib +r \"{}\"'.format(get_folder))
        os.system('attrib +h \"{}\\desktop.ini\"'.format(get_folder))

        print("Folder icon changed successfully.")


change_folder_icon()
