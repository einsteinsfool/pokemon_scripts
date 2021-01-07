import faster_than_requests as r
from bs4 import BeautifulSoup
import re
from itertools import islice

# print letter statistics for chosen array up to 26 elements, starting from most common
def letter_statistics(array):
	array = dict(sorted(array.items(), key=lambda x: x[1], reverse=True))
	for letter in islice(array, 0, 26):
		print(letter, array[letter])
	print(len(array))

source = r.get2str("https://thesilphroad.com/species-stats")
soup = BeautifulSoup(source, "html.parser")

first_letter = {}
first_two_letters = {}
four_letters = {}
last_letter = {}
vowels = []
palindromes = []
stats = {}
names = []
lengths = [0]*12

file = open("pokemon.txt", "w")
file.write("NAME\t\t\t\tID\tMAX CP\tATT\tDEF\tHP\tDEF*HP\tSUM\tPROD\t\tHEIGHT\tWEIGHT\t\tTYPES\n")

divs = soup.findAll(class_= "speciesWrap")
for div in divs:
	if "unreleased" in div["class"]:
		continue

	# fix Pokemon names so they are more parse-friendly
	name = div.find("h1").contents[0].replace("’", "'")
	name = name.replace("♂", " (male)")
	name = name.replace("♀", " (female)")
	if name.startswith("Galarian"):
		name = name.split()[1].title() + " (galar)"
	if name.startswith("Alolan"):
		name = name.split()[1].title() + " (alola)"
	if name.startswith("Mega"):
		continue

	# add Pokemon name without form (only species) to name and name-length tables
	if name.split()[0].lower() not in names:
		names.append(name.split()[0].lower())
		lengths[len(name.split()[0].lower())] += 1

	# count Pokemon starting with each letter and each two letters
	first_letter[name[0]] = first_letter.get(name[0], 0) + 1
	first_two_letters[name[:2]] = first_two_letters.get(name[:2], 0) + 1

	# count each of 4-long substrings in Pokemon names to see which occurr the most times
	for i in range(0, len(name)-3):
		if name[i+3] == ' ':
			break
		four_letters[name[i:i+4].lower()] = four_letters.get(name[i:i+4].lower(), 0) + 1

	# collect Pokemon with 3+ consecutive vowels in names
	pattern = re.compile("^.*[aeiouyAEIOUY]{3,}.*$")
	if pattern.match(name):
		vowels.append(name)

	# collect Pokemon with palindrome names
	if name.split()[0].lower() == name.split()[0].lower()[::-1]:
		palindromes.append(name)

	# collect Pokemon with the same stats
	attack, defense, stamina = div["data-base-attack"], div["data-base-defense"], div["data-base-stamina"]
	stats[(attack, defense, stamina)] = stats.get((attack, defense, stamina), [])
	stats[(attack, defense, stamina)].append(name)

	# save data about each Pokemon in a text file for later manual use
	file.write(name + '\t'*(4-int(len(name)/8)) + div["data-species-num"] + '\t' + div["data-max-cp"] + '\t' + attack + '\t' + defense + '\t' + stamina
				+ '\t' + div["data-tankiness"] + '\t' + div["data-summed-stats"] + '\t' + div["data-multiplied-stats"]
				+ '\t'*(2-int(len(div["data-multiplied-stats"])/8)) + div.find_all("td")[1].contents[0] + '\t' + div.find_all("td")[3].contents[0]
				+ '\t'*(2-int(len(div.find_all("td")[3].contents[0])/8)) + ','.join([element.contents[0] for element in div.find(attrs={"class": "monTypes"}).find_all("div")]) + '\n')

file.close()

# count Pokemon ending with each letter
for name in names:
	last_letter[name[-1]] = last_letter.get(name[-1], 0) + 1

letter_statistics(first_letter)
letter_statistics(first_two_letters)
letter_statistics(last_letter)
letter_statistics(four_letters)

print(vowels)
print(palindromes)

for stat in stats:
	# if there are multiple Pokemon with the same stats and they're not just different forms of the same Pokemon (like Grimer and Alolan Grimer)
	if len(stats[stat]) > 1 and stats[stat][0].split()[0] != stats[stat][1].split()[0]:
		print(stats[stat])

names.sort(key=lambda x: len(list(filter(lambda y: y in "aeiouy", x))), reverse=True) # Pokemon names with most vowels
print(names[:20])
names.sort(key=len) # shortest Pokemon names
print(names[:20])

print(lengths) # Pokemon name length counts
