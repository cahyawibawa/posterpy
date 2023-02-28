# PosterPy

This is a python script that helps you to search, download movie posters and set them as folder icons. PosterPy uses the popular [IMDbPY](https://imdbpy.github.io/) package to search movies and [TMDb](https://www.themoviedb.org/) API to download movie posters.

![posterpy](https://user-images.githubusercontent.com/62229971/221837376-d4075c72-a4c8-4fa5-a911-fccc5b41b51c.png)

## For Your Attention

- Your PC may take some time to index the newly added icons. If the icons doesn't appear after 3 - 5 minutes try clearing and resetting thumbnail cache of our PC. [Here](https://www.sevenforums.com/tutorials/10797-thumbnail-cache-clear-reset.html) is a article on how to clear and reset thumbnail cache in Windows.

- Since PosterPy is using the TMDb API to download movie posters you need to have a TMDb API key in order to use this script. To register for an API key click [here](https://www.themoviedb.org/account/signup). Once you register an account [this](https://developers.themoviedb.org/3/getting-started/introduction) will help you to request and find your API key. (This is an one time process. Once you obatin your API key you need to enter it to the script when it ask for the key and that's it.)

## I don't like these icons. How do i remove them?

To remove the poster icon from a folder, just delete the .ico and desktop.ini file from the folder. desktop.ini file is hidden by default. Therefore make sure you have **Show Hidden Items** option ticked.

## Git Installation

```
# clone the repo
$ git clone https://github.com/sameera-madushan/PosterPy.git

# change the working directory to PosterPy
$ cd PosterPy

# install the requirements
$ pip3 install -r requirements.txt
$ python -m pip install IMDbPY


```

## Usage

```
python posterpy.py
```
