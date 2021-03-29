---
Title: Google Drive API
Date: 2021-04-01
Category: Programming
Tags: google drive, api, python
---

# Introduction

Where I work, we've grown quickly and organically in the past few years.  This means we have had to catch up to keep our technology and infrastructure systems in support of our growing work.  Before we had formally organized programs, many staff members used Google docs via their personal `@gmail.com` accounts to manage and share work.  Later, as we became more established as Example Company, we set up Google Apps for Business, and set up a `example.com` email address for each user, allowing them to work with Google Drive in our domain.  However, many of our old files were still owned by `@gmail.com` users.  Google does not allow transfer of file ownership across domains, so I had to come up with a workaround to transfer ownership of files in the `example.com` Google Drive that were owned by a `gmail.com` user to a `example.com` user. Essentially, this workflow temporarily places files in a Shared Drive that outside users can access, and then moves them back to their original location, assigning an `example.com` user as the owner.  Ideally, everything should be in a Shared Drive, but we're not ready to do that yet as it would necessitate larger overhauls of our systems, so everything will stay in Google Drive for now.

This blog post demonstrates this process with two sample personas:

* **Dev**. Dev used to use `dev@gmail.com` for Example Company work, and now needs to transfer ownership of all those file to `dev@example.com`.  Dev knows a little about Python and about APIs but is not proficient, so Dev can run code that Ali provides.  To do this for a user who is completely unfamiliar with Python or interacting with APIs will require much more hand-holding.
* **Ali**. Ali is an expert Python user and has worked extensively with various APIs.  Ali is the sysadmin for Example Company.  Ali wrote code that Dev could run in a Jupyter notebook for part of this workflow, as Ali can not directly access `dev@gmail.com`.

The rough workflow is listed below, with sample code following. Depending on Dev's comfort level running code, some of these steps can be consolidated. They are broken out here to keep things as simple as possible for Dev and reduce confusion for other team members as files are moved.

1. Ali creates a Jupyter notebook with step by step instructions for Dev to run.  Ali creates a Shared Drive for Example Company and ensures `dev@gmail.com` has full access to it.
1. Dev sets up Google's API
1. Dev runs code in the provided Jupyter notebook to get a list of all files in the `example.com` Google Drive *(not Shared Drive)* that are owned by `dev@gmail.com`.
1. Dev runs code in the provided Jupyter notebook to filter these results to get two lists:
    * Google Drive files (Docs, Sheets, Slides, etc.) that they own
    * Non-Google Drive files (uploaded PDFs, Excel spreadsheets, images, etc.) that they own
1. Dev runs code in the provided Jupyter notebook to transfer ownership of Google Drive files that were owned by `dev@gmail.com` to `example-holder@gmail.com`.  
1. Dev runs code in the provided Jupyter notebook to transfer ownership of non-Google Drive files to a Shared Drive owned by Example Company, keeping a log of each file's original parent folder. This will not be this file's final location.
1. Ali then moves those non-Google files from the Shared Drive back to their original location (using the parents that were in the log), and re-assigns ownership to `dev@example.com`.
1. Ali moves all the files that are newly owned by `example-holder@gmail.com` to a Shared Drive, keeping a log of each file's original parent folder, and immediately moves them back to their original location  (using the parents that were in the log).
1.  Ali verifies that there are no remaining files owned by `example-holder@gmail.com`.
1. Once everything is done, Ali removes `dev@gmail.com` from Example Company's Shared Drive. Dev will still have access to everything via `dev@example.com`.



# Set up Google API 

https://developers.google.com/drive/api/v3/quickstart/python

When asked to select a google account, be sure to select the one that you want to move the ownership from (dev@gmail.com).
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



# Change file ownership from dev@gmail.com to example_holder@gmail.com. 
Ownership can only be transferred within a domain, so you can't transfer directly from dev@gmail.com to dev@example.com.  Since Dev is not super proficient in Python, it's easier to move things to example_holder@gmail.com, and then let the owner of example_holder@gmail.com do the next steps, as the owner of example_holder@gmail.com is fluent in Python and experienced using APIs.  


# Get information about a specific file by file id

This isn't necessarily part of this workflow but it is useful to be able to troubleshoot individual files.



# Move the transferred files to a carpentries shared drive, owned by the example.com domain, logging their original parent.  Knowing their original parent will be very important to 

Now that the files are owned by example_holder@gmail.com, the authentication steps above should be repeated in a new folder, to give credentials to example_holder@gmail.com.  The shared drive in the example.com domain should include example_holder@gmail.com as a user.


# Move them back to their original parent.  

This is why it's important to keep the log of the original parent.  Since dev@example.com is not proficient enough with Python and the API, they can not do this themselves.  If they did, they would be the new owner.  However,  ali@example.com has this profiency and ali@example.com can do it.  However, this will make ali@example.com the new owner.  Ali can then transfer ownership from ali@example.com to dev@example.com, because now they are in the same domain.


# Removing dev@gmail.com as a user from files

Since Dev works for Example Company, they should only have access to Example's documents via their dev@example.com email address, not dev@gmail.  This looks for any files where dev@gmail.com has read or edit access, and removes dev@gmail.com entirely.





