from pwn import *
import requests
'''
nc geography.cityinthe.cloud 9090
Let's start it off easy, what's your UID value?
c57a5dff8ae62abcd2fa70a663f9dd11
What state has the abbreviation MN?
'''

uid = 'c57a5dff8ae62abcd2fa70a663f9dd11'

p = remote('geography.cityinthe.cloud', 9090)
p.recvuntil("Let's start it off easy, what's your UID value?\r\n")
p.sendline(uid)

'''
$ python solve_geography.py
[+] Opening connection to geography.cityinthe.cloud on port 9090: Done
[*] Switching to interactive mode
Let's start it off easy, what's your UID value?
What state has the following fun fact? Louisville is the state's largest city.
$
[*] Interrupted
[*] Closed connection to geography.cityinthe.cloud port 9090
$ python solve_geography.py
[+] Opening connection to geography.cityinthe.cloud on port 9090: Done
[*] Switching to interactive mode
Let's start it off easy, what's your UID value?
What year was New York established?
$
[*] Interrupted
[*] Closed connection to geography.cityinthe.cloud port 9090
$ python solve_geography.py
[+] Opening connection to geography.cityinthe.cloud on port 9090: Done
[*] Switching to interactive mode
Let's start it off easy, what's your UID value?
What state has the abbreviation LA?
'''

# https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations
abbr_to_full = {
'AL': 'Alabama',
'AK': 'Alaska',
'AZ': 'Arizona',
'AR': 'Arkansas',
'CA': 'California',
'CO': 'Colorado',
'CT': 'Connecticut',
'DE': 'Delaware',
'FL': 'Florida',
'GA': 'Georgia',
'HI': 'Hawaii',
'ID': 'Idaho',
'IL': 'Illinois',
'IN': 'Indiana',
'IA': 'Iowa',
'KS': 'Kansas',
'KY': 'Kentucky',
'LA': 'Louisiana',
'ME': 'Maine',
'MD': 'Maryland',
'MA': 'Massachusetts',
'MI': 'Michigan',
'MN': 'Minnesota',
'MS': 'Mississippi',
'MO': 'Missouri',
'MT': 'Montana',
'NE': 'Nebraska',
'NV': 'Nevada',
'NH': 'New',
'NJ': 'New',
'NM': 'New',
'NY': 'New',
'NC': 'North',
'ND': 'North',
'OH': 'Ohio',
'OK': 'Oklahoma',
'OR': 'Oregon',
'PA': 'Pennsylvania',
'RI': 'Rhode',
'SC': 'South',
'SD': 'South',
'TN': 'Tennessee',
'TX': 'Texas',
'UT': 'Utah',
'VT': 'Vermont',
'VA': 'Virginia',
'WA': 'Washington',
'WV': 'West',
'WI': 'Wisconsin',
'WY': 'Wyoming',
}

def capitals():
    result = dict()
    r = requests.get('https://en.wikipedia.org/wiki/List_of_capitals_in_the_United_States')
    reg = '<tr>\n'
    reg += '<td[^>]*><a[^>]*>([^\n]*)</a></td>\n'
    reg += '<td[^>]*>([^\n]*)</td>\n'
    reg += '<td[^>]*>([^\n]*)</td>\n'
    reg += '<td[^>]*><a[^>]*>([^\n]*)</a></td>\n'
    reg += '<td[^>]*>([^,.]*)</td>\n'
    return re.findall(reg, r.text)

def get_cities():
    result = dict()
    r = requests.get('https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States')
    reg = '<td>[A-Z]*\n</td>\n'
    reg += '<td[^>]*><a[^>]*>([^\n]*)</a>\n</td>\n' # capital
    reg += '<td[^>]*><a[^>]*>([^\n]*)</a>\n</td>\n' # largest
    return re.findall(reg, r.text)

capitals = capitals()
#capitals = [(u'Alabama', u'AL', u'1819', u'Montgomery', u'1846'), (u'Alaska', u'AK', u'1959', u'Juneau', u'1906'), (u'Arizona', u'AZ', u'1912', u'Phoenix', u'1889'), (u'Arkansas', u'AR', u'1836', u'Little Rock', u'1821'), (u'California', u'CA', u'1850', u'Sacramento', u'1854'), (u'Colorado', u'CO', u'1876', u'Denver', u'1867'), (u'Connecticut', u'CT', u'1788', u'Hartford', u'1875'), (u'Delaware', u'DE', u'1787', u'Dover', u'1777'), (u'Florida', u'FL', u'1845', u'Tallahassee', u'1824'), (u'Georgia', u'GA', u'1788', u'Atlanta', u'1868'), (u'Hawaii', u'HI', u'1959', u'Honolulu', u'1845'), (u'Idaho', u'ID', u'1890', u'Boise', u'1865'), (u'Illinois', u'IL', u'1818', u'Springfield', u'1837'), (u'Indiana', u'IN', u'1816', u'Indianapolis', u'1825'), (u'Iowa', u'IA', u'1846', u'Des Moines', u'1857'), (u'Kansas', u'KS', u'1861', u'Topeka', u'1856'), (u'Kentucky', u'KY', u'1792', u'Frankfort', u'1792'), (u'Louisiana', u'LA', u'1812', u'Baton Rouge', u'1880'), (u'Maine', u'ME', u'1820', u'Augusta', u'1832'), (u'Maryland', u'MD', u'1788', u'Annapolis', u'1694'), (u'Massachusetts', u'MA', u'1788', u'Boston', u'1630'), (u'Michigan', u'MI', u'1837', u'Lansing', u'1847'), (u'Minnesota', u'MN', u'1858', u'Saint Paul', u'1849'), (u'Mississippi', u'MS', u'1817', u'Jackson', u'1821'), (u'Missouri', u'MO', u'1821', u'Jefferson City', u'1826'), (u'Montana', u'MT', u'1889', u'Helena', u'1875'), (u'Nebraska', u'NE', u'1867', u'Lincoln', u'1867'), (u'Nevada', u'NV', u'1864', u'Carson City', u'1861'), (u'New Hampshire', u'NH', u'1788', u'Concord', u'1808'), (u'New Jersey', u'NJ', u'1787', u'Trenton', u'1784'), (u'New Mexico', u'NM', u'1912', u'Santa Fe', u'1610'), (u'New York', u'NY', u'1788', u'Albany', u'1797'), (u'North Carolina', u'NC', u'1789', u'Raleigh', u'1792'), (u'North Dakota', u'ND', u'1889', u'Bismarck', u'1883'), (u'Ohio', u'OH', u'1803', u'Columbus', u'1816'), (u'Oklahoma', u'OK', u'1907', u'Oklahoma City', u'1910'), (u'Oregon', u'OR', u'1859', u'Salem', u'1855'), (u'Pennsylvania', u'PA', u'1787', u'Harrisburg', u'1812'), (u'Rhode Island', u'RI', u'1790', u'Providence', u'1900'), (u'South Carolina', u'SC', u'1788', u'Columbia', u'1786'), (u'South Dakota', u'SD', u'1889', u'Pierre', u'1889'), (u'Tennessee', u'TN', u'1796', u'Nashville', u'1826'), (u'Texas', u'TX', u'1845', u'Austin', u'1839'), (u'Utah', u'UT', u'1896', u'Salt Lake City', u'1858'), (u'Vermont', u'VT', u'1791', u'Montpelier', u'1805'), (u'Virginia', u'VA', u'1788', u'Richmond', u'1780'), (u'Washington', u'WA', u'1889', u'Olympia', u'1853'), (u'West Virginia', u'WV', u'1863', u'Charleston', u'1885'), (u'Wisconsin', u'WI', u'1848', u'Madison', u'1838'), (u'Wyoming', u'WY', u'1890', u'Cheyenne', u'1869'), (u'Guam', u'GU', u'1898', u'Hag\xe5t\xf1a', u'1,051'), (u'Northern Mariana Islands', u'MP', u'1947', u'Saipan', u'48,220'), (u'Puerto Rico', u'PR', u'1898', u'San Juan', u'395,326'), (u'U.S. Virgin Islands', u'VI', u'1917', u'Charlotte Amalie', u'18,481')]
print(capitals)
print(len(capitals))
city_data = get_cities()
print(city_data)

abbr_to_full = {code: state for (state, code, stateyear, capital, capitalyear) in capitals}
largest_to_state = dict()
for state in abbr_to_full.values():
    for (state1, code, stateyear, capital, capitalyear) in capitals:
        if state1 != state:
            continue
        found = False
        for (capital1, largest) in city_data:
            if capital1 == capital:
                found = True
                largest_to_state[largest] = state
                break
        if not found:
            largest_to_state[capital] = state
print(largest_to_state)

least_recent_capital = (3000, None, None)
most_recent_capital = (0, None, None)
for (state, code, stateyear, capital, capitalyear) in capitals:
    tmp = int(capitalyear.replace(',', ''), 10)
    if tmp > most_recent_capital[0]:
        most_recent_capital = (tmp, capital, state)
    if tmp < least_recent_capital[0]:
        if state in ['New Mexico']:
            continue
        least_recent_capital = (tmp, capital, state)

for _ in range(1000):
    x = p.recvline()

    print('got %r' % (x,))
    m = re.findall('What state has the abbreviation (..)\\?', x)
    if m:
        s = abbr_to_full[m[0]]
        print('sending %r' % (s,))
        p.sendline(s)
        continue
    m = re.findall('([a-zA-Z ]*) is the capital of which state\\?', x)
    if m:
        state = [state for (state, code, stateyear, capital, capitalyear) in capitals if capital == m[0]][0]
        print('capital %r owner %r' % (m[0], state))
        p.sendline(state)
        continue
    m = re.findall('What year was ([a-zA-Z ]*) established\\?', x)
    if m:
        year = [stateyear for (state, code, stateyear, capital, capitalyear) in capitals if state == m[0]][0]
        print('state %r year %r' % (m[0], year))
        p.sendline(year)
        continue
    m = re.findall('What is the capital of ([a-zA-Z ]*)\\?', x)
    if m:
        capital = [capital for (state, code, stateyear, capital, capitalyear) in capitals if state == m[0]][0]
        print('state %r capital %r' % (m[0], capital))
        p.sendline(capital)
        continue
    m = re.findall('([a-zA-Z ]*) has been the state capital of ([a-zA-Z ]*) since what year\\?', x)
    if m:
        year = [capitalyear for (state, code, stateyear, capital, capitalyear) in capitals if state == m[0][1] and capital == m[0][0]][0]
        print('state %r capital %r year %r' % (m[0][1], m[0][0], year))
        p.sendline(year)
        continue
    if x == "What state has the following fun fact? Memphis is the state's largest city, although Nashville is the largest metro area.\r\n":
        p.sendline('Tennessee')
        continue
    if x == "What state has the following fun fact? Capital's twin city, Minneapolis, is the state's largest.\r\n":
        p.sendline('Minnesota')
        continue
    if x == 'What state has the following fun fact? Third-largest state capital; however, the Cincinnati and Cleveland metropolitan areas are both slightly larger.\r\n':
        p.sendline('Ohio')
        continue
    if x == "What state has the following fun fact? Least populous U.S. state capital. Burlington is the state's largest city.\r\n":
        p.sendline('Vermont')
        continue
    if x == "What state has the following fun fact? Milwaukee is the state's largest city.\r\n":
        p.sendline('Wisconsin')
        continue
    if x == "What state has the following fun fact? Smallest capital by land area. Baltimore is the state's largest city. Capitol building is the oldest in the U.S. still in use.\r\n":
        p.sendline('Maryland')
        continue
    if x == "What state has the following fun fact? Omaha is the state's largest city. It shares the largest metro area with Council Bluffs, Iowa.\r\n":
        p.sendline('Nebraska')
        continue
    if x == "What state has the following fun fact? Only state capital that is not also its county seat (not counting the two state capitals that are independent cities and not located in any county). Detroit is the state's largest city.\r\n":
        p.sendline('Michigan')
        continue
    if x == "What state has the following fun fact? Louisville is the state's largest city.\r\n":
        p.sendline('Kentucky')
        continue
    m = re.findall("What state has the following fun fact?.+? ([a-zA-Z ]*) is the state's largest city", x)
    if m:
        largest = m[0]
        print('largest_to_state[%r] == %r' % (largest, largest_to_state[largest]))
        p.sendline(largest_to_state[largest])
        continue
    if x == 'What state has the following fun fact? Shortest serving current state capital.\r\n':
        print('%r' % (most_recent_capital,))
        p.sendline(most_recent_capital[2])
        continue
    if x == 'What state has the following fun fact? Longest continuously serving capital in the U.S.\r\n':
        print('%r' % (least_recent_capital,))
        p.sendline(least_recent_capital[2])
        continue
    if x == "What state has the following fun fact? Also served as the state's capital from 1636\xe2\x80\x931686 and 1689\xe2\x80\x931776. It was one of five co-capitals 1776\xe2\x80\x931853, and one of two co-capitals 1853\xe2\x80\x931900.\r\n":
        p.sendline('Rhode Island')
        continue
    if x == 'What state has the following fun fact? State capital with the most populous metro area in the U.S.\r\n':
        p.sendline('Georgia')
        continue
    if x == 'What state has the following fun fact? Denver was called Denver City until 1882.\r\n':
        p.sendline('Colorado')
        continue
    if x == 'What state has the following fun fact? Jacksonville is the largest city, and Miami has the largest metro area.\r\n':
        p.sendline('Florida')
        continue
    if x == 'What state has the following fun fact? Charleston is the smallest capital city that is still the most populous city in its state. Huntington has the largest metropolitan area.\r\n':
        p.sendline('West Virginia')
        continue
    if x == 'What state has the following fun fact? Second largest metro area and combined statistical area behind Greenville.\r\n':
        p.sendline('South Carolina')
        continue
    if x == 'What state has the following fun fact? Most populous U.S. state capital and the only capital with more than 1 million citizens.\r\n':
        p.sendline('Arizona')
        continue
    if x == "What state has the following fun fact? Largest capital by municipal land area. Anchorage is the state's largest city.\r\n":
        p.sendline('Alaska')
        continue
    m = re.findall('What year was ([A-Za-z ]*) established\\?',x)
    if m:
        year = [stateyear for (state, code, stateyear, capital, capitalyear) in capitals if state == m[0]][0]
        print('%r established %r' % (m[0], year))
        p.sendline(year)
        continue
    p.interactive()
        
p.interactive()

# got 'Your flag: SKY-GOUS-3768\r\n'
