Title: Jupyter Notebook and the Django shell
Date: 2016-11-04
Category: Programming
Tags: python, django

I've been working on a project analyzing data about Philadelphia City Council - elections, demographics, terms of service, etc.  A very crude version of this project is [here](http://phlcitycouncil.pythonanywhere.com/).  I want to make this more robust, and a big part of doing so includes playing with code.  One of my favorite ways to play with Python code is using the Jupyter Notebook.  It's an interactive brower based platform where I can run snippets of code, view the results, and easily edit and re-run things until I get what I'm looking for.

Today I discovered the [shell-plus Django extension](http://django-extensions.readthedocs.io/en/latest/shell_plus.html), which lets you run Django shell in various interactive Python shells.

Like most Python packages, it can be installed with pip.

```
$ pip install django-extensions
```

The module then needs to be added to the INSTALLED_APPS in your settings.py file:

```
INSTALLED_APPS = (
    ...
    'django_extensions',
)
```

While I typically start a new Jupyter notebook like this:

```
$ jupyter notebook
```

to start it with the Django shell, I need to start it like this:

```
$ python manage.py shell_plus --notebook
```

Now when I create a new notebook, I can choose between a standard Python 3 notebook or a Django Shell Plus notebook.  Then I can import Django, import my modules, and anything else I need, and work on my Django project.

Note that if I start a notebook the typical way, I still have the option to open a Django Shell Plus notebook, but it does not actually run as such.  I need to run the notebook using the special command above.  



