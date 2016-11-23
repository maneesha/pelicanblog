Title: Django Databases and Date Ranges
Date: 2016-11-13
Category: Programming
Tags: python, django


I'm continuing to work on my project analyzing data about Philadelphia City Council - elections, demographics, terms of service, etc., even as heartbroken and terrified I am about the recent Presidential election.  A very crude version of this project is [here](http://phlcitycouncil.pythonanywhere.com/).  A big thing that this never did was to look at the progression from being a candidate to being an elected council member, with distinct start and end dates.  Now that I'm doing this, I need to be able to record each term for each Councilmember, ensuring there are no overlaps.  This means a single Councilmember can not be in more than one office at any time, and a single office can not be held by more than one Councilmember at any time.

This means that I need to test for date ranges.  [I posed the question on Reddit](https://www.reddit.com/r/learnpython/comments/5cgavm/django_model_prevent_overlapping_dates/) (because I thought Reddit responders were a bit gentler than Stack Overflow responders; that's not always the case).  The algorithm to test for overlapping dates seemed straightforward enough - although [another Reddit post](https://www.reddit.com/r/django/comments/2ckxdy/dealing_with_start_and_end_date_fields/) helped me figure out just how to write it.  

I then needed help understanding where and when to call it. My question on Reddit included a response telling me about the clean() method and about ValidationError. I learned that [the save() method can be overwritten to include error handling](https://docs.djangoproject.com/en/1.10/ref/models/instances/#django.db.models.Model.save).

I still need to work on understanding error handling.  A few posts I started reading to help:

* Stack Overflow: [Manually raising (throwing) an exception in Python](http://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python?rq=1) 
* Stack Overflow: [ValidationError in Django](http://stackoverflow.com/questions/8557885/validationerror-in-django)

As I started to work on writing all of this, I happened to sit in on a BarCamp Philly session about data modeling, in which the speaker specifically addressed the challenge of conflicts in date ranges. Since his talk was in a language I don't know, I paid attention to the general content but not specific syntax and such of his presentation.  Instead, I continued googling my question about handling overlapping date ranges in Django.  I discovered that [Django supports the daterange field in Postgres](https://docs.djangoproject.com/en/1.10/ref/contrib/postgres/fields/#daterangefield).  My project is using sqlite as the database engine.  I realized I had two options -- setting up Postgres and moving my database there to take advantage of the daterange type, or writing all the code to do this validation and keep my database in sqlite, which needs no setup.  I decided writing code was easier than setting up a database server and migrating my entire database. It is pretty cool, though, how much I learned just from my initial question about managing overlapping date ranges.
