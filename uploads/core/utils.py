from datetime import datetime
import re

def parse_date(datestr, format='%Y-%m-%d'):
    try:
        return datetime.strptime(datestr, format).date()
    except:
        return None

def parse_category(string):
    p = re.compile('.*(R3C|WRC).*')
    return p.sub(r'\g<1>', string)

def parse_stage(string):
    p = re.compile(r'.*PS(\d*).*')
    return p.sub(r'\g<1>', string)

def parse_car(string):
    p = re.compile(r'.*PS\d*-([\d\s\w]*)-.*')
    return p.sub(r'\g<1>', string)