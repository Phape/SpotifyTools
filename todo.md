# Further Course of this Project

## todo's

## fixme's

* if the user had turned on auto refresh and turned it off again, then reloads the page, the form is submitted again and auto refresh is active again --> it should be off
* When making too many requests to spotify, it gives a timeout --> Handle the timeout
* Make the transitions of the list items in a ranking work every time, not only when hard-reloading

## ideas

* possibility to display song lyrics (good api for that?)
* Use the Spotify API endpoint "Get User's Followed Artists" to find out which genres the user might like
  * Same thing can be done with this endpoint: "Get a User's Top Artists and Tracks"
* Use Spotify search API to display top songs of a genre on the website
* deactivate auto refresh if the user switches the tab
  * activate auto refresh again if user comes back to the tab

## third party issues

### issue with spotify links

At the moment, there is no solution to create a genre link to spotify that works on all three major platforms.
Best case would be:

* Spotify app opens on all platforms when clicking the link (instead of a browser tab)
* Spotify displays tracks for a genre (instead of tracks and artists)

There are two possibilities for a link to Spotify:

* The URI: eg. <spotify:search:genre:pop> (Deeplink)
* The URL: eg. open.spotify.com/search/genre:pop (Universial Link)

You can try reproducing the error yourself. For best result, view this file in your browser and click the two links above.

When using Spotify Web, even this link should work: open.spotify.com/search/genre:pop:tracks

Here is a table that shows which links work on which devices:

| Link Example                             |  iOS Spotify App   | Android Spotify App | Win10 Spotify App  | Win10 Spotify Web  |
| ---------------------------------------- | :----------------: | :-----------------: | :----------------: | :----------------: |
| <spotify:search:Drake>                   | :heavy_check_mark: | :heavy_check_mark:  | :heavy_check_mark: |   :interrobang:    |
| <spotify:search:genre:pop>               |        :x:         |         :x:         | :heavy_check_mark: |   :interrobang:    |
| open.spotify.com/search/genre:pop        | :heavy_check_mark: |         :x:         |        :x:         | :heavy_check_mark: |
| open.spotify.com/search/genre:pop/tracks |        :x:         |         :x:         |        :x:         | :heavy_check_mark: |

The solution I would choose is the second row of the link examples. Sadly, it doesn't seem to work on mobile devices yet.
