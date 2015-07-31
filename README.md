# FaKe - Facebook data marKet
Created by Seyoung Park(seyoung.park@aalto.fi) @ 2015.June.29th.:tada:


## Motivation
I interned at [e4net](http://www.e4net.net/) for one month in 2015 July. There I was assigned to build a Django app and present them. It was to teach myself about web framework and show them about Django.


## What is FaKe?
The application is about a web store. My web store is called FaKe. FaKe stands for “Facebook big data marKet”. Facebook has billions of users and many people can’t survive a day without using it. That enables Facebook to collect and parse tremendously huge amount of private data about their customers every-second life. Facebook is “free” but we all know where they get the cash from: the data. They sell the data they collect to relevant advertisers. We all know that these things happen but still we don’t really know how this kind of business works and what kind of data is available and sold. It’s very sensitive but also undeniably interesting. FaKe demonstrates an open market for Facebook user data. Facebook administrators can register data products and advertisers can shop them.


## Is it real?
The application is called **FaKe**. Indeed it is. This is just for fun :)

## State
The app misses vast amount of features to be called as a web store. The store page lacks proper searching, you cannot pay and you cannot retrieve your forgotten account. I've spent only 12 days for this project so please don't expect too much. However, I've put quite much effort on authentication and authorization part and anyone can get even tiny benefit from it.

## Environment
Mac OS X 10.10.4 (Actually this shouldn't matter in anycase.)
Python 2.7.9
Django 1.8.2

## Tests
1. To start a server
```
# /tango_extended/
python manage.py runserver
```
Then open your browser and go to http://127.0.0.1:8000/rango/ .
Yes, I haven't worked out with the url and this
project is extended from [Tango with Django](http://www.tangowithdjango.com/)"

2. To work in the shell to play with DB.
```
# /tango_extended/
python manage.py shell
```

3. To create a superuser
```
# /tango_extended/
python manage.py createsuperuser
```

4. To view Django admin page
Go to http://127.0.0.1:8000/admin/

## Presentation
Check out my [slide presentation](https://drive.google.com/open?id=13GfhisjNddkNsGmjFB-jID53FthjIqkK-8-RFHDJVf4)

## Tips
When you edit views.py or some Python scripts, the local server might not be able to update it quick enough. In such case, restart the server.

## License
MIT
