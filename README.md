Scapelist
======

Source code of [Scapelist](https://www.hackerleague.org/hackathons/midem-music-hack-day-2014/hacks/scapelist), a hack developed at the [MIDEM Music Hack Day 2014](http://new.musichackday.org/2014/cannes/)

How does a landscape sound like?

You take a picture of, let's say, the Grand Canyon in Colorado, a la Instagram, but you also want to attach a song to it, a song that makes sense to you while you were taking that picture.

Now imagine that other people went to the same place, took another picture of it but picked a different song.

You end up with a playlist of songs related to that landscape, a ScapeList, curated by the users themselves, which you can listen to.

![Screenshot](http://s27.postimg.org/5bkyw205v/screenshot1.png "Screenshot")

Install Dependencies
------

(preferably in a virtualenv)

* Linux Ubuntu:
  * sudo apt-get install libmysqlclient-de
  * pip install -r requirements

* Mac OS X:
  * export PATH=$PATH:/usr/local/mysql/bin
  * pip install -r requirements
  
You need an API key for both [Instagram](http://instagram.com/developer/) and [Echonest](https://developer.echonest.com/account/register)
Once you get these API keys, replace the text in *scape/views.py*s

Create database
------

In MySQL run:
* CREATE DATABASE database_name CHARACTER SET utf8 COLLATE utf8_general_ci;
  your user should have granted privileges to database_name

Create tables
------

* Edit django settings (located at *scapelist/settings.py*): change the database name, user name and user password accordingly
* Run: 'python manage.py syncdb'

Run local server
------

* Run: 'fab up'
* Open a browser and load 'http://0.0.0.0:8007' (default url, if you want to change it edit *fabfile.py*)

