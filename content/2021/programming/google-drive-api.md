---
Title: Google Drive API
Date: 2021-04-01
Category: Programming
Tags: google drive, api, python
---

# What I was doing

End goal is to take many files that were owned by bob@gmail.com and change ownership to be bob@example.com.  Bob's not super proficient in working with Python or using APIs, but this isn't entirely new to him either. 

# Set up Google API 

https://developers.google.com/drive/api/v3/quickstart/python

When asked to select a google account, be sure to select the one that you want to move the ownership from (bob@gmail.com).
https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the

Install the Google Client Library.  Ideally do this in some sort of virtual environment.
https://developers.google.com/drive/api/v3/quickstart/python#step_2_install_the_google_client_library



# Set up service credentials 

Scopes here are just read-only
https://developers.google.com/drive/api/v3/quickstart/python#step_3_set_up_the_sample

Here are all the scopes that are available.
https://developers.google.com/drive/api/v2/about-auth#OAuth2Authorizing

# Make sure it's you

This code will show you information about yourself. You should see your name, email, and other information listed.

# Get all files in the google drive

This returns all the files in that user's google drive.  Depending on how big this is, this can take several minutes to run.

# Get a list (set) of all unique file owners



# For a single file owner, create a list of all files owned by that user


# Separate this list into Google Drive files and non-Google Drive files.  

Ownership changes work only for google drive files, not for uploaded images, pdfs, Excel spreadsheets, etc.  



# Change file ownership from bob@gmail.com to example_holder@gmail.com. 
Ownership can only be transferred within a domain, so you can't transfer directly from bob@gmail.com to bob@example.com.  Since Bob is not super proficient in Python, it's easier to move things to example_holder@gmail.com, and then let the owner of example_holder@gmail.com do the next steps, as the owner of example_holder@gmail.com is fluent in Python and experienced using APIs.  


# Get information about a specific file by file id

This isn't necessarily part of this workflow but it is useful to be able to troubleshoot individual files.



# Move the transferred files to a carpentries shared drive, owned by the example.com domain, logging their original parent.  Knowing their original parent will be very important to 

Now that the files are owned by example_holder@gmail.com, the authentication steps above should be repeated in a new folder, to give credentials to example_holder@gmail.com.  The shared drive in the example.com domain should include example_holder@gmail.com as a user.


# Move them back to their original parent.  

This is why it's important to keep the log of the original parent.  Since bob@example.com is not proficient enough with Python and the API, they can not do this themselves.  If they did, they would be the new owner.  However,  ali@example.com has this profiency and ali@example.com can do it.  However, this will make ali@example.com the new owner.  Ali can then transfer ownership from ali@example.com to bob@example.com, because now they are in the same domain.


# Removing bob@gmail.com as a user from files

Since Bob works for Example Company, they should only have access to Example's documents via their bob@example.com email address, not bob@gmail.  This looks for any files where bob@gmail.com has read or edit access, and removes bob@gmail.com entirely.





