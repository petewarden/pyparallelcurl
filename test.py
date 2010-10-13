#!/usr/bin/env python
 
# A test script for the ParallelCurl class
# 
# This example fetches a 100 different results from Google's search API, with no more
# than 10 outstanding at any time.
#
# By Pete Warden <pete@petewarden.com>, freely reusable, see http://petewarden.typepad.com for more

import pyparallelcurl
import pycurl
import urllib
import json
import sys

SEARCH_URL_PREFIX = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&rsz=large&filter=0'

# This function gets called back for each request that completes
def on_request_done(content, url, ch, search):
    
    if content is None:
        print "Fetch error for "+url
        return
    
    httpcode = ch.getinfo(pycurl.HTTP_CODE);    
    if httpcode != 200:
        print "Fetch error "+str(httpcode)+" for '"+url+"'"
        return
    
    responseobject = json.loads(content)
    if 'responseData' not in responseobject or 'results' not in responseobject['responseData']:
        print "No results found for '"+search+"'"
        return
    
    print "********"
    print search+":"
    print "********"
    
    allresponseresults = responseobject['responseData']['results']
    for responseresult in allresponseresults:
        title = responseresult['title']
        print title

# The terms to search for on Google
terms_list = [
    "John", "Mary",
    "William", "Anna",
    "James", "Emma",
    "George", "Elizabeth",
    "Charles", "Margaret",
    "Frank", "Minnie",
    "Joseph", "Ida",
    "Henry", "Bertha",
    "Robert", "Clara",
    "Thomas", "Alice",
    "Edward", "Annie",
    "Harry", "Florence",
    "Walter", "Bessie",
    "Arthur", "Grace",
    "Fred", "Ethel",
    "Albert", "Sarah",
    "Samuel", "Ella",
    "Clarence", "Martha",
    "Louis", "Nellie",
    "David", "Mabel",
    "Joe", "Laura",
    "Charlie", "Carrie",
    "Richard", "Cora",
    "Ernest", "Helen",
    "Roy", "Maude",
    "Will", "Lillian",
    "Andrew", "Gertrude",
    "Jesse", "Rose",
    "Oscar", "Edna",
    "Willie", "Pearl",
    "Daniel", "Edith",
    "Benjamin", "Jennie",
    "Carl", "Hattie",
    "Sam", "Mattie",
    "Alfred", "Eva",
    "Earl", "Julia",
    "Peter", "Myrtle",
    "Elmer", "Louise",
    "Frederick", "Lillie",
    "Howard", "Jessie",
    "Lewis", "Frances",
    "Ralph", "Catherine",
    "Herbert", "Lula",
    "Paul", "Lena",
    "Lee", "Marie",
    "Tom", "Ada",
    "Herman", "Josephine",
    "Martin", "Fanny",
    "Jacob", "Lucy",
    "Michael", "Dora"
]

if len(sys.argv) > 1:
    max_requests = sys.argv[1]
else:
    max_requests = 10

curl_options = {
    pycurl.SSL_VERIFYPEER: False,
    pycurl.SSL_VERIFYHOST: False,
    pycurl.USERAGENT: 'Parallel Curl test script',
    pycurl.FOLLOWLOCATION: True
}

parallel_curl = pyparallelcurl.ParallelCurl(max_requests, curl_options)

for terms in terms_list:
    search = '"'+terms+' is a"';
    search_url = SEARCH_URL_PREFIX+'&'+urllib.urlencode({'q':terms})
    parallel_curl.startrequest(search_url, on_request_done, search)

# This should be called when you need to wait for the requests to finish.
# This will automatically run on destruct of the ParallelCurl object, so the next line is optional.
parallel_curl.finishallrequests()

print 'max_requests='+str(max_requests)
