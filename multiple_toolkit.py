###############################################################################################################################
######################################################   SETUP SCRIPT   #######################################################
###############################################################################################################################

#################################################   IMPORT RELEVANT MODULES   ##################################################
# Borrowing modules
import numpy as np              # linear algebra
import pandas as pd             # dataframe
import re                       # regular expression
import matplotlib.pyplot as plt # data visualization

# User-define modules
import provenir                  # to interact efficiently with retrieving job postings and printing results
import individual_toolkit as itk # to retrieve unit functions. See README for content descriptions

##################################################   DEFINE GLOBAL VARIABLES   #################################################
# Get path and list of jobs in Job Bulletins.
# These are raw data
(raw_path, raw_jobs) = provenir.get_raw_jobs()

# Get path and list of jobs in JobBulletins_cleaned
# These are cleaned data
(cleaned_path, cleaned_jobs) = provenir.get_cleaned_jobs()

###############################################################################################################################
#####################################################   JOB_CLASS_TITLE   #####################################################
###############################################################################################################################
def jct_print_results(job_path, job_type):
    '''
    Prints out results when applying itk.jct_get_one function to job postings.
    job_path can only be either raw_path or cleaned_path.
    job_type can only be either raw_jobs or cleaned_jobs.
    '''
    provenir.print_results(path=job_path, files=job_type, fn=itk.jct_get_one)

def _jct_checkpoint1(print_option=False):
    '''Check if no occurence of the word, CAMPUS INTERVIEWS ONLY, in jct'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            result = itk.jct_get_one(cleaned_job)
            if result.find('CAMPUS INTERVIEWS ONLY') != -1:
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with itk.jct_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def jct_get_many():
    '''Returns JOB_CLASS_TITLE field for all jobs as a dataframe'''
    # Make sure checkpoints have been passed
    assert _jct_checkpoint1()==0
    
    # Return an n-by-1 dataframe for job title
    r = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        result      = itk.jct_get_one(cleaned_job)
        r.append(result)
        
    df = pd.DataFrame(data=r, columns=['JOB_CLASS_TITLE'])
    return df
#################################################################################################################################
########################################################   JOB_CLASS_NO   #######################################################
#################################################################################################################################
def jcn_print_results(job_path, job_type):
    '''
    Prints out results when applying itk.jcn_get_one function to job postings.
    job_path can only be either raw_path or cleaned_path.
    job_type can only be either raw_jobs or cleaned_jobs.
    '''
    provenir.print_results(path=job_path, files=job_type, fn=itk.jcn_get_one)
    
def _jcn_checkpoint1(print_option=False):
    '''Check if all jobs are read properly'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            itk.jcn_get_one(cleaned_job)
        except:
            nopass.append(job_path)
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
            
    # Returns
    return len(nopass)

def jcn_get_many():
    '''Returns JOB_CLASS_NO field for all jobs as a dataframe'''
    # Make sure checkpoints have been passed
    assert _jcn_checkpoint1()==0
    
    # Return an n-by-1 dataframe for job title
    r = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        result      = itk.jcn_get_one(cleaned_job)
        r.append(result)
        
    df = pd.DataFrame(data=r, columns=['JOB_CLASS_NO'])
    return df

#################################################################################################################################
########################################################   JOB_DUTIES   #########################################################
#################################################################################################################################
def jd_print_results(job_path, job_type, double_space=True):
    '''
    Prints out results when applying itk.jd_get_one function to job postings.
    job_path can only be either raw_path or cleaned_path.
    job_type can only be either raw_jobs or cleaned_jobs.
    '''
    provenir.print_results(path=job_path, files=job_type, fn=itk.jd_get_one)
    
def _jd_checkpoint1(print_option=False):
    '''Check if the word DUTIES is in each job'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            if 'DUTIES' not in cleaned_job.split():
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with itk.jd_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def _jd_checkpoint2(print_option=False):
    '''Check if the phrase REQUIREMENTS/MINIMUM QUALIFICATIONS is in each job'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            if 'REQUIREMENTS/MINIMUM QUALIFICATIONS' not in raw_job.split('\n'):
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with itk.jd_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)
    