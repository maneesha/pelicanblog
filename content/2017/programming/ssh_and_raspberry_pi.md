Title: ssh and Raspberry Pi
Date: 2017-06-22
Category: Programming
Tags: raspberrypi

Many years ago I got an early version of the Raspberry Pi.  I fiddled with it a bit but didn't do much with it.  A few months ago I decided to buy a newer version to have a mini computer I could use for a specific web scraping project I was running.  I have a cron job that runs a Python script every minute and saves the results to a file, all on the Raspberry Pi.

Recently I realized I don't have to connect the Raspberry Pi to a monitor, mouse, and keyboard to check on the status of my scraper.  Raspberry Pi has built in `ssh` access.  To summarize what's [currently in their documentation](https://www.raspberrypi.org/documentation/remote-access/ssh/)

* Enable ssh access in the Raspberry Pi Configuration option from the Preferences Menu
* At the Raspberry Pi terminal, type `hostname -i` to get the Raspberry Pi's IP address
* At your local computer's Linux terminal type in `ssh pi@<that-ip-address`.  For example, `ssh pi@192.168.0.0`
* Type `yes` for the security/authenticity warning
* Enter your Raspberry Pi password when prompted*
* Now you'll be at the Raspberri Pi command line prompt

This makes it easy to copy files from the Raspberry Pi to the local machine.

To copy the file `f.txt` from the Raspberry Pi to your local machine, use the `scp` command.  Use the same user and address as ssh above followed by a colon and the full path to the file to note the source file. Add a space separator, and then note the local destination path. You'll be asked for your password as above.

```
scp pi@192.168.0.0:/home/pi/f.txt /home/maneesha/Documents

```

You can [set up public/private keys](https://help.ubuntu.com/community/SSH/OpenSSH/Keys) so you don't need to enter a password each time -- that's a topic for another post. I've written the above in the context of working with Raspberry Pi but it can apply to any server you have ssh access to.

*The Raspberry Pi ships with a default username `pi` and password `raspberry` -- change this!
