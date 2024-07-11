from datetime import datetime

def validate_files(request, field, update=False):
    
    #El .copy() crea una copia mutable del objeto
    request = request.copy()
    
    if update:
        if type(request[field]) == str: request.__delitem__(field)
    else:
        #Si el campo es un string, setea que el item que me indicas sea None
        if type(request[field]) == str: request.__setitem__(field, None)
   
    return request
    
def format_date(date):
    date = datetime.strptime(date, '%d/%m/%Y')
    date = f"{date.year}-{date.month}-{date.day}"
    return date