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

We now are going to get all the files in the Google Drive for `example.com`.  Each file in Google Drive has associated metadata, like its name, id, url, etc.  This is a full list of [all metadata for a file](https://developers.google.com/drive/api/v3/reference/files). Many of the metadata fields are self explanatory.  For `mimeType`: this the file type such as [Google's own file types](https://developers.google.com/drive/api/v3/mime-types).  Non-Google file types (pdfs, uploaded images, etc.) are not well documented. Later we'll use a brute force method to check if it's one of Google's own filetypes by seeing if the string contains `google-apps`.

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
We can now get a list of all unique files owners in our domain. This isn't entirely necessary for what we are doing now, but is useful in general when you want to identify all the people who have ownership access to files in your domain. We create a list of all owners in our files, and tranform that list into a set to get sorted, unique values.

```python
owners = []
for f in all_example_files:
    owners.append(f['owners'][0]['emailAddress'])
unique_owners = set(owners)
print(unique_owners)
```

# For a single file owner, create a list of all files owned by that user

This creates a list of files owned by that user.  It then saves this to a `.json` file using `json.dump`.  Side note about the [difference between `json.dump` and `json.dumps`](https://docs.python.org/3.8/library/json.html): `json.dumps` transforms a list to a json formatted string; `json.dump` transforms a list into a json file.

```python
def get_user_files(file_list, user_email, json_filename):
    """
    Function takes three arguments:
    - a list of google drive files
    - a user email address
    - a filename string with .json extension
    Function returns a list of files owned by that user and
    saves the list to a json file.
    """

    user_files = []

    counter = 0
    for i in file_list:
        if i['owners'][0]['emailAddress'] == user_email:
            user_files.append(i)
            counter += 1

    print(counter, i['owners'][0]['emailAddress'])  # just a way to watch the code run
    with open(json_filename, 'w') as files:
        json.dump(user_files, files)

    return user_files
```

# Separate this list into Google Drive files and non-Google Drive files.  

Non google files are pdfs, excel files, image files, etc. that were uploaded to Google Drive by the user.  Google Drive file ownership can be changed within the same domain programatically.  Non-Google Drive file ownership can not be changed programmatically.  These files need to be moved to a [Shared Drive](https://support.google.com/a/answer/7212025) and them moved back to the original location.

```python
def split_by_file_type(file_list, google_filename, nongoogle_filename):
    '''
     Function takes three arguments:
    - a list of google drive files
    - a filename string with .json extension to hold the google files
    - a filename string with .json extension to hold the non-google files
    Function returns two lists of files (google and non-google) owned by that user and
    saves the lists to a json file.
    '''
    google_files = []
    non_google_files = []
    for file in file_list:
        if "google-apps" in k['mimeType']:
            google_files.append(file)
        else:
            non_google_files.append(file)

    with open(google_filename, 'w') as files:
        json.dump(google_files, files)

    with open(nongoogle_filename, 'w') as files:
        json.dump(non_google_files, files)

    return (google_files, non_google_files)

# Example use.  This will save two files to the current working directory.
split_by_file_type(dev_files, 'dev_google_files.json', 'dev_non_google_files.json')
```


# Change file ownership from one `@gmail` account to another `@gmail` account
Ownership can only be transferred within a domain, so you can't transfer directly from dev@gmail.com to dev@example.com.  This example is included as a way to show how to transfer file ownership within a domain (dev@gmail.com to example_holder@gmail.com), and move file ownership from dev@gmail.com to example-holder@gmail.com.  Later, ownership can be transferred to `dev@example.com` via a [Shared Drive](https://support.google.com/a/answer/7212025).

This intermediary step is not entirely necessary. We could move files to a [Shared Drive](https://support.google.com/a/answer/7212025) directly, and them move them back to their parent location. We may want to do it in a case where Dev is no longer employed at Example Company, and do not want to give them the "keys" to Example Company's workspaces.  Moving files to the Shared Drive and back should happen as soon as possible.  When moving files to a Shared Drive, the links will stay the same, but the file will not be in its expected location, causing some users to have difficulty finding it.

```python
def transfer_google_file_ownership(file_list):
    """
    Function takes one arguments
    * file name to json list of files to transfer as a string
    It returns two lists and creates two .json files with those two lists
    * Files where ownership was transferred successfully
    * Files with an error in transferring ownership
    """

    with open(file_list, "r") as read_file:
        google_files_to_transfer = json.load(read_file)

    ownership_transferred = []
    ownership_transfer_error = []

    for file in google_files_to_transfer:
        try:
            make_user_owner(new_email_owner, file['id'], new_email_permission)
            ownership_transferred.append(file['id'])
        except Exception as e:
            print(type(e))
            print(e)
            ownership_transfer_error.append(file['id'])

    # Convert successfully transferred file list to json
    with open('ownership_transferred.json', 'w') as f:
        json.dump(ownership_transferred, f)

    # Convert ownership transfer error file list to json
    with open('ownership_transfer_error.json', 'w') as f:
        json.dump(ownership_transfer_error, f)

    return (ownership_transferred, ownership_transfer_error)

# Example use.  This will save two files to the current working directory.
transfer_google_file_ownership(dev_google_files.json')

```
# Get information about a specific file by file id

This isn't necessarily part of this workflow but it is useful to be able to troubleshoot individual files.
A key part of this is the `supportsAllDrives` option.  This defaults to `False`. By changing this to `True`, this will search for the `fileid` in Shared Drives as well.  When it's set to `False`, Shared Drives are excluded.

```python
import sys
def get_file_info(fileid, parameters_to_get):
    '''
    Function takes two arguments: a file id and a csv string of file parameters to get.
    It returns metadata on the specified file.
    '''
    try:
        info = service.files().get(fileId=fileid, 
                                   fields=parameters_to_get, 
                                   supportsAllDrives = True).execute()
    except: # catch *all* exceptions
        e = sys.exc_info()
        info = e
    return info

# Example use.
included_fields = "id, kind, name, owners, webViewLink, parents, modifiedTime, permissions, mimeType"
fid = "1234567890"
# This will return the text of an error message or the metadata for that file
f = get_file_info(fid, included_fields)
```

# Move the transferred files to the Example Company Shared Drive, owned by the example.com domain

Now that the files are owned by `example_holder@gmail.com`, [the authentication steps above](#set-up-service-credentials) should be repeated in a new folder, to give credentials to `example_holder@gmail.com`.  The Shared Drive in the `example.com` domain should include `example_holder@gmail.com` as a Content Manager.  We need to log each file's original parent, so that each file can be restored to its original location.

This code can also be used for `dev@example.com` to move files of non-Google Drive types to the Shared Drive, as ownership of these files can not be changed directly.

```python

def move_files(filelist, new_parent_id):
    """
    Function takes two arguments
    * file name to json list of files to transfer as a string
    * id of the parent to move files to
    It returns two lists and creates two .json files with those two lists
    * Files where file was transferred successfully
    * Files with an error in transferring file
    """
    parent_transfers = []
    parent_transfer_errors = []

    for f in filelist:
        try:
            file_id = f['id']
            orig_parent = f['parents']
            # Get the original file's parents
            previous_parents = service.files().get(fileId=file_id,
                                        fields='parents', supportsAllDrives = True).execute()
            # Remove those parents and add new parents
            file = service.files().update(fileId=file_id,
                                            addParents=new_parent_id,
                                            removeParents=previous_parents,
                                            fields='id, parents', 
                                            supportsAllDrives=True).execute()
            log = [file_id, orig_parent]
            parent_transfers.append(log)
        except:
            parent_transfer_errors.append(f['id'])

    return (parent_transfers, parent_transfer_errors)

```

# Move them back to their original parent.  

This is why it's important to keep the log of the original parent.  The function to do this is similar to the one above.  In this case though, our source data is a list of lists.  For each sublist, item at index 0 is the file id and item at index 1 is the parent to restore.


```python

def move_files(filelist):
    """
    Function takes two arguments
    * file name to json list of files to transfer as a string
    * id of the parent to move files to
    It returns two lists and creates two .json files with those two lists
    * Files where file was transferred successfully
    * Files with an error in transferring file
    """
    shared_drive_transfers = []
    shared_drive_transfer_errors = []

    for f in filelist:
        try:
            file_id = f[0]
            # Get the original file's parents
            previous_parents = service.files().get(fileId=file_id,
                                        fields='parents', supportsAllDrives = True).execute()
            # Remove those parents and add new parents
            file = service.files().update(fileId=file_id,
                                            addParents=f[1],
                                            removeParents=previous_parents,
                                            fields='id, parents', 
                                            supportsAllDrives=True).execute()

            shared_drive_transfers.append(f[0])
        except:
            shared_drive_transfer_errors.append(f['id'])

    return (shared_drive_transfers, shared_drive_transfer_errors)

```


# Removing dev@gmail.com as a user from files

Since Dev works for Example Company, they should only have access to Example's documents via their dev@example.com email address, not dev@gmail.  The above steps showed how to transfer ownership. We also need to see where `dev@gmail.com` may have other levels of access to the file, and remove them.  This looks for any files where `dev@gmail.com` has read or edit access, and removes `dev@gmail.com` entirely.

First, we look for all files in our domain.  Of those, they can fall into one of three categories. For this example, I'm referring to them as *Restricted Access*, *Anyone with Link*, and *Errors*.  *Restricted Access* can only be accessed by designated people, and those are the ones we are focusing on here. *Anyone with Link* can be accessed by anyone, so there is no need to remove `dev@gmail.com`.   *Errors* catches all the files that didn't work to troubleshoot later.

```python
def delete_user(file_id, permission_id):
    """
    Function takes two arguments
    * file id of a file to remove
    * permission id of the user to remove

    """
    param_perm = {}
    remove_user = service.permissions().delete(fileId = file_id,
                                 permissionId = permission_id, ).execute()


restricted_access = []
anyone_with_link = []
key_error = []

## Using the all_example_files list we created above, we can go through each file and categorize it.
## We will then come back just to the restricted_access files.

for j in all_example_files:

    try:
        file_perms = []
        
        for i in j['permissions']:
            # Create a list of all the existing permissions
            file_perms.append(i['id'])

        # Check to see if "anyoneWithLink" is included in the file_perms
        # If so, put the file data in the `anyone_with_link` list
        if "anyoneWithLink" in file_perms:
            anyone_with_link.append(j)
        # If not, put the file data in the `restricted_access` list
        else: 
            restricted_access.append(j)
   
    except(KeyError):
        # Put file data for KeyError files in a separate list
        key_error.append(j)


## We now go through the restricted_access list and 
## run the delete_user function defined above to remove
## a user from the file.  This goes through a list of users,
## not just a single user.

gmails_to_remove = [] # list of email addresses to be removed
removed_access_by_file = []
errors = []

for k in restricted_access:
    deleted_users = []

    try:
        for p in k['permissions']:
            if p['type'] == 'domain':
                print(k['id'], "Domain")
                print(k['webViewLink'])
            if p['emailAddress'] in gmails_to_remove and p['role'] != "owner":
                print(k['webViewLink'])
                print("deleting: ", k['id'], p['emailAddress'] )
                removed_access_by_file.append([k['id'], p['emailAddress'], p['id']])
                delete_user(k['id'], p['id'])

    except:
        errors.append(p['id'])
        pass
```



