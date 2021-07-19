from mid import app, datetime, time

@app.template_filter("formatdatetime")
def format_datetime(value):
    if value is None:
        return ""
    
    n_t = time.time ()
    offset = datetime.fromtimestamp (n_t ) - datetime.utcfromtimestamp(n_t)
    value = datetime.fromtimestamp ((int (value )/1000 )) + offset
    return value.strftime ('%Y-%m-%d %H:%M:%S')