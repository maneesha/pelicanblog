Title: Looping through Python command line arguments
Date: 2017-02-20
Category: Programming
Tags: shell, bash, python

I have a Python script that does some image manipulation and outputs a new file. From the command line, it takes two arguments, the old file and new file:

```
python image_converter.py oldfile.jpg newfile.jpg
```

I wanted to run this over a bunch of files, and used this bash script to loop over the files.  This let me go over every file, and create a new file with 'new' prepended to the file name.

```
for f in *.jpg
do
python image_converter.py $f "new_$f"
done
```

I now had bunch of files, 'img1.jpg', 'img2.jpg', with their modified counterparts, 'new_img1.jpg', 'new_img2.jpg', and so on.  I used this script to drop the first four characters from the new file name.  Note this requires being in another directory; otherwise the new-new names just end up being the old ones.

Renaming files
```
for f in *.*
do
mv $f "${f:3}"
done
```





