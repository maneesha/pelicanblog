Title: Subtotals and Grouping with Pandas
Date: 2017-03-01
Category: Programming
Tags: python, pandas

For a long time, I've had this hobby project exploring Philadelphia City Council election data.  I've learned no one has this data collected in a consistent, normalized manner.  Vote counts were presented in different ways (as explored in this blog post), candidate names were presented differently (with a middle initial in one election and without it in another).  Part of my plan for normalizing data came from exploring a couple of data sets from Philadelphia elections.  It looked like for any given ward and division, there was a count for the number of absentee ballots, provisional ballots, and machine ballots. 


For example, here's an excerpt of the results for ward 1 division 3 in the 2015 General Election:
```
1,3,"A","DISTRICT COUNCIL - 1ST DISTRICT","Write In","",0
1,3,"A","DISTRICT COUNCIL - 1ST DISTRICT","MARK F SQUILLA","DEMOCRATIC",27
1,3,"M","DISTRICT COUNCIL - 1ST DISTRICT","Write In","",0
1,3,"M","DISTRICT COUNCIL - 1ST DISTRICT","MARK F SQUILLA","DEMOCRATIC",220
1,3,"P","DISTRIT COUNCIL - 1ST DISTRICT","Write In","",0
1,3,"P","DISTRICT COUNCIL - 1ST DISTRICT","MARK F SQUILLA","DEMOCRATIC",2
```

However, here's an excerpt of the results for ward 1 division 3 in the 2011 General Election, where there were two lines for machine ballots (M) for each candidate.
```
1,3,A,DISTRICT COUNCIL - 1ST DIST,MARK F SQUILLA,DEMOCRATIC,1
1,3,A,DISTRICT COUNCIL - 1ST DIST,Write In,,0
1,3,M,DISTRICT COUNCIL - 1ST DIST,MARK F SQUILLA,DEMOCRATIC,65
1,3,M,DISTRICT COUNCIL - 1ST DIST,MARK F SQUILLA,DEMOCRATIC,69
1,3,M,DISTRICT COUNCIL - 1ST DIST,Write In,,0
1,3,M,DISTRICT COUNCIL - 1ST DIST,Write In,,0
1,3,P,DISTRICT COUNCIL - 1ST DIST,MARK F SQUILLA,DEMOCRATIC,2
1,3,P,DISTRICT COUNCIL - 1ST DIST,Write In,,0
```

When asked, the City Commissioners office said that this was a an error and that they'd fix it. They said it was because it represented each machine count rather than the total, but couldn't explain why two records existed in polling places where there were three machines.

My database required that (ward, division, ballot_type, office, candidate) were unique.  So while I had written scripts to populate my database from the csv data where there was one line for each  (ward, division, ballot_type, office, candidate) set, that didn't work when there were multiple lines.  I thought I could re-write my script so that if (ward, division, ballot_type, office, candidate) existed, then it would simply add to the vote count.  I decided instead to sum the vote counts by the  (ward, division, ballot_type, office, candidate) group before putting it in the database.

For this I used Python's Pandas library.

After importing pandas, I read my csv file:

```
import pandas as pd

data = pd.read_csv('dist1.csv')
```

This gave me results like:

```
1 	3 	A 	DISTRICT COUNCIL - 1ST DISTRICT 	MARK F SQUILLA 	DEMOCRATIC 	1
1 	3 	A 	DISTRICT COUNCIL - 1ST DISTRICT 	Write In 	NaN 	0
1 	3 	M 	DISTRICT COUNCIL - 1ST DISTRICT 	MARK F SQUILLA 	DEMOCRATIC 	65
1 	3 	M 	DISTRICT COUNCIL - 1ST DISTRICT 	MARK F SQUILLA 	DEMOCRATIC 	69
1 	3 	M 	DISTRICT COUNCIL - 1ST DISTRICT 	Write In 	NaN 	0
1 	3 	M 	DISTRICT COUNCIL - 1ST DISTRICT 	Write In 	NaN 	0
1 	3 	P 	DISTRICT COUNCIL - 1ST DISTRICT 	MARK F SQUILLA 	DEMOCRATIC 	2
1 	3 	P 	DISTRICT COUNCIL - 1ST DISTRICT 	Write In 	NaN 	0

```

I could then get the sum of the votes by the group () like this;

data.groupby(by=['ward', 'division', 'ballot_type', 'office', 'candidate', 'party'])['votes'].sum()

This gave me results like:

```
1      3        A            DISTRICT COUNCIL - 1ST DISTRICT  MARK F SQUILLA  DEMOCRATIC      1
                M            DISTRICT COUNCIL - 1ST DISTRICT  MARK F SQUILLA  DEMOCRATIC    134
                P            DISTRICT COUNCIL - 1ST DISTRICT  MARK F SQUILLA  DEMOCRATIC      2
```

What was consistently missing from this was all the write in votes -- those with NaN for party.  This is [how pandas works](http://pandas.pydata.org/pandas-docs/stable/missing_data.html#na-values-in-groupby).  I replaced all NaN values with "noparty" as follows:

data['party'] = data['party'].fillna('noparty')

Now when I ran 

data.groupby(by=['ward', 'division', 'ballot_type', 'office', 'candidate', 'party'])['votes'].sum()

those write-in votes were included, giving me

```
1      3        A            DISTRICT COUNCIL - 1ST DISTRICT  MARK F SQUILLA  DEMOCRATIC      1
                                                              Write In        noparty         0
                M            DISTRICT COUNCIL - 1ST DISTRICT  MARK F SQUILLA  DEMOCRATIC    134
                                                              Write In        noparty         0
                P            DISTRICT COUNCIL - 1ST DISTRICT  MARK F SQUILLA  DEMOCRATIC      2
                                                              Write In        noparty         0

```


I then wanted to spit this pandas series out to a new csv file:

```
x = data.groupby(by=['ward', 'division', 'ballot_type', 'office', 'candidate', 'party'])['votes'].sum()

x.to_csv('/home/myfolder/foo.csv')
```

This filled in all the values that weren't displayed in the grouping structure above, so I ended up with this:

```
1,3,A,DISTRICT COUNCIL - 1ST DISTRICT,MARK F SQUILLA,DEMOCRATIC,1
1,3,A,DISTRICT COUNCIL - 1ST DISTRICT,Write In,noparty,0
1,3,M,DISTRICT COUNCIL - 1ST DISTRICT,MARK F SQUILLA,DEMOCRATIC,134
1,3,M,DISTRICT COUNCIL - 1ST DISTRICT,Write In,noparty,0
1,3,P,DISTRICT COUNCIL - 1ST DISTRICT,MARK F SQUILLA,DEMOCRATIC,2
1,3,P,DISTRICT COUNCIL - 1ST DISTRICT,Write In,noparty,0
```

I now had a csv file for 2011 data matching the structure of the other election years and was ready to use it in my work.

Since I had 11 data sets that I needed to clean up like this, I used the Python `glob` library to go over each one.  

```
import glob

files = glob.glob('dist*.csv')

for file in files:
    data = pd.read_csv(file)
	data['party'] = data['party'].fillna('noparty')
	output_data = data.groupby(by=['ward', 'division', 'ballot_type', 'office', 'candidate', 'party'])['votes'].sum()
	output_data.to_csv('new_' + file)
```















