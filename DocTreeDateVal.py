# Comment From Visual code 
# comment from Textmate


import time
def is_date_valid(year, month, day):
    this_date = '%d/%d/%d' % (month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True
        
print(is_date_valid(2017,11,31))