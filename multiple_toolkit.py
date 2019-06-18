###############################################################################################################################
######################################################   SETUP SCRIPT   #######################################################
###############################################################################################################################

#################################################   IMPORT RELEVANT MODULES   #################################################
# Borrowing modules
import numpy as np              # linear algebra
import pandas as pd             # dataframe
import re                       # regular expression
import matplotlib.pyplot as plt # data visualization

# User-define modules
import provenir                  # to interact efficiently with retrieving job postings and printing results
import individual_toolkit as itk # to retrieve unit functions. See README for content descriptions

##################################################   DEFINE GLOBAL VARIABLES   ################################################
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
    '''Checks if CAMPUS INTERVIEWS ONLY is in jct. No pass when yes.'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            jct = itk.jct_get_one(cleaned_job)
            if jct.find('CAMPUS INTERVIEWS ONLY') != -1:
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with provenir.spotlight() and itk.jct_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def _jct_checkpoint2(print_option=False):
    '''Checks if a job title has an open parenthesis in it. No pass when yes.'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            jct = itk.jct_get_one(cleaned_job)
            if jct.find('(') != -1:
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with provenir.spotlight() and itk.jct_get_one()')
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
    ## no CAMPUS INTERVIEWS ONLY in jct
    assert _jct_checkpoint1()==0
    ## no open parenthesis ( in jct
    assert _jct_checkpoint2()==0
    
    # Return an n-by-1 dataframe for job title
    r = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        jct         = itk.jct_get_one(cleaned_job)
        r.append(jct)
        
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
    '''Checks if all jobs are read properly'''
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
    ## make sure all jobs are read properly
    assert _jcn_checkpoint1()==0
    
    # Return an n-by-1 dataframe for job title
    r = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        jcn         = itk.jcn_get_one(cleaned_job)
        r.append(jcn)
        
    df = pd.DataFrame(data=r, columns=['JOB_CLASS_NO'])
    return df

#################################################################################################################################
########################################################   JOB_DUTIES   #########################################################
#################################################################################################################################
def jd_print_results(job_path, job_type):
    '''
    Prints out results when applying itk.jd_get_one function to job postings.
    job_path can only be either raw_path or cleaned_path.
    job_type can only be either raw_jobs or cleaned_jobs.
    '''
    provenir.print_results(path=job_path, files=job_type, fn=itk.jd_get_one, double_space=True)
    
def _jd_checkpoint1(print_option=False):
    '''Checks if the word DUTIES is in each job'''
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
                  'Inspect each of them with provenir.spotlight() and itk.jd_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def _jd_checkpoint2(print_option=False):
    '''Checks if the phrase REQUIREMENTS/MINIMUM QUALIFICATIONS is in each job'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            if 'REQUIREMENTS/MINIMUM QUALIFICATIONS' not in cleaned_job.split('\n'):
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with provenir.spotlight() and itk.jd_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def _jd_checkpoint3(print_option=False):
    '''Checks if NOTE, SPECIAL, VACANCY, or any of their variations, are in jd. No pass when yes.'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            jd = itk.jd_get_one(cleaned_job)
            if ('NOTE' in jd) or ('SPECIAL' in jd) or ('VACANCY' in jd):
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with provenir.spotlight() and itk.jd_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def jd_get_many():
    '''Returns JOB_DUTIES field for all jobs as a dataframe'''
    # Make sure checkpoints have been passed
    ## every job must have the word DUTIES in it, even if raw data doesn't
    ## add manually if needed
    assert _jd_checkpoint1()==0
    ## normalize all variations of the word REQUIREMENTS to REQUIREMENTS/MINIMUM QUALIFICATIONS
    assert _jd_checkpoint2()==0
    ## no occurences of the words NOTES, SPECIAL, VACANCY (and their variations) are allowed
    assert _jd_checkpoint3()==0
    
    # Return an n-by-1 dataframe for job title
    r = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        jd          = itk.jd_get_one(cleaned_job)
        r.append(jd)
        
    df = pd.DataFrame(data=r, columns=['JOB_DUTIES'])
    return df

#################################################################################################################################
#########################################################   OPEN_DATE   #########################################################
#################################################################################################################################
def od_print_results(job_path, job_type):
    '''
    Prints out results when applying itk.od_get_one function to job postings.
    job_path can only be either raw_path or cleaned_path.
    job_type can only be either raw_jobs or cleaned_jobs.
    '''
    provenir.print_results(path=job_path, files=job_type, fn=itk.od_get_one)
    
def _od_checkpoint1(print_option=False):
    '''Checks if an open parenthesis is in between Open Date and ANNUAL SALARY. No pass when none.'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            start = 'Open Date'; end = 'ANNUAL SALARY'
            temp  = cleaned_job[cleaned_job.index(start):cleaned_job.index(end)]
            if '(' not in temp:
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with provenir.spotlight() and itk.jd_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def _od_checkpoint2(print_option=False):
    '''Checks if the word Revised (or any of its variation) is in between Open Date and ANNUAL SALARY. No pass when yes.'''
    # The idea is that if length of nopass is more than 1,
    # then this checkpoint has not been passed.
    nopass = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        try:
            start = 'Open Date'; end = 'ANNUAL SALARY'
            temp  = cleaned_job[cleaned_job.index(start):cleaned_job.index(end)].lower()
            if 'revised' in temp:
                nopass.append(job_path)
        except:
            ## If this part is executed, there is problem with itk.jct_get_one
            print('Jobs surrounded by # fail at unit level.' + 
                  'Inspect each of them with provenir.spotlight() and itk.jd_get_one()')
            provenir.catch_bad_jobs(job_path)
            return
    
    # Print out which job fails at this checkpoint
    if print_option:
        for e in nopass:
            print(e)
    
    # Returns
    return len(nopass)

def od_get_many():
    '''Returns OPEN_DATE field for all jobs as a dataframe'''
    # Make sure checkpoints have been passed
    ## every job must have the open parenthesis ( in between Open Date and ANNUAL SALARY
    assert _od_checkpoint1()==0
    ## no variations of the word Revised is in between Open Date and ANNUAL SALARY
    assert _od_checkpoint2()==0
    
    # Return an n-by-1 dataframe for job title
    r = []
    for file_name in cleaned_jobs:
        job_path    = cleaned_path + file_name
        cleaned_job = open(job_path, 'rt').read()
        od          = itk.od_get_one(cleaned_job)
        r.append(od)
        
    df = pd.DataFrame(data=r, columns=['OPEN_DATE'])
    return df

#################################################################################################################################
############################################   DRIVERS_LICENSE_REQ & DRIV_LIC_TYPE   ############################################
#################################################################################################################################