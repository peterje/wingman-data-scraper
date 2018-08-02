from lxml import etree
from collections import Counter
import pandas as pd
import sys

USERNAME = sys.argv[1]
PATH = sys.argv[2]

parser = etree.HTMLParser()
tree = etree.parse(PATH, parser)

class Match:
	def __init__(
		self,
		map, 
		date, 
		time, 
		wait, 
		duration,
		ping, 
		kills,
		assists, 
		deaths,
		mvps,
		hsp,
		score,
		rounds_for, 
		rounds_against):


		self.map = map
		self.date = date
		self.time = time
		self.wait = wait 
		self.duration = duration
		self.ping = ping
		self.kills = kills
		self.assists = assists
		self.deaths = deaths
		self.mvps = mvps
		self.hsp = hsp
		self.score = score
		self.rounds_for = rounds_for
		self.rounds_against = rounds_against



def nth_parent(t, n):
	for i in range(n):
		t = t.getparent()
	return t

def get_matches(t):
	matches = t.xpath('//*[@id="personaldata_elements_container"]/table/tbody/tr')

	return matches[1:]

def get_map(m):
	map_raw = m.xpath('./td[1]/table/tbody/tr[1]/td')[0].text
	map_format = map_raw.strip().replace("Wingman ", "")

	return map_format

def get_date(m):
	date_raw = m.xpath('./td[1]/table/tbody/tr[2]/td')[0].text
	date_format = date_raw.strip()[:11]

	return date_format

def get_time(m):
	time_raw = m.xpath('./td[1]/table/tbody/tr[2]/td')[0].text
	time_format = time_raw.strip()[11:20]

	return time_format

def get_wait(m):
	wait_raw = m.xpath('./td[1]/table/tbody/tr[3]/td')[0].text
	wait_format = wait_raw.strip().replace("Wait Time: ", "")

	return wait_format

def get_duration(m):
	duration_raw = m.xpath('./td[1]/table/tbody/tr[4]/td')[0].text
	duration_format = duration_raw.strip().replace("Match Duration: ", "")

	return duration_format

def get_usr_stats(m, username):
	for i in range(7):
		try:
			current_usr = m.xpath('./td[2]/table/tbody/tr[$index]/td[1]/div[2]/a', index = i)[0]
			if current_usr.text == username:
				usr_wrapper = nth_parent(current_usr, 3)
				return usr_wrapper, i
		except IndexError:
			pass

	print("error: username not found")
	return 1

def get_ping(usr):
	return usr[1].text

def get_kills(usr):
	return usr[2].text

def get_assists(usr):
	return usr[3].text

def get_deaths(usr):
	return usr[4].text

def get_mvps(usr):
	return 0 if not usr[5].text.replace("★","").strip() else usr[5].text.replace("★","")
	
def get_hsp(usr):
	return usr[6].text

def get_score(usr):
	return usr[7].text

def get_rounds(m, pos):
	score_raw = m.xpath('./td[2]/table/tbody/tr[4]/td')[0].text.strip()
	rounds_for = score_raw[0] if pos < 4 else score_raw[-1]
	rounds_against = score_raw[0] if pos > 4 else score_raw[-1]

	return rounds_for, rounds_against

match_path = get_matches(tree)
matches = []
for m in match_path:
	m_map = get_map(m)
	m_date = get_date(m)
	m_time = get_time(m)
	m_wait = get_wait(m)
	m_duration = get_duration(m)
	usr_stats,usr_pos = get_usr_stats(m, USERNAME)
	m_ping = get_ping(usr_stats)
	m_kills = get_kills(usr_stats)
	m_assists = get_assists(usr_stats)
	m_deaths = get_deaths(usr_stats)
	m_mvps = get_mvps(usr_stats)
	m_hsp = get_hsp(usr_stats)
	m_score = get_score(usr_stats)
	m_for, m_against = get_rounds(m, usr_pos)

	
	m_match = Match(
					m_map,
					m_date,
					m_time,
					m_wait,
					m_duration,
					m_ping,
					m_kills,
					m_assists,
					m_deaths,
					m_mvps,
					m_hsp,
					m_score,
					m_for,
					m_against
					)

	matches.append(m_match)

labels = vars(matches[0])
table = []
table.append(labels)

for m in matches:
	data = vars(m)
	row = []
	for d in data:
		row.append(data[d])
	table.append(row)

headers = table.pop(0)

df = pd.DataFrame(table, columns=headers)


df.to_csv("wingman.csv")
