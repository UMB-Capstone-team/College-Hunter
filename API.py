import requests
import json
#https://rapidapi.com/sshanbond/api/university-college-list-and-rankings
url ='https://api.data.gov/ed/collegescorecard/v1/'
dataset = 'schools.json?'
filter_params ='latest.student.size__range=10000..'
fields= ['id',
         'school.name',
         '2015.student.size',
         '2020.student.size',
         'location.lat',
         'location.lon',
         'latest.admissions.sat_score.midpoint.math',
         'latest.admissions.act_score.midpoint.math',
         'admission.rate'
         'oops.variable.does.not.exist']
options='&per_page=100&page=0'
api_key= "&api_key=MHgWdG6I183QDehzQpEp1ZYFmSjJqOytO8ICj7Xl"



request_url = url + dataset + filter_params +\
    "&fields="+','.join(fields)+ options + api_key

print(request_url)

resp  = requests.get(request_url)

data  = resp.text
data1 = json.loads(data)

print(data)

#https://api.data.gov/ed/collegescorecard/v1/schools.json?latest.school.state=MA&latestper_page=100&page=0&api_key=MHgWdG6I183QDehzQpEp1ZYFmSjJqOytO8ICj7Xl

#with open('key.txt') as f:
#    api_key ='&api_key='+f.readlines()[0]
#api_key

#print(resp.json())

'''
headers = {
    'Accepts':'application/json',
    'X-RapidAPI-Key':'MHgWdG6I183QDehzQpEp1ZYFmSjJqOytO8ICj7Xl'
}
r = requests.get(url, headers=headers)
'''
