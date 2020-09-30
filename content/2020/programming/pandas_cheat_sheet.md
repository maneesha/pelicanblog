---
Title: Pandas cheat sheet
Date: 2020-09-27
Category: Programming
Tags: Python, pandas
---


Because I often find myself looking up how to do the same things over and over again in Pandas, this is a list of what I think are my most frequent searches and how to do these things.



## Filter a dataframe by value of one column

This will return all rows where the `math_score` is greater than 75. 


```
df.loc[(df['math_score'] > 75)]
```

This will return all rows where the `math_score` is greater than 75 and `reading_score` is greater than 80. Note each clause is in parentheses.


```
df.loc[(df['math_score'] > 75) & (df['reading_score'] > 80)]
```



## Pandas lambda function

The `apply` function can be used to manipulate values in a dataframe or specified columns based on a custom function.  We can write a simple function like:


```
def adjust_score(num):
    return num * 1.15
```

We can then apply it to the `score` column in our dataframe.  For each value in `df['score']` it multiplies it by 1.15.  It returns the new values but does not change the column.

```
df['score'].apply(lambda x: adjust_score(x))

```

This can then be used to create a new column in the dataframe.

```
df['adjusted_score'] = df['score'].apply(lambda x: adjust_score(x))
```


## Dates and quarters

Pandas has a `PeriodIndex` feature which will let you get dates by quarters.  Read more in [this Stack Overview post](https://stackoverflow.com/questions/37632766/python-pandas-get-fiscal-quarter-from-fiscal-year-and-month-for-uk).

```
all_workshops['quarter'] = pd.PeriodIndex(all_workshops['start_date'], freq='Q-DEC').strftime('%YQ%q')
```


## Check if a string contains a substring


This returns a series of boolean values. 

```
df['lunch'].str.contains('pizza')
```

Filter your dataframe to include only rows that meet this criteria:

```
df[df['lunch'].str.contains('pizza')]

```

## Select unique rows between two dataframes

This gives you what's in `df1` but not `df2`.

If you have two dataframes with the same columns, you can find the rows that are unique (not duplicated) between the two dataframes.  From this [Stack Overflow](https://stackoverflow.com/questions/23460345/selecting-unique-rows-between-two-dataframes-in-pandas) post, it looks for what's in the `lunch` column of `df1`, checks to see if it's in the `lunch` column of `df2`, then takes the inverse of that (noted by the `~`).

```
df1[~df1.['lunch']].isin(df2['lunch'])
```

## Renaming columns in a dataframe

Use `rename` and pass a dictionary to `columns`. The key is the old column name, and the value is the new column name.

```
df.rename(columns={'count':'Total Attendance'})

```
or rename all columns by passing a list to `df_columns`.  Be sure the items in the list are in the correct order.  

```
df.columns = ['id', 'first_name', 'last_name', 'test_score']
```


## Convert date string to date type

If you have a set of values like `2020-05-06`, `2020-06-12` and so on, these can be converted to Pandas `datetime` types:


```
df['start_date'] = pd.to_datetime(df['start_date'])
```


## Sort a data frame

Note whether to do ascending, and where to put `na` values (at the beginning or end of the sort).

```
df.sort_values(by=['last_name', 'first_name', 'city'], ascending=False, na_position='first', inplace=True)
```

##  Convert numeric types

If Pandas is reading floats when you wanted them to be integers

```
df['score] = df['score].astype('int)
```

## Grouping and aggregating

Grouping and aggregating can return either a series or a dataframe.  

Returns a series (both do the same thing)

```
df.groupby(['Name', 'Fruit'])['Number'].agg('sum')
```
```
df.groupby(['Name', 'Fruit'])['Number'].agg('sum')
```

Returns a dataframe (both do the same thing)

```
df.groupby(['Name', 'Fruit'])[['Number']].agg('sum')
```
```
df.groupby(['Name', 'Fruit'])[['Number']].sum()
```


## Change one value based on another

Using the code shared above to filter values of one column, we can then re-assign values of an existing column or create a new column with the given value.  See this [Stack Overflow post](https://stackoverflow.com/questions/19226488/change-one-value-based-on-another-value-in-pandas).  In this example, the code looks for all values of `start_date` between `2018-01-01` and `2018-03-31`. It then puts the value `2018Q1` in the `quarter` column for all matching rows.  If the `quarter` column does not already exist, it creates it.  If it does exist, it overwrites the values in that quarter.


```
all_workshops.loc[((all_workshops['start_date'] >= "2018-01-01") &  
                    (all_workshops['start_date'] <= "2018-03-31")), 'quarter'] = "2018Q1"
```


## Merge dataframes

If you have two dataframes:

* `all_students` with fields including `id, first_name, last_name` and so on
* `student_awards` with fields including `award_id, student_id, award_type, award_date` and so on 

These dataframes can be merged as follows:

```
student_progress = pd.merge(left=all_students, 
                            right=student_awards, 
                            how="left", 
                            left_on="id", 
                            right_on="student_id",
                            )
```

This is similar to the SQL statement:

```
SELECT * 
FROM all_students st JOIN student_awards aw
ON st.id = aw.student_id;
```