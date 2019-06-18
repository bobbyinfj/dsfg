#################################################################################################################################
#####################################################   JOB_CLASS_TITLE   #######################################################
#################################################################################################################################
def jct_get_one(job):
    '''Returns the field JOB_CLASS_TITLE (jct) as a string'''
    # Locate relevant information: from the beginning to the phrase, Class Code
    end  = 'Class Code'
    temp = job[:job.index(end)]
    # Split at white space, automatically skipping all escape characters. 
    # This feature of split is amazing!
    jct = temp.split()
    
    # Returns
    jct = ' '.join(jct) # join words with white spaces
    return jct

#################################################################################################################################
#######################################################   JOB_CLASS_NO   ########################################################
#################################################################################################################################
def jcn_get_one(job):
    '''Returns the field JOB_CLASS_NO (jcn) as a string'''
    # Locate relevant information: from the phrase Class Code to the phrase Open Date
    start = 'Class Code'; end = 'Open Date'
    temp = job[job.index(start):job.index(end)]
    # Check if anything in temp is a digit via isdigit(). If it is, get it
    jcn  = [e for e in temp.split() if e.isdigit()][0] # first element in the list is the class code
    # Per requirement, if Class Code only has 3 non-zero digits, then becomes 0###
    if len(jcn) == 3:
        jcn = '0'+jcn
    
    # Returns
    return jcn

#################################################################################################################################
########################################################   JOB_DUTIES   #########################################################
#################################################################################################################################
def jd_get_one(job):
    '''Returns the field JOB_DUTIES (jd) as a string'''
    # Locate the relevant information: from the word DUTIES to the phrase REQUIREMENTS/MINIMUM QUALIFICATIONS
    start = 'DUTIES'; end = 'REQUIREMENTS/MINIMUM QUALIFICATIONS'
    temp  = job[job.index(start):job.index(end)]
    # Split at white space and ignore the 0th element (the word 'DUTIES')
    temp = temp.split()[1:]
    # Join with white space to get the required format
    jd = ' '.join(temp)
    
    # Returns
    return jd
#################################################################################################################################
###########################################   DRIVERS_LICENSE_REQ & DRIV_LIC_TYPE   #############################################
#################################################################################################################################
def _get_dl_info(job):
    '''
    Helper function for DRIVERS_LICENSE_REQ and DRIV_LIC_TYPE fields. Not intended for single use.
    '''
    # Locate the information
    start = job.index('PROCESS NOTES') 
    temp  = job[start:]

    # Find driver license and its type
    temp  = temp.split('\n')                                               # Ex: ['PROCESS NOTES', '', etc.]
    dl   = []                                                              # dl=information about driver's license
    for possibly_contains_dl in temp:
        if 'driver' in possibly_contains_dl:
            DL_info = ([e for e in 
                        possibly_contains_dl.split('.')                    # Ex: 4., Some positions..., etc.
                        if len(e) > 3])                                    # split at period and kill itemizers
            for sentence in DL_info:
                if 'may' in sentence:                                      # 'may' is a clear indicator for not required
                    dl.append(('P', np.nan))
                    break
                else:                                                      # else, DL is required
                    start = possibly_contains_dl.index('^^^') + len('^^^')
                    end   = possibly_contains_dl.index('@@@')
                    info  = possibly_contains_dl[start:end]
                    if len(info) > 2:                                      # ' ' has length 1. put 2 just to make sure
                        dl.append(('R', info))                             # Ex: ' A ', already 3 characters
                    else:
                        dl.append(('R', np.nan))
                    break
            break
    
    # Returns
    dl = pd.DataFrame(data=dl, columns=['DRIVERS_LICENSE_REQ', 
                                        'DRIV_LIC_TYPE'])                  # returns as a dataframe
    return dl

###################################################   DRIVERS_LICENSE_REQ   #####################################################
def dlr_get_one():
    '''Returns DRIVERS_LICENSE_REQ (dlr) (string)'''
    try:
        dlr = list(dl_baseline['DRIVERS_LICENSE_REQ'])
    except:
        warning = 'Define a global variable called dl_baseline via dl_baseline=_get_dl_info(job)'
        raise ValueError(warning)
        
    return dlr

######################################################   DRIV_LIC_TYPE   ########################################################
def dlt_get_one():
    '''Returns DRIV_LIC_TYPE (dlt) (string)'''
    try:
        dlt = list(dl_baseline['DRIV_LIC_TYPE'])
    except:
        warning = 'Define a global variable called dl_baseline via dl_baseline=_get_dl_info(job)'
        raise ValueError(warning)
    
    return dlt

#################################################################################################################################
###########################################   ENTRY_SALARY_GEN & ENTRY_SALARY_DWP   #############################################
#################################################################################################################################
def _get_salary_info(salary_text):
    '''
    Helper function for ENTRY_SALARY_GEN and ENTRY_SALARY_DWP. Not intended for single use.
    Returns job's salary in the form of $#####-$#####, $##### (flat-rated)
    '''
    # The idea is to use isdigit() function to recognize a number. So need to strip off everthing that fails this.
    # Replace '.' with white space. This resolves '#####.' (dot at the end)
    # Replace '$' with white space. This resolves '$#####' (dollar sign in the beginning)
    # Replace ',' with empty space. This resolves '$##,###' (comma in the middle of the number)
    # Empty space because we will split at white space later
    temp = (salary_text.replace('.', '')
                       .replace('$', '')
                       .replace(',', '')
                       .replace(';', '')
                       .replace('*',''))
    
    # Get salaries in temp by using the isdigit() function. 
    salary_range = []
    for word in temp.split():      # split here
        if len(salary_range) >= 2: # break to make sure that only the first listed salary range is included
            break
        else:                      # otherwise, put it in the salary_range list
            if word.isdigit():
                salary_range.append(word)
    
    # Returns the required format
    return '-'.join(salary_range)

#####################################################   ENTRY_SALARY_GEN   ######################################################
def esg_get_one(job):
    '''Returns ENTRY_SALARY_GEN (esg) (string)'''
    # Locate the information: from ANNUAL SALARY to Department of Water and Power
    start = 'ANNUAL SALARY'; end = 'Department of Water and Power'
    temp  = job[job.index(start):job.index(end)]
    
    # Returns
    esg = _get_salary_info(salary_text=temp)
    return esg

def esd_get_one(job):
    '''Returns ENTRY_SALARY_DWP (esd) (string)'''
    # Locate the information: from Department of Water and Power to NOTES: (with colon)
    start = 'Department of Water and Power'; end = 'NOTES:'
    temp  = job[job.index(start):job.index(end)]
    
    # Returns
    esd = _get_salary(salary_text=temp)
    return esd

#################################################################################################################################
########################################################   OPEN_DATE   ##########################################################
#################################################################################################################################
def od_get_one(job):
    '''Returns OPEN_DATE (od) (string)'''
    # Locate the information: from Open Date to the first '(' (open parenthesis
    temp = job[job.index('Open Date'):job.index('(')]
    # Get the last element
    od   = temp.split()[-1]
    
    return od