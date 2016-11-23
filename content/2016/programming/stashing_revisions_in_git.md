Title: Stashing revisions in Git
Date: 2016-11-13
Category: Programming
Tags: git



Sometimes I'll be working on a project, having moved along a few steps from my last commit, only to remember there was something else I wnated to do before the point I'm at now.  Since the point I'm at now isn't really ready for a commit, I don't want to make a sloppy commit, but I don't want to lose the bit of work I've done so far.  That's what git stash is for.  This returns me to the state of my last commit, setting aside the work that I've been doing.  I can re-apply the stashed work later.  There may be the same kinds of  conflicts you'd expect with merges, but you don't have to make an unnecessary, messy commit, and you won't lose any of your work.  Here's how it goes:


```
$ git stash

```

This should return output telling you you're back at your last commit.  Now you can do any work you want, and add and commit as normal.  

When you're ready to add your stashed work back, type 

```
$ git stash pop

```

This applies those stashed changes to your new, latest commit.  Merge conflicts, if any, are denoted with a series of pointy braces like usual.  Fix and commit those, and you're back on track.  

