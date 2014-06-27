#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, sys, csv

# Loads the JSON file containing the correspondances

TRANSLIT = json.load(open('ru.json'))
VOWELS = ["А", "Е", "Ё", "И", "О", "У"]

def translit(s, lang):
	
	s = unicode(s, "utf-8")
	s = s.upper()
	prev_char = "none"
	next_char = "none"
	
	out = [""]

	for i in range(0, len(s)):
		
		# if not at end of word
		if (i != len(s) - 1):
			next_char = s[i+1]
		else:
			next_char = "none"

		current_char = s[i]

		translit_choices = ["none"]

		if (current_char in TRANSLIT):

			# Special rules
			if 'before' in TRANSLIT[current_char][lang]:
				if next_char in TRANSLIT[current_char][lang]['before']['letters']:
					translit_choices[0] = TRANSLIT[current_char][lang]['before']['translit']

			if 'beginning' in TRANSLIT[current_char][lang] and prev_char in ["none", " "]:
				translit_choices[0] = TRANSLIT[current_char][lang]['beginning']['translit']
			
			if 'word_ending' in TRANSLIT[current_char][lang]:
				if next_char in [" ", "none"]:
					if prev_char in TRANSLIT[current_char][lang]['word_ending']['after']['letters']:
						translit_choices[0] = TRANSLIT[current_char][lang]['word_ending']['after']['translit']

			if 'after' in TRANSLIT[current_char][lang]:
				if prev_char in TRANSLIT[current_char][lang]['after']['letters']:
					translit_choices[0] = TRANSLIT[current_char][lang]['after']['translit']

			if 'between_vowels' in TRANSLIT[current_char][lang] and next_char in VOWELS and prev_char in VOWELS:
				translit_choices[0] = TRANSLIT[current_char][lang]['between_vowels']['translit']

			if translit_choices[0] == "none":
				translit_choices = TRANSLIT[current_char][lang]['translit']

			if len(translit_choices) > 1:

				for j in range(0, len(out)):
				#For each translit that exists already

					#Duplicate the list and add the new char
					for l in translit_choices:
						out.insert(len(out), "")
						print out
						out[len(out)] = out[j]+l.lower()

			else:
				for j in range(0, len(out)):
					out[j] += translit_choices[0].lower()
		
		elif current_char == " ":
			for j in range(0, len(out)):
					out[j] += " "

		prev_char = current_char

	# End char loop

	for i in range(0, len(out)):
		out[i] = title_case(out[i])
		print lang + "," + out[i] + "," + title_case(s)

	return len(out)

# from http://magnatecha.com/title-case-a-string-in-python/
def title_case(line):
    return ' '.join([s[0].upper() + s[1:] for s in line.split(' ')])

count = 0

# Opens the CSV and parse all the names
if len(sys.argv) > 1:
	
	csv_file = sys.argv[1]

	if len(sys.argv) > 2:
		langs = [sys.argv[2]]
	else:
		langs = ["en", "fr", "de", "lv", "cs", "es"]

	with open(csv_file, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',')
		for row in reader:
			for lang in langs:
				count += translit(row[0], lang)

print "Total variants: " + str(count)