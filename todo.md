# Further Course of this Project

## todo's

* Space between artist cards
* Only one artist card per row on mobile devices
* Spotify and Wiki icons should be floating right for genres

## fixme's

## ideas

* A white animated bar below the navi-bar that indicates when the site will refresh next
  * to replace the text "This site refreshes every x seconds."
* possibility to display song lyrics (good api for that?)

## third party issues

At the moment, there is no solution to create a genre link to spotify that works on all three major platforms.
Best case would be:

* Spotify app opens on all platforms when clicking the link (instead of a browser tab)
* Spotify displays tracks for a genre (instead of tracks and artists)

There are two possibilities for a link to Spotify:

* The URI: eg. <spotify:search:genre:pop>
* The URL: eg. open.spotify.com/search/genre:pop

You can try reproducing the error yourself. For best result, view this file in your browser and click the two links above.

When using Spotify Web, even this link should work: open.spotify.com/search/genre:pop:tracks

Here is a table that shows which links work on which devices:

| Link Example                             |  iOS Spotify App   | Android Spotify App | Win10 Spotify App  | Win10 Spotify Web  |
| ---------------------------------------- | :----------------: | :-----------------: | :----------------: | :----------------: |
| <spotify:search:Drake>                   | :heavy_check_mark: |    :interrobang:    | :heavy_check_mark: |   :interrobang:    |
| <spotify:search:genre:pop>               |        :x:         |         :x:         | :heavy_check_mark: |   :interrobang:    |
| open.spotify.com/search/genre:pop        | :heavy_check_mark: |         :x:         |        :x:         | :heavy_check_mark: |
| open.spotify.com/search/genre:pop/tracks |        :x:         |         :x:         |        :x:         | :heavy_check_mark  |

The solution I would choose is the second row of the link examples. Sadly, it doesn't seem to work on mobile devices yet.
