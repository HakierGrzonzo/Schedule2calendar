import requests, json, bs4

user = {"LoginName": None, "Password": None}
with open("clientSecret.txt") as f:
	lines = f.readlines()
	user['LoginName'] = lines[0].strip()
	user['Password'] = lines[1].strip()

def ParseTable(table):
	res = list()
	table = table.find('main')
	for test in table.find_all('div'):
		event = dict()
		try:
			dateAndDay = test.find('h2').get_text().strip()
			event['date'] = dateAndDay[dateAndDay.find(',') + 1:].strip().replace('.', '-')
			meta = list()
			for div in test.find_all('div', 'daneWiersz'):
				divs = div.find_all('div')
				meta.append(divs[1].get_text().strip())
			event['name'] = meta[0] + ' - ' + meta[2]
			res.append(event)
		except Exception as e:
			pass
	nextWeek_url = table.find('div', 'navigation').find('a', 'button-next').get('href')
	return res, nextWeek_url

def GetTests(user, weeks_forward = 4):
	session = requests.Session()
	root_url = "https://cufs.vulcan.net.pl"
	login_url = "/gliwice/Account/LogOn?ReturnUrl=%2Fgliwice%2FFS%2FLS%3Fwa%3Dwsignin1.0%26wtrealm%3Dhttps%253a%252f%252fuonetplus.vulcan.net.pl%252fgliwice%252fLoginEndpoint.aspx%26wctx%3Dhttps%253a%252f%252fuonetplus.vulcan.net.pl%252fgliwice%252fLoginEndpoint.aspx"
	print('UonetParser: Logging in')
	loggedIn = session.post(root_url + login_url, data = user)
	loggedIn = bs4.BeautifulSoup(loggedIn.text, features="lxml")
	inputs = loggedIn.find_all('input')
	agent = dict()
	for tag in inputs:
		if tag.get('name') != None:
			agent[tag.get('name')] = tag.get('value')
	print('UonetParser: Reaching endpoint')
	try:
		endpoint = session.post(agent['wctx'], data=agent)
	except:
		raise ValueError('UonetParser: Bad username or password')
	endpoint = bs4.BeautifulSoup(endpoint.text, features = "lxml")
	other_root = "https://uonetplus-opiekun.vulcan.net.pl"
	StudentSite = "/gliwice/004001/Start/Index/"
	print('UonetParser: Connecting to "uczeń"')
	Student = session.get(other_root + StudentSite)
	Student = bs4.BeautifulSoup(Student.text, features="lxml")
	res = None
	for nav in Student.find_all('nav'):
		for link in nav.find_all('a'):
			if link.get_text() == 'Sprawdziany':
				res = link.get('href')
				break
	res += '?rodzajWidoku=2'
	events = list()
	print('UonetParser: Getting tests')
	for x in range(weeks_forward + 1):
		TestSite = session.get(other_root + res)
		TestSite = bs4.BeautifulSoup(TestSite.text, features = "lxml")
		event_, res = ParseTable(TestSite)
		events += event_
	return events

if __name__ == '__main__':
	GetTests(user)
