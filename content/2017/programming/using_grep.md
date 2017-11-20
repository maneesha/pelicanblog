Title: Using grep
Date: 2017-11-19
Category: Programming
Tags: shell, bash


`grep` is a bash program that searches files for lines containing a match to a given pattern.

Without any special tricks, it's used like this.  This will search for the pattern `string` inside the file `file.txt`.  Each line that matches is displayed entirely.

```
grep 'string' file.txt
```

This can take a few flags.  The `-E` flag tells `grep` to treat the string like a regular expression.  The numbers in curly braces mean to take one character before and four characters after the string.

```
grep -E '.{0,1}string.{0,4}' file.txt
```

The `-o` flag prints only the matching part of the line.

```
grep -oE '.{0,1}string.{0,4}' file.txt
```

The `-n` flag prints line numbers.

```
grep -oEn '.{0,1}string.{0,4}' file.txt
```


The `-m` flag suppresses output to the maximum number of occurences.  The following command will display only 5 occurences.  The `-m` flag must be the last one in the chain of flags or must stand alone before or after the other flags.

```
grep -oEnm 5 '.{0,1}string.{0,4}' file.txt
```

```
grep -m 5 -oEn '.{0,1}string.{0,4}' file.txt
```

The `-i` flag performs a case insensitive search.

```
grep -m 5 -oEni '.{0,1}string.{0,4}' file.txt
```

`grep` can handle multiple files.  In this example, the first five occurences in each `json` file will be displayed.

```
grep -onE -m 5 ".{0,3}scraped.{0,40}" *.json
```


Parts of a file, such as the output of `tail` can be passed to `grep` to search just 

```
tail -20 file.txt | grep  -E '.{0,3}string.{0,40}'
```


The deeper I get into `grep`, the less I ever want to use `Ctrl-F` in a file editor again.  Check out [Software Carpentry's shell lessons](http://swcarpentry.github.io/shell-novice/) to learn more.  I also like this [cheat sheet](https://www.computerhope.com/unix/ugrep.htm) for quick reference.