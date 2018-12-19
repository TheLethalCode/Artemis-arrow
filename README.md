# Artemis-arrow

Tired of looking in different places for a variety of different entertainment? Yep, we have been there, done that! That's why, we introduce you to Artemis Arrow. Artemis is the Greek goddess of hunt. There has never been a history of her arrow ever missing. Anything you need, Artemiss' arrow will race towards it in the humongous hub (i.e internet) and bring it to you without fail. 

## Planned Features(Under Development)

### Primary Features
  - Download songs, anime, book
  - Upload them to Google Drive if necessary

### Miscellaneous Features
  - Add the song to youtube playlist
  - Add anime to myanime watch list
  - Add books to goodreads readlist
  
## Contributing

THE PRIMARY DEVELOPMENT BRANCH IS "devel". Fork this repo and send all further pull requests to this branch.

This project is in its early stage, so all contributions are welcome. The app's features and functionalities have been elaborated below. Choose a certain feature, and work on it. Test it locally before sending a PR.

TIP:- It would be better if you work under a virtual environment in python :) . 

### Frontend

Since this is a webapp, we will be needing a front end for it. The design is upto you, the primary functionalities that it should have are:-
  - Provide choice between, anime, books, or songs (Buttons would be preferrable, but not a necessity).
  - Provide an option for uploading the downloaded content to drive or not after the first step.
  - A search box for searching the desired content after the above steps.
  - After the search, confirm the searched result before downloading.
  - Provide the download link.

### Backend

This app uses flask library to use as the primary web framework in our application and the request library for amassing the content to be downloaded.

#### Songs

We will be using the Youtube REST API, for querying the song data, through which we will be able to get the url for the youtube video of the song. Then we will use youtube_dl to download the song in audio format. For now, we wouldn't be using OAuth, but later on we will be integrating it to add the songs to the youtube playlist.

#### Books

We will be mostly using ["Library Genesis"](https://libgen.is/) (a website for all book contents) for downloading all the books. For additional features,we will be using GoodReads API to add the books to the favourite list.

#### Anime

The primary website where download of anime seems feasible is [KissAnime](http://kissanime.ru/) (if you find any other place, please inform me XD). So we will be using the kissanime.ru (rapidvideo server is the most easiet, but not foolproof) website for downloading any anime. As an additional feature, we will be adding the downloaded anime to [MAL](https://myanimelist.net/) watch list.

