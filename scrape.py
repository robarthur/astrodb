#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib
from urllib.request import urlopen
import datetime
import re
import json

#Assume all wiki formatted dates look like YYYY-mm-dd.
#This seems easier than trying to pattern match things that look like 'age'
def calculate_age(born_string):
    try:
        born = datetime.datetime.strptime(born_string, '%Y-%m-%d')
        today = datetime.date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except:
        return 0

#Misson format looks like Mission 1 (Expidition 1, Expidition 2), Mission 2, Mission 3 (Expidition 1)
#Custom function to only split on commas outside of brackets
def split_mission_list(mission_list):
    missions = []
    depth = 0
    mission = ''
    for c in mission_list:
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif not depth and c in {','}:
            missions.append(mission.strip())
            mission = ''
            continue
        mission += c
    return missions

#Possible conventions..
# x days, y hours, z minutes
# x days y hours z minutes
# xd yh zm
# xd, yh, zm
# xd, y hours and z minutes
def get_minutes_from_time_string(time_string):
    minutes_per_unit = {"m": 1, 'minutes':1, "min":1, "h": 60, "hours":60, "hrs":60, "d": 1440, "days":1440, "w": 10080,"weeks":10080}
    total_time_in_mins = 0
    for k in minutes_per_unit:
        split_time_string = time_string.split(k)
        split_time_string_trimmed = [x.strip(' ,').replace("and", "") for x in split_time_string]
        if len(split_time_string_trimmed)>1:
            last_digits_first_record = re.search(r'\d+$', split_time_string_trimmed[0])
            first_digits_last_record = re.search(r'^\d+', split_time_string_trimmed[1])
            if (last_digits_first_record and first_digits_last_record) or (last_digits_first_record and split_time_string_trimmed[1] == ''):
                total_time_in_mins += minutes_per_unit[k] * int(last_digits_first_record.group(0))
    return(total_time_in_mins)

wiki_page="wiki/List_of_space_travelers_by_name"
site_base="https://en.wikipedia.org/{}".format(wiki_page)
hdr = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request(site_base,headers=hdr)
page = urlopen(req)
soup = BeautifulSoup(page.read(), "html.parser")



for header in soup.find_all('h2'):
    if header.find('span',class_='mw-headline'):
        section_name = header.find('span',class_='mw-headline').get('id')
        if re.match('^[A-Z]$', section_name):
            list_of_st=header.find_next('ul')
            for st in list_of_st.find_all('li'):
                italics = st.find('i')
                if italics:
                        link = italics.find('a', class_=lambda x: x != 'image' and x != 'alt', href=True, recursive=False)
                else:
                    link = st.find('a', class_=lambda x: x != 'image', href=True, recursive=False)
                if not link or not link.text:
                    continue
                #print(link.string)
                #print(link['href'])

                site_base="https://en.wikipedia.org{}".format(link['href'])

                req = urllib.request.Request(site_base,headers=hdr)
                page = urlopen(req)
                soup = BeautifulSoup(page.read(), "html.parser")


                table = soup.find('table', class_='infobox vcard')
                result = {}
                exceptional_row_count = 0
                if table:
                    for tr in table.find_all('tr'):
                       if tr.find('th') and tr.find('td') and not tr.find('th').find('span'):
                            column = tr.find('th').text.replace(" ","").replace("\n","")
                            value = tr.find('td').text
                            #Remove references from value strings
                            value = re.sub('\[[0-9]+\]','',value)
                            result['wiki_'+column] = value 
                            #handle special fields
                            #print(column.lower())
                            if column.lower() == "born":
                                birth_date = value[value.find("(")+1:value.find(")")].strip('age')
                                age = calculate_age(birth_date)
                                result["BirthDate"] = birth_date
                                result["Age"] = age
                            if column.lower() == "missions":
                                result["MissionList"] = split_mission_list(value)
                                result["MissionList"] = [x.strip(' ') for x in result["MissionList"]]
                            if column.lower() == "timeinspace":
                                result['MinutesInSpace'] = get_minutes_from_time_string(value)
                            if column.lower() == "totalevatime":
                                result['TotalEVAMinutes'] = get_minutes_from_time_string(value)
                            if "occupation" in column.lower():
                                print(value)

                    #print(json.dumps(result))