from datetime import datetime
import re

def parse_date(datestr, format='%Y-%m-%d'):
    try:
        return datetime.strptime(datestr, format).date()
    except:
        return None

def parse_category(string):
    p = re.compile('.*(R3C|WRC|R5|R2|R1|S2000|S1600|WRC_16).*')
    return p.sub(r'\g<1>', string).replace('_', ' ')

def parse_stage(string):
    p = re.compile(r'.*PS(\d*).*')
    return p.sub(r'\g<1>', string).replace('_', ' ')

def parse_car(string):
    p = re.compile(r'.*PS\d*-([\d\s\w]*)-.*')
    return p.sub(r'\g<1>', string).replace('_', ' ')

def parse_youtube_id(string):
    p = re.compile(r'.*(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})')
    return p.sub(r'\g<1>', string)

def parse_rally(string):
    p = re.compile(r'.*replays\/([\w\s\d]*)-.*')
    return p.sub(r'\g<1>', string).replace('_', ' ')