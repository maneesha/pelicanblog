Title: Making files by the batch
Date: 2017-02-13
Category: Programming
Tags: shell, bash


I had a list of names and I wanted to create an empty file with each of those names.

First I saved my list of names to a file with the .md extension since they were all going to be markdown files.

names.txt
```
barack.md
joe.md
hillary.md
bernie.md
```

Then I wanted to loop through the list of names, and create a file with each name.  I tried writing a loop like this. It works for echo but I could not figure out why touch did not work.

This works:
```
while read NAME; 
do 
echo "$NAME"; 
done < names.txt
```

This does not:
```
while read NAME; 
do 
touch "$NAME"; 
done < names.txt
```

Some Googling led me to find I didn't need to write a loop.  I could just pipe the file to `xargs touch`:

```
cat names.txt | xargs touch
```

I now had empty files named for each item in my names.txt file.





























