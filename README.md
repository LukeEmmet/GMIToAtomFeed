# GMIToAtomFeed

A CGI script to generate an Atom feed for your Gemini log by parsing your gemlog index summary

# GMI based feed generator

The convention for blog/gemlog feeds seems to be Atom+XML, and looking round at the options for generating these there is a python script and writing them by hand.

I'm avoiding installing Python for now on my sparse machine, and the thought of writing Atom XML by hand makes my left eye twitch. 

## Automatic feed generation

I thought it would be nice to write a feed generator that takes as its input a text/gemini file, which is the obvious way authors want to list out and describe their blog posts. The feed generator is automatically up to date as it reads the same human authored list of posts.

Whilst I've written this version in Rebol, actually the script is very simple and could be easily implemented in other languages.

This is all very easy due to the fact that text/gmi is a simple line based format. This fundamental design choice of Gemini is going to prove fruitful for so many light weight parsing situation. Thanks Solderpunk and friends.

## Feed format

The author writes their blog posts in the usual way and creates a link in their blog index underneath their gemini visible folder. This blog index can be linked to from their home page and read by normal human visitors.

The CGI script reads this same blog index file, and parses it as follows

Heading 1 becomes the blog title

```
# My blog title
```

The list of links are scanned, and those that have a display text of the form "date<space>title" are taken as blog entries. Any other links are ignored.

```
=> secondpost.gmi 2020-7-1 My second blog post
=> firstblogpost.gmi 22-Jun-2020 My first blog post
=> ignoreme.gmi This one is ignored as it doesnt start with a date
```

The titles are also normalised/simplified to remove hyphens and underscores, so you can put a natural hyphen between the date and title

```
=> thirdpost.gmi 2/7/2020 - A third post, hyphen will be removed
```

The date format is fairly flexible and anything that passes the Rebol string to date function will be fine.

The final url is assembled by appending the link target onto the blog base url.

All other lines are ignored in building the feed.

## Per-user feeds

The design allows for many users on the same machine to make use of the feed. In the script there is a list of known users, which allows each of them to have their own gemlog file and base url and timezone.

```
;---extend as necessary with other users
users: context [
    lukee: context [
        gemlog-path: %/var/gemini/blog/index.gmi
        base-url: "gemini://gemini.marmaladefoo.com/blog/"
        author-name: "Luke Emmet"
        author-email: "luke@marmaladefoo.com"
        timezone: "Z"
    ]
]
```

Then the username is passed to the CGI script to generate the feed for that user:

```
=> gemini://domain/cgi-bin/atom-feed.cgi?lukee Atom feed for lukee
=> gemini://domain/cgi-bin/atom-feed.cgi?username2 Atom feed for username2
... and so on
```

And the resultant url submitted to Capcom or linked from the users blog page.

Alternatively the script could be extended to programmatically look up this information if there is a common layout and convention on the machine.

## Example

This site, Marmaladefoo, uses this script for its feed generator:

=> gemini://gemini.marmaladefoo.com/blog/index.gmi Human readable blog index (GMI)
=> gemini://gemini.marmaladefoo.com/cgi-bin/atom-feed.cgi?lukee Generated Atom feed

## Installation/Source

You will need Rebol on your machine, and a CGI compatible Gemini server.