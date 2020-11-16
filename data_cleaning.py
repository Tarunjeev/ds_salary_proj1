#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 03:05:20 2020

@author: tarunjuneja
"""

import pandas as pd

df = pd.read_csv('glassdoor_jobs.csv')

# Removing salary estimate with the value = -1
df = df[df['Salary Estimate'] != '-1']

#Parsing Salary Estimate values using lambda functions where we split some things or we replace some things with blank spaces
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x:x.replace('k', '').replace('$',''))

# Just in case if I would have taken a data with much more values then there were some cases that companies payed on hourly bases
df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)
# Now let's add 2 variables minimum salary and maximum salary
df['min_salary'] = minus_Kd.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = minus_Kd.apply(lambda x: int(x.split('-')[1]))
df['average_salary'] = (df.min_salary + df.max_salary)/2


# Company Name text
df['company_txt'] = df.apply(lambda  x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

# Just to make data more clean, removing company from type of ownership
df['Type of Ownership'] = df['Type of ownership'].apply(lambda x: x.replace('Company -',''))
del df['Type of ownership']

#
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])

#To double check if we have any outliers
df.job_state.value_counts()

# No values in that column so taking headquarters out
df['some_state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

# Age of the company
df['age'] = df.Founded.apply(lambda x: x if x<1 else 2020 - x)

# Parsing of job description
# 1) python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()
# 2) spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df.spark_yn.value_counts()
# 3) aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df.aws_yn.value_counts()
# 4) excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df.excel_yn.value_counts()
# 5) R
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r-studio' or 'r studio' in x.lower() else 0)
df.R_yn.value_counts()

df.to_csv('salary_data_cleaned.csv', index = False)
