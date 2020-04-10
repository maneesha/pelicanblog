---
Title: Bash Terminal Hints
Date: 2020-01-31
Category: Programming
Tags: bash
---

### Find text in a file

```
grep -r "phrase to search" .
```

The `.` (period) at the end says to search the current directory.
The `-r` flag says to search recursively, in the directories inside your current directory.

Other flags include:

* `-l` Display only the filename and path in the results. Otherwise it displays the filename and path along with the target text bounded by a few * characters.
* `-w` Set word boundaries, so it will find only the word surrounded by whitespace. So `grep -r java .` will find `javascript` while `grep -rw java  .` will not.   
* `-n` Displays line numbers of where the search term appears in the document in the results.
* `i` Makes the search case insensitive.
* `-o` Display only the target text in the results.
* `E` Use regular expressions in the search term. This will find the word 'target' and display the 3 characters before it and the 10 characters after it.

```
grep -rnoE '.{0,3}target.{0,10}' . 

```

This will find any lowercase word that starts with b and ends with r:

```
grep -rnoE '.{0,3}\bb[a-z]+r\b.{0,10}' . 

```

* `--exclude-dir=dirA` Excludes directory `dirA` from the recursive search.
* `--exclude-dir={dirA,dirB}` Excludes directories `dirA` and `dirB` from the recursive search. Note it does not work if there's just one directory inside the `{ }`.  It also does not work if you put spaces in between the directory names or around the equal sign.

### Use your terminal's history

```
history
```

will give you a line numbered list of all the commands you have entered for some period of time, dependent on your system's settings.  If you are working in multiple terminal windows, I don't know how to keep track of what's what. 

Each history item comes with a line number.  Enter an exclamation point followed by the line number to immediately run that command again. So for a bash history that looks something like this:

```
128  01/03/20 12:45:52 ls
129  01/03/20 12:45:57 cd my_thesis/
130  01/03/20 12:45:58 ls
131  01/03/20 12:46:02 git status
132  01/03/20 12:46:08 git branch
133  01/03/20 12:46:12 git checkout master
```

line 131 can be run again with:

```
!131
```

On most systems, by default, each command has a line number but does not show when that command was executed.  Add this line to your `.bashrc` file to make each line also have a date time stamp.

```
# Make a datetime stamp show up in history
export HISTTIMEFORMAT="%d/%m/%y %T "

```

You can pipe `grep` into `history` and find all occurences of a given word in your history.

```
history | grep "phrase to search"
```
### Find files

Find files by location, type, and name

```
find ~/path/to/files/  -name "thesis*.*" -type f
```

Find all files (as opposed to directories which would get `-type d` ) in the `~/path/to/files/` directory named `thesis-something`.

Other flags include:

* `-mtime -1` Modified in the last 1 day
* `-mmin -30` Modified in the last 30 minutes
* `-size +1024M` Files over 1 gigabyte in size
* `! -name "*.pdf"` Exclude files with `.pdf` extension
* `-delete` Delete the results. *Do not do this! This is irrecoverable!*


### Navigate around the your current command

If you're typing a long command at your terminal prompt, you may want to easily navigate through the command.

* `ctrl-A`  Goes to start of line
* `ctrl-E`  Goes to end of line
* `alt-F`   Goes forward 1 word   
* `alt-B`   Goes back 1 word
* `ctrl-U`  Deletes from cursor to start of line
* `ctrl-K`  Deletes from cursor to end of line
* `alt-D`   Deletes from cursor to end of word
* `ctrl-XX` Toggle between current cursor position and start of line 

### Scroll through the terminal

In the terminal, hitting up arrow will cycle through your history of commands. So up arrow can't be used to scroll up through the terminal. Instead, you can hit either `shift-PgUp` / `shift-PgDn` to scroll through one screen at a time; or `ctrl-shift-up arrow` / `ctrl-shift-down arrow` to scroll through line by line if you want to keep your hands on the keyboard.
