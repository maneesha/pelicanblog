---
Title: Sublime Hints
Date: 2020-02-15
Category: Programming
Tags: sublime
---

## Tips for using sublime

#### Selecting text 

* `ctrl-D` to select a word. Continue hitting `ctrl-D` to select subsequent instances of that word.
* `ctrl-L` to select a line.
* `ctrl-A` to select the entire document.
* `ctrl-shift-M` to select something inside a set of brackets
* `ctrl-shift-up_arrow` to move the current line up one (and likewise with down arrow)

#### Multicursor

If you want to add or remove characters from the beginning or end of a selection of lines from your document:

1. Go to the first line of your selection, and hit `ctrl-L` to select that line
1. Continue hitting `ctrl-L` until every line you want has been selected.
1. Hit `ctrl-shift-L` and your selection will remain, with a cursor at the end of each line.
1. Use your keyboard's arrow keys to move the cursor. This will give you a cursor at the same position on each line, relative to the beginning or end of the line.  
1. Type whatever you wanted to in, and it will repeat on every line.
1. `esc` to get your single cursor back

#### Open from terminal

If you are in a bash terminal and want to open that directory in sublime:

```
subl .
``` 
The `.` (period) is short hand for the current directory.

Any directory can be opened in this way.

```
subl ~/path/to/my/directory
```

