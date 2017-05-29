Title: About this site
Date: 2013-06-01
Category: Programming
Tags: python, pelican

This website is built in [Pelican](http://docs.getpelican.com/en/3.6.3/index.html), a static site generator built in Python.  This blog post is where I'm storing all my notes on how I built it.  I've backdated it so it always ends up as my earliest post, but I'll continually maintain the post.

I'm running Ubuntu 16.04 and have both Python 2.7 and 3.5 installed on my computer.

I began with creating and starting a virtual environment named pelican3. This virtual environment will automatically be started; otherwise it can be manually started using the workon command.

```
$ mkvirtualenv --python /usr/bin/python3 pelican3
$ workon pelican3
```

and then installing Pelican and Markdown:

```
$ pip install pelican markdown
```
A few other things came with that, so running pip freeze (which sends a list of all installed Python packages to stout) gives me this:

```
blinker==1.4
docutils==0.12
feedgenerator==1.9
Jinja2==2.8
Markdown==2.6.7
MarkupSafe==0.23
pelican==3.6.3
Pygments==2.1.3
python-dateutil==2.5.3
pytz==2016.6.1
six==1.10.0
Unidecode==0.4.19
```

This could be run as 

```
$ pip freeze > requirements.txt
```

which would send that output to a file called requirements.txt.

Next I started my Pelican site:

```
$ pelican quickstart
```

You'll be asked a bunch of questions. You can edit the responses later, some more easily than others.

```
> Where do you want to create your new web site? [.] 
```

This refers to the directory on your own computer where you'll be keeping all your website's files.  The single dot or period refers to the current directory that you're in. If you ran pelican-quickstart from right directory, no need to do anything.  Otherwise you'll need to enter an absolute path to the directory you should be working from.

```
> What will be the title of this web site? 
```

That's what ever you want the title to be like "My Super Cool Blog"

```
> Who will be the author of this web site? 
```

Use your name, a pseudonym, whatever you want.

```
> What will be the default language of this web site? [en] 
```
[en] stands for English but you can find other codes [here](http://www.w3schools.com/tags/ref_language_codes.asp).

```
> Do you want to specify a URL prefix? e.g., http://example.com   (Y/n) 
> What is your URL prefix? (see above example; no trailing slash)
```

It took me a while to figure out what this was for.  It's for when you actually end up hosting your site somewhere, like at http://www.example.com or in my case, http://www.maneeshasane.com.  This is how you tell Pelican what all your URLs will begin with.  Note that the first question just asks if you want to do this; the second question asks for the actual URL.

```
> Do you want to enable article pagination? (Y/n) 
> How many articles per page do you want? [10] 
```

This prevents your blog posts from all appearing on one continous page. You can then specify the number of articles per page.

```
> What is your time zone? [Europe/Paris]
```

Self explanatory.  Use [these timezone values.](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)


```
> Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n) 
> Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n) 
```
I said yes to these although I'm not sure exactly what this is, because that's what was suggested.

```
> Do you want to upload your website using FTP? (y/N) 
> Do you want to upload your website using SSH? (y/N) Y
> What is the hostname of your SSH server? [localhost] ************
> What is the port of your SSH server? [22] 
> What is your username on that server? [root] **********
> Where do you want to put your web site on that server? [/var/www] **********
> Do you want to upload your website using Dropbox? (y/N) n
> Do you want to upload your website using S3? (y/N) n
> Do you want to upload your website using Rackspace Cloud Files? (y/N) n
> Do you want to upload your website using GitHub Pages? (y/N) n
```

I decided to use SSH to upload my site, so I answered no to all the other methods.  The rows of asterisks are where I put in my ssh server name, my user name, and the path to where this site will live on that server.  These things (host, port, username, and path) can all be changed in the Makefile.


I generally used the well written documentation on the Pelican website, but I need to keep a reminder of things that I did to get Pelican working with my situation.  I'm using this blog post as a place to keep these notes up to date and easily accessible.

Pelican content is written in markdown. The default folder is called 'content' but can be called anything. If you keep the default name, build your site like this (run this command from your top level Pelican directory):

```
$ pelican content
```

If you rename it, for example, to 'bucket' then build your site like this:

```
$ pelican bucket
```

This generates the site to the output folder. The files can be viewed at output/index.html, but this way, it can't always locate CSS and other assets.  To really view your site, you need to run a Python webserver.  In Python 3:

```
cd output
python -m http.server
```
and then preview your site [locally](http://localhost:8000).

From there, you can deploy, and the [Pelican docs](http://docs.getpelican.com/en/stable/publish.html#deployment) give some information on how to do so.


However, all this can be done Fabric or Make.  I had trouble getting Fabric to work with Python 3.5 so I used Make. Run this command from your top level Pelican directory.

```
$ make html
```

will generate the html from your markdown (using settings in pelicanconf.py).

```
$ make publish
```

will generate the site for production (using publishconf.py, which imports pelicanconf and adds in or overrides settings for production).

```
$ make serve
```


will serve your site locally.  However, if you make changes to your site while it is running, the server won't refresh. To do that you need to

```
$ make devserver
```

Hit Ctrl-C to terminate the server and type

```
$ ./develop_server.sh stop
```

to kill that process, so the server isn't running in the background preventing other processes from running.


Since I already set up Pelican to use ssh, I can now push my site to my server with

```
$ make rsync_upload 
```

I just needed to enter my password.

I'm a minimalist, so I wanted to keep my site visually simple.  I changed the theme to [bluediea](https://github.com/blueicefield/pelican-blueidea) - it's not much different from Pelican's default theme but has some additional features. I manually edited some of the css to set my own color scheme.

I enabled the ability to search my site by adding 

```
DISPLAY_SEARCH_FORM = True
```

to pelicanconf.py. The code for this is already in base.html.  Note this uses Duck Duck Go as its search engine, and won't work on this site until Duck Duck Go has indexed it, so that could be some time.  Someday I'll use Pelican's [tipue](http://www.tipue.com/search/) search so I'm not dependent on a service like Duck Duck Go or Google indexing my site.

Once I made this site include pages and not just posts, I wanted the pages to display at the top. The theme's documentation makes you think all you have to do is set this in `pelicanconf.py`:

```
DISPLAY_PAGES_ON_MENU = True
```

However that doesn't actually work because there is an improperly capitalized variable name.  

The line 

`{% for pg in PAGES | sort(attribute=PAGES_SORT_ATTRIBUTE) %}`

should acually be 

`{% for pg in pages | sort(attribute=PAGES_SORT_ATTRIBUTE) %}`

This then adds the pages to the same title bar as the categories.  To get the categories to show in a subtitle bar and not the title bar, you need to add this to `pelicanconf.py`:

```
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_SUBMENU = True
```











