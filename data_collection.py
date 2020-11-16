#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 20:34:46 2020

@author: tarunjuneja
"""

import glassdoor_scraper as gs
import pandas as pd
path = "/Users/tarunjuneja/Desktop/ds_salary_proj1/chromedriver"

df = gs.get_jobs('data scientist', 1000, False, path, 15)

df.to_csv('glassdoor_jobs.csv', index = False)
