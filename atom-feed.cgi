#!/usr/local/bin/rebol -cs

REBOL [
    author: "Luke Emmet"
    email: "luke [at] marmaladefoo [dot] com"
    title: "GMI to Atom generator"
    description: {
        
        A converter from GMI gemlog entries to Atom XML format
        
        It expects the user to be passed on the querystring like this: feed.cgi?lukee or similar"
    
        This script reads a GMI file for the user, gets the feed title from last h1 on the page, parses
        links having the format:
        
        => <relativepath.gmi> <date> <title>
        
        REBOL is tolerant of various date formats, can be given in at least the following forms
        1-Jul-2020
        2020-7-1
        1/7/2020
        
        link lines that do not match the pattern are ignored, are other lines in the file
        
        The emitted content is Atom/XML
    }
    
]


users: context [
    lukee: context [
        gemlog-path: %/var/gemini/blog/index.gmi
        base-url: "gemini://gemini.marmaladefoo.com/blog/"
        author-name: "Luke Emmet"
        author-email: "luke@marmaladefoo.com"
        timezone: "Z"
    ]
]


default-user: "lukee"       ;if none provided

this-url: "gemini://gemini.marmaladefoo.com/cgi-bin/atom-feed.cgi"




;___________no need to change below here____________

prin rejoin ["20 application/atom+xml" crlf]
username: any [(get-env "QUERY_STRING") ""]
if username = "" [username: default-user]
user: get in users to-word  username
last-updated: 1-Jan-1970


markup-escape: funct [input] [
    data: copy input
    replace/all data "&" "&amp;"
    replace/all data "<" "&lt;"
    replace/all data ">" "&gt;"
    replace/all data {"} "&quot;"
    :data
]

feed-title: join "Atom feed for " user/author-name

posts: []
post: make object! [
    title: "New post"
    link: ""
    updated: ""
]

date-to-rfc3339: funct [date timezone] [
    ;simplistic but OK
    rejoin [
        date/year "-" 
        (either date/month <  10 [join "0" date/month] [date/month]) "-" 
        (either date/day <  10 [join "0" date/day] [date/day]) 
        "T" 
        "00:00:00"  ; date/hour ":" date/minutes ":" date/seconds
        timezone
    ]
]

title-case: funct [text] [
   join (uppercase first text) (next text)
]


foreach line read/lines user/gemlog-path [    
    words: parse/all line " "
    
    
    if words/1 = "#"  [feed-title: trim next line]
    
    if words/1 = "=>" [
        link: words/2
        text: reform next next words
        
        
        if (parse text [copy date-part to " " thru " " copy title to end]) [
                
            attempt [
                post-date: to-date date-part
                            
                new-post: make post []
                
                new-post/title:   title-case trim reform parse/all title " _-"
                new-post/link: join user/base-url link
                new-post/updated:  date-to-rfc3339 post-date user/timezone
                
                if post-date > last-updated [last-updated: post-date]   ;assumes at least one valid entry!
                append/only posts new-post
                
            ]
            
        ]
    ]
    
]

print rejoin [

{<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

    <id>} user/base-url {</id>
    <title>} (markup-escape feed-title) {</title>
    <updated>} (date-to-rfc3339 last-updated user/timezone) {</updated>
    <link href="}  this-url {?} username {" rel="self"/>  
    <author>
        <name>} (markup-escape user/author-name) {</name>
        <email>} (markup-escape user/author-email) {</email>
    </author>
}

]
foreach post posts [
    print rejoin [
    {
    <entry>
        <title>} (markup-escape post/title) {</title>
        <link href="} post/link {"></link>
        <id>} post/link {</id>
        <updated>} post/updated {</updated>
    </entry>}
    ]
]


print "</feed>"



