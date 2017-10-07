import urllib2
import os
import sys
from bs4 import BeautifulSoup as bs
import re
import time

# Update cookies and img_cookies before running

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', re.sub('\s+',' ',text))
cookies = {
	"SessionScopeTested": "0",
	"SESSIONSCOPETESTED": "1",
	"HasSessionScope": "0",
	"HASSESSIONSCOPE": "1",
	"CFTOKEN": "778d558ce90a24be-679AC99D-5056-010E-4D23EEE955A4CA99",
	"CFID": "135390",
	"GLOGOUT": "https://webapp.mis.vanderbilt.edu:443/student-search/logout^jsessionid=E03wwyVhW0CCk9BU-tRbycqmb4ACHXIwegJT39a5KsZOPGUkYMqV!1569070806|",
	"JSESSIONID": "E03wwyVhW0CCk9BU-tRbycqmb4ACHXIwegJT39a5KsZOPGUkYMqV!1569070806",
	"BIGipServer~business_apps~webapp_selfserv_9005": "!Nu+0KiGi+Bc/CaN0dd4HTw/aQogjoXl9o2J4ivigq/nuDk2ZlqQzH5SYbNG7kEbszcFWpo0qQn7LyoI="
}
	# "USERPASSWORD": "%247K%2D%27E%40%20%20",
	# "USERNAME": "shiaue",
# "CTOKEN": "d354de491ac1e0fa-436FFA25-5056-010E-4D50671B7F17E1D0"
# 	"GLOGOUT": "https://webapp.mis.vanderbilt.edu:443/student-search/logout^jsessionid=QJOxQWYJ6M4iQVP455WIqmOznysGTgoZwkfviofmKiAcsA_tZibS!1741094770|https://webapp.mis.vanderbilt.edu:443/student-search/logout^jsessionid=hqOx980C4G8iABCXT-AA4UXrM4YVxeuUkn4if-G9_dDai8AqSH6k!1741094770|https://webapp.mis.vanderbilt.edu:443/student-search/logout^jsessionid=_7Kyx2FEqMFM7sa3vl48FFocssasugslT8BQZo8iiulxd2-PLFmA!1741094770|https://webapp.mis.vanderbilt.edu:443/student-search/logout^jsessionid=twC4RR3wTewyCLBZBVlr_TWzYDof-q0JbDxWNHm_JZRxWsCaoJ72!1741094770|",
img_cookies = {
	"GLOGOUT": "https://webapp.mis.vanderbilt.edu:443/student-search/logout^jsessionid=E03wwyVhW0CCk9BU-tRbycqmb4ACHXIwegJT39a5KsZOPGUkYMqV!1569070806|",
	"JSESSIONID": "E03wwyVhW0CCk9BU-tRbycqmb4ACHXIwegJT39a5KsZOPGUkYMqV!1569070806",
	"BIGipServer~business_apps~webapp_selfserv_9005": "!Nu+0KiGi+Bc/CaN0dd4HTw/aQogjoXl9o2J4ivigq/nuDk2ZlqQzH5SYbNG7kEbszcFWpo0qQn7LyoI="
}
opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in cookies.items())))
opener2 = urllib2.build_opener()
#redo session
start = 20785
end = 20786
redo = [15728, 20297, 19010, 19036]
print "start", start, "end", end

# for StudentID in xrange(start,end,1):
for StudentID in redo:
	skip = False
	url = 'https://vanderbilt.datacenter.adirondacksolutions.com/vanderbilt_thd_prod/mobile/CheckInOut.cfm?StudentID='+str(StudentID)
	try:
		response = opener.open(url)
	except urllib2.URLError:
		print "URLError:", StudentID
		time.sleep(2)
		response = opener.open(url)
	webContent = response.read()
	html_list = webContent.splitlines()
	student = ""
	for line in html_list:
		if "<H2>" in line:
			student = remove_tags(line)[1:]
			if len(student) <= 5:
				skip = True			
			break
	if skip is False:	
		soup = bs(webContent, "html.parser")
		images = soup.find_all('img')
		print StudentID, student
		dest_dir = os.path.join(os.getcwd(), "students", student)
		try:
			os.makedirs(dest_dir)
		except OSError:
			pass # already exists
		fname = os.path.join(dest_dir, student+'.html')
		opener2.addheaders = [('Referer', url)]
		opener2.addheaders.append(('Cookie', "; ".join('%s=%s' % (k,v) for k,v in img_cookies.items())))
		for i in images:      #Processing each link and getting the url value
			img_url = i.get('src')
			print "img URL:", img_url
			try:
				data = opener2.open(img_url)
			except urllib2.HTTPError:
				print "urllib2.HTTPError", StudentID, "image"
				time.sleep(2)
				data = opener2.open(img_url)
			data = data.read()
		 	# print "data:", data
		 	with open(os.path.join(dest_dir,student+".jpeg"), "wb") as code:
		 		code.write(data)
		f = open(fname, 'w')
		f.write(webContent)
		f.close()

