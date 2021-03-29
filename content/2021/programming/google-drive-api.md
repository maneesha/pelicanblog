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

We begin working in the `example.com` workspace. Ensure Dev is signed in to `dev@example.com`.  Create a directory called `dev-example`.

To begin, the Dev must [set up the Google Drive API and install necessary Python packages](https://developers.google.com/drive/api/v3/quickstart/python).  Note even though Google's documentation requires Python 2.6 or greater, please use Python 3.x as 2.x versions [have been deprecated for over a year](https://www.python.org/doc/sunset-python-2/).

To [enable the Google Drive API](https://developers.google.com/drive/api/v3/quickstart/python#step_1_turn_on_the
), you'll be asked to set up an app. You may be asked to select an account if you are logged in to more than one google account.  If this happens, be sure to select `dev@example.com`. Give your app it a name when prompted. Select "Desktop app" for your OAuth Client.  You'll be asked to download client configuration.  Save this file (`credentials.json`) to the `dev-example` directory.

Dev will now install the [Google Client Library](https://developers.google.com/drive/api/v3/quickstart/python#step_2_install_the_google_client_library
), ideally in some sort of virtual environment (that's a topic for another day as there are many ways to manage Python environments)
.

# Get started with the code

The next sections describe the code used to set up credentials and run each step of the process. I like doing this in a Jupyter notebook, as it allows the user to run code step by step and view results in between.


# Set up service credentials 

Now that we have enabled the API and installed the necessary libraries, we can set up our service credentials.  This function will create Dev's service credentials. The `service` will be used in all subsequent API calls.  This creates a `token.pickle` file in the same working directory.  You may be asked to select an account to use this.  If this happens, be sure to select `dev@example.com`. This code is adapted from the [sample setup in Google's documentation](https://developers.google.com/drive/api/v3/quickstart/python#step_3_set_up_the_sample).

The scopes in that documentation are `read-only`; many [levels of scopes can be set up](https://developers.google.com/drive/api/v2/about-auth#OAuth2Authorizing). The scopes in this example allow full, permissive scope to access all of a user's files, excluding the Application Data folder. If you change your scopes, you must delete the `token.pickle` file so that it can be re-generated.

```python
SCOPES = ['https://www.googleapis.com/auth/drive']

def set_creds():
    """Sets Google Drive API credentials
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service

service = set_creds()
```

# Make sure it's you

This code is a quick check to show you information about yourself. You should see your name, email, and other information listed.

```python
print(service.about().get(fields='user').execute())
```

This should display something like:

```text
{'user': {'kind': 'drive#user', 'displayName': 'Dev User', 'photoLink': 'https://lh3.googleusercontent.com/a-/abcde12345', 'me': True, 'permissionId': '9876543210', 'emailAddress': 'dev@example.com'}}
```

# Get all files in the google drive

We now are going to get all the files in the Google Drive for `example.com`.  Each file in Google Drive has associated metadata, like its name, id, url, etc.  This is a full list of [all metadata for a file](https://developers.google.com/drive/api/v3/reference/files).

Here we create a list of what parameters we want to get. Note this is not actually `list` data type in Python.  Rather is a `string` of comma separated values enclosed in parentheses.  We also want to include a `nextPageToken` so we can go through each page of the results. 


```python
parameters_to_get = "(id, kind, name,  owners, webViewLink, parents, modifiedTime, permissions, mimeType)"
included_fields = "nextPageToken, files{}".format(parameters_to_get)

def get_files(service):
    '''
    Returns list of dictionaries of all files in that user's domain.
    '''
    result = []
    page_token = None
    while True:

        param = {}
        if page_token:
            param['pageToken'] = page_token
        files = service.files().list(fields=included_fields, **param).execute()

        result.extend(files['files'])
        page_token = files.get('nextPageToken')
        if not page_token:
            break

    return result

```

We can now run this function, and spot check some of the results.

```python
# This may take a few minutes to run.
all_example_files = get_files(service=service)

# See how many files were returned
print("Count files returned:", len(all_example_files))

# Peek at the first and last files in the list
print(all_example_files[0])
print(all_example_files[-1])
```


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





