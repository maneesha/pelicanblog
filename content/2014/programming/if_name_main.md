Title: If __name__ == __main__
Date: 2014-07-01
Category: Programming
Tags: Python

When you work in python, you’ll see this if `__name__ = '__main__'` all over the place. It took me forever to really understand what it means. Actually, I still often have to think through each time I see or use it (but I don’t really use it myself).

I recently taught an intro to Python workshop and talked about this with my co-instructors. We found some good explanations on line. This is my shot at explaining things in a way that makes sense to me. Hopefully it’ll help other people too.

`if __name__ == "__main__"` is what runs when the script is run from the command line using a command like `python myscript.py` — as opposed to being imported. So the code in that `if` block will run when the program is being run directly. If the program is imported, then other parts of the code will run but this block won’t. So you can have a script with a bunch of function definitions which then run only inside this `if` block. Then if you want to import the functions into another script, you can do so without the part of the script that make them run.

Some links for more clarification:

http://stackoverflow.com/questions/419163/what-does-if-name-main-do

http://docs.python.org/2/tutorial/modules.html

http://effbot.org/pyfaq/tutor-what-is-if-name-main-for.htm
