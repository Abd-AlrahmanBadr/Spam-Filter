#!/usr/bin/python3

import os
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import threading

words = {}
sp = 1.0
hp = 1.0
spamCounter = 0.0
hamCounter = 0.0

def prepareDictionary():
	"""
	PrepareDictionary() will get the words from the dataset emails, Calculate the percentage 
		of every word as a spam or ham.
	"""
	files = os.listdir("msgs")
	filesCounter = len(files)
	global spamCounter
	global hamCounter

	for i in range(filesCounter):
		f = open("msgs/" + files[i], "r").read()
		wordExist = {}
		fileWords = readEmail(f)
		wordsCounter = len(fileWords)
		if files[i][:3] != "spm":
			hamCounter = hamCounter + 1.0
			for j in range(wordsCounter):
				if fileWords[j] in wordExist:
					continue;
				wordExist[fileWords[j]] = True
				if fileWords[j] in words:
					words[fileWords[j]][1] = words[fileWords[j]][1] + 1.0
				else:
					words[fileWords[j]] = [0.0, 1.0]
		else:
			spamCounter = spamCounter + 1.0
			for j in range(wordsCounter):
				if fileWords[j] in wordExist:
					continue;
				wordExist[fileWords[j]] = True
				if fileWords[j] in words:
					words[fileWords[j]][0] = words[fileWords[j]][0] + 1.0
				else:
					words[fileWords[j]] = [1.0, 0.0]

	for token in words:
		words[token][0] = words[token][0] / spamCounter
		words[token][1] = words[token][1] / hamCounter

	global sp 
	global hp
	sp = spamCounter / filesCounter
	hp = hamCounter / filesCounter

def readEmail(email):
	"""
	ReadEmail(email) will filter its input(email), delete stop words, numbers and puctuations.
	Returns list of tokens.
	"""
	email = ''.join(c for c in email if c not in punctuation)
	words = email.split()
	stop_words = set(stopwords.words('english'))
	word_tokens = word_tokenize(email)
	texts = [w for w in word_tokens if not w in stop_words]

	EmailWords = []
	for word in texts:
		try:
			int(word)
		except:
			EmailWords.append(word)

	return EmailWords

def binHamSpam(email):
	"""
	binHamSpam(email) will calculate the probability of every word in the 
		input(email) being a spam and being a ham.
	Send these two probablities to isSpamOrHam() to calculate the final probability of the whole email.
	Returns the whole email probability.
	"""
	emailWords = readEmail(email)
	spamPro = 1.0
	hamPro = 1.0
	for word in words:
		if word in emailWords:
			if words[word][0] != 0:
				spamPro = spamPro * words[word][0]
			if words[word][1] != 0:
				hamPro = hamPro * words[word][1]
		else:
			if words[word][0] != 0:
				spamPro = spamPro * (1.0 - words[word][0])
			if words[word][1] != 0:
				hamPro = hamPro * (1.0 - words[word][1])

	return [isSpam(spamPro, hamPro), isHam(spamPro, hamPro)]

def isSpam(spamPro, hamPro):
	"""
	Returns the probability of being this email a spam email based on Bayse Algorithm
	"""
	return ((spamPro * sp) / ((spamPro * sp) + (hamPro * hp)))

def isHam(spamPro, hamPro):
	"""
	Returns the probability of being this email a ham email based on Bayse Algorithm
	"""
	return ((hamPro * hp) / ((hamPro * hp) + (spamPro * sp)))

def learn(spamOrHam, newEmail):
	"""
	Save New Emails as spam or ham.
	"""
	files = os.listdir("msgs")
	filesCounter = len(files)
	Save = True
	for i in range(filesCounter):
		f = open("msgs/" + files[i], "r").read()
		if f == newEmail:
			Save = False
			break

	if Save:
		if spamOrHam:
			f = open("msgs/msg" + str(int(hamCounter + 1)) + ".txt", "w")
			f.write(newEmail)
		else:
			f = open("msgs/spmsg" + str(int(spamCounter + 1)) + ".txt", "w")
			f.write(newEmail)

def main():
	prepareDictionary()
	newEmail = open("Test.txt", "r").read()
	Result = binHamSpam(newEmail)
	ham = Result[0] >= Result[1]

	threading.Thread(target = learn, args = (ham, newEmail), ).start()

	if ham:
		print("This email is ham...")
	else:
		print("This email is spam...")

main()