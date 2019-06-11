# Import relevant modules
import os # interface with the underlying OS

def get_raw_jobs():
    '''
    GET_RAW_JOBS returns a tuple (raw_path, raw_jobs), where raw_path is the path to the folder containing raw_jobs, i.e., Job 
    Bulletins, and raw_jobs is the list of all jobs in the Job Bulletins folder. Keep in mind that these are just file names.
    '''
    
    # Define path to look at
    path = 'CityofLA/Job Bulletins/'
    
    # Get a list of all txt files in this path
    raw_jobs = os.listdir(path)
    raw_jobs.sort() # WARNING: this mutates the list
    
    # Remove `Vocational Worker  DEPARTMENT OF PUBLIC WORKS.txt` 
    # as it doesn't share the same job description pattern of the City of LA
    raw_jobs.remove('Vocational Worker  DEPARTMENT OF PUBLIC WORKS.txt')
    
    # Sanity check
    assert len(raw_jobs) == 682 # this number comes from already trying this code individually
    
    # Returns
    return (path, raw_jobs)

def get_cleaned_jobs():
    '''
    GET_CLEANED_JOBS returns a tuple (clean_path, clean_jobs), where clean_path is the path to the folder containing clean_jobs, 
    i.e., JobBulletins_clean, and clean_jobs is the list of all jobs in the JobBulletins_clean folder. Keep in mind that these 
    are just file names.
    '''
    # Define path to look at
    path = 'CityofLA/JobBulletins_cleaned/'

    # Get a list of all txt files in this path
    cleaned_jobs = os.listdir(path)
    cleaned_jobs.sort() # WARNING: this mutates the list
    
    # Remove `Vocational Worker  DEPARTMENT OF PUBLIC WORKS.txt` 
    # as it doesn't share the same job description pattern of the City of LA
    cleaned_jobs.remove('Vocational Worker  DEPARTMENT OF PUBLIC WORKS.txt')
    
    # Sanity check
    assert len(cleaned_jobs) == 682 # this number comes from already trying this code individually
    
    # Returns
    return (path, cleaned_jobs)
