import os # module to interface with the underlying OS

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

def catch_bad_jobs(job_path):
    '''
    CATCH_BAD_JOBS prints paths to jobs that throw errors in the try clause for data cleaning purposes.
    '''
    ## Define some useful variables
    border_line = '##############################################################################################'
    how_many    = int((len(border_line) - len(job_path))/2) - 3 # 3 white spaces on each side
    print(border_line)
    print('#'*how_many + '   ' + job_path + '   ' + '#'*how_many)
    print(border_line)
    
def print_results(path, files, fn, double_space=False):
    '''
    PRINT_RESULTS prints outputs when applying the function fn to each file in files.
    '''
    for file_name in files:
        job_path = path + file_name            # define path to file_name
        job_info = open(job_path, 'rt').read() # read in job as a string
        try:
            result = fn(job_info)
            if double_space:                   # add double-space to aid result visualization
                result += '\n'
            print(result)
        except:
            catch_bad_jobs(job_path)           # catch jobs that fail the try clause
            
def spotlight(job_name, job_path, job_type):
    '''
    Retrieves a specific job posting.
    job_path can only be raw_path or cleaned_path
    job_type can only be raw_jobs or cleaned_jobs
    '''
    job_idx  = job_type.index(job_name)     # get idx of this job in the list of job_type
    job_path = job_path + job_type[job_idx] # define path to this job
    content  = open(job_path, 'rt').read()  # read in this job as a string
    
    return content