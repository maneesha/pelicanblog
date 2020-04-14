---
Title: Git log cheat sheet
Date: 2020-04-14
Category: Programming
Tags: git
---

`git log` is an excellent command to view the history of commits in your project.  There are a number of flags it can take to customize the output.  These are some of my favorites.


```
git log
```
Returns the entire history of the current branch of your project 

<hr>

```
git log --oneline
```
Condensed view of git log. Displays only a truncated commit hash and the commit message.
<hr>

```
git log -4
```
Shows just the last 4 commits

<hr>
```
git log -name-status
```

Shows the files that were changed in each commit
<hr>

```
git log -p
```

Shows the file diff in the log output
<hr>
```
git log --after="2019-07-01" --before="2019-09-30"
```

Shows commits in a date range
<hr>
```
git log --grep="cookie"
```

Shows commits where commit message contains a term
<hr>

```
git log -- config.py
```

Shows commits just for a given file
<hr>

```
git log -S"cookie"

# OR 

git log -G"\bc[a-z]*ie\b"

```

Shows commits where that term was added to a file.  -S flag for text search; -G for regex search