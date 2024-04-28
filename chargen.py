#!/usr/bin/python3
import argparse
import sys
import os
import random
import textwrap
import re

'''
TODO:
'''

class SmartFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

def check_opts():
	parser = argparse.ArgumentParser(description="Generate random character names", formatter_class=SmartFormatter)
	parser.add_argument('-d', action='store_true', help="Show debug output (DEFAULT: FALSE)", default=False)
	parser.add_argument('-n', nargs=1, type=int, help='''R|Number of characters to generate (DEFAULT: 1)''', default=1)
	parser.add_argument('-c', nargs=1, type=str, help='''R|Use specific class: AUGER, MAGE, MARINE, NOMAD, PRIEST, WARRIOR (DEFAULT: ANY)''', default="ANY")
	parser.add_argument('-g', nargs=1, type=str, help='''R|Use specific gender: FEMALE, MALE, NONBINARY (DEFAULT: ANY)''', default="ANY")
	parser.add_argument('-k', nargs=1, type=int, help='''R|Rank of characters to generate (DEFAULT: 1)''', default=1)
	parser.add_argument('-r', nargs=1, type=str, help='''R|Use specific single race: DWARF, ELF, HUMAN, LIZARD, ORC (DEFAULT: ANY)''', default="ANY")
	parser.add_argument('-f', nargs=4, type=str, help='''R|Use specific family racial makeup: DWARF, ELF, HUMAN, LIZARD, ORC (DEFAULT: ANY)''', default=["ANY","ANY","ANY","ANY"])
	parser.add_argument('-b', nargs=4, type=str, help='''R|Specify date of birth (DEFAULT: BLANK)''', default="NONE")
	parser.add_argument('-z', nargs=4, type=str, help='''R|Specify current date (DEFAULT: 1/1/10065)''', default="1/1/10065")




	global args
	args=parser.parse_args()

class characterobj(object):
	char_stats = {}
	char_name=""
	char_race=[]
	char_trait=[]
	char_gender=""
	char_height=0
	char_build=""
	char_weight=0
	char_hair=""
	char_eye=""
	char_diety=""
	char_motive=""
	char_alive=True
	char_elem=""
	char_dob=""
	char_rank=0
	char_exp=0
	char_silver=0
	char_skills={}
	char_dp=0
	char_eu=0
	char_du=0
	char_lf=0
	char_cm=0
	char_mm=0
	char_gm=0
	char_cv=0
	char_mv=0
	char_gv=0

	def roll_char(self,char_class,char_race,char_gender,char_family):
		if(len(self.char_stats)==0):
			# STAT ROLLS

			self.roll_stats()
			self.roll_place()
			print(char_family.count("ANY"))
			if(char_family.count("ANY")<4):
				if(debug): print("DEBUG: MANUAL RACIAL MAKEUP")
				makeup=[]
				for r in char_family:
					if(r == "ANY"):
						add=self.roll_race(False)
					else:
						add=r
					makeup.append(add)
				if(debug): print("DEBUG: RACE IS "+str(makeup))
				self.char_race=makeup

			else:
				if(char_race=='MIXED'):
					makeup=[]
					while(True):
						for z in range(4):
							makeup.append(self.roll_race(False))
						print("AAA"+str(makeup))
						print(makeup[0])
						print(makeup.count("ANY"))
						print(makeup.count(makeup[0]))
						if(makeup.count(makeup[0])==4):
							makeup.clear()
						else:
							break
					self.char_race=makeup
				elif(char_race!='ANY'):
					if(debug): print("DEBUG: MANUAL SINGLE RACE")
					self.char_race = [char_race,char_race,char_race,char_race]
				else:
					if(debug): print("DEBUG: ROLLING RACE")
					self.roll_race(True)
			if(debug): print("DEBUG: char_race: "+str(self.char_race))

			self.roll_trait()

			self.roll_gender()
			if(debug):print("DEBUG: char_gender: "+ self.char_gender)

		else:
			print("ERROR: CHARACTER ALREADY ROLLED")

	def roll_sum(self,number,sides,use):
		rollresults=roll(number,sides)
		while(len(rollresults)>use):
			if(debug): print("DEBUG: DISCARDING ROLL "+str(min(rollresults)))
			rollresults.remove(min(rollresults))
		sum=0
		for i in rollresults:
			sum+=i
		if(debug): print ("SUM is "+str(sum))
		return sum

	def roll_stats(self):
		if(debug): print("DEBUG: STATS")

		if(debug): print ("DEBUG: ROLLING STATS: STR")
		self.char_stats["STR"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: INT")
		self.char_stats["INT"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: PER")
		self.char_stats["PER"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: CSE")
		self.char_stats["CSE"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: HEA")
		self.char_stats["HEA"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: AGI")
		self.char_stats["AGI"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: PWR")
		self.char_stats["PWR"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: COM")
		self.char_stats["COM"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: WIL")
		self.char_stats["WIL"]=self.roll_sum(3,6,3)
		if(debug): print ("DEBUG: ROLLING STATS: PLACED")

	def roll_place(self):
		# PLACED ROLL

		PLACED=self.roll_sum(4,6,3)
		MINSTAT=min(self.char_stats, key=self.char_stats.get)
		if(debug): print("DEBUG: MIN STAT is "+MINSTAT+" with value "+str(self.char_stats[MINSTAT]))
		if(PLACED > self.char_stats[MINSTAT]):
			if(debug): print("DEBUG: PLACED ROLL IS "+str(PLACED)+" WHICH IS LARGER THAN "+MINSTAT+"'S VALUE OF "+str(self.char_stats[MINSTAT]))
			self.char_stats[MINSTAT]=PLACED

	def roll_race(self,set_char):

		# RACE ROLL
		while(True):
			if(debug): print("-----")
			if(debug): print("DEBUG: RACE")
			RACE=self.roll_sum(1,20,1)
			if(debug): print("DEBUG: RACE ROLL: "+str(RACE))
			match RACE:
				case num if 1<= num <= 10:
					if(debug): print("DEBUG: HUMAN")
					if(set_char): self.char_race=['HUMAN','HUMAN','HUMAN','HUMAN']
					else: return 'HUMAN'
					break
				case num if 11 <= num <= 12:
					if(debug): print("DEBUG: ELF")
					if(set_char): self.char_race=['ELF','ELF','ELF','ELF']
					else: return 'ELF'
					break
				case num if 13 <= num <= 14:
					if(debug): print("DEBUG: DWARF")
					if(set_char): self.char_race=['DWARF','DWARF','DWARF','DWARF']
					else: return 'DWARF'
					break
				case num if 15 <= num <= 16:
					if(debug): print("DEBUG: LIZARD")
					if(set_char): self.char_race=['LIZARD','LIZARD','LIZARD','LIZARD']
					else: return 'LIZARD'
					break
				case num if 17 <= num <= 18:
					if(debug): print("DEBUG: ORC")
					if(set_char): self.char_race=['ORC','ORC','ORC','ORC']
					else: return 'ORC'
					break
				case num if 19<= num <= 20:
					if(debug): print("DEBUG: MIXED")
					MRACE=self.roll_sum(1,20,1)
					FRACE=self.roll_sum(1,20,1)
					if(debug): print ("DEBUG: ROLLS: "+str(MRACE)+", "+str(FRACE))

	def roll_trait(self):
		if(debug):print('-----')
		if(debug):print("TRAITS")
		if(self.char_race.count(self.char_race[0])==4):
			# GIVE ALL TRAITS
			if(debug):print ("ALL TRAITS")
			match self.char_race[0]:
				case "HUMAN":
					self.roll_place()
				case "ELF":
					self.char_trait.append("Exceptional PER")
					self.char_trait.append("Distance Judgement")
					self.char_trait.append("Missile Skill")
					self.char_trait.append("Soulless")
				case "DWARF":
					self.char_trait.append("Exceptional HEA")
					self.char_trait.append("Material Sense")
					self.char_trait.append("Armor Construction")
					self.char_trait.append("Great Durability")
				case "LIZARD":
					self.char_trait.append("Exceptional AGI")
					self.char_trait.append("Quickness")
					self.char_trait.append("Water Breathing")
					self.char_trait.append("Homing")
				case "ORC":
					self.char_trait.append("Exceptional WIL")
					self.char_trait.append("Enhanced Smell")
					self.char_trait.append("Physical Viciousness")
					self.char_trait.append("Mental Stubborness")

		else:
			if(debug):print("ROLL TRAITS")
			traits=[]
			for parent in self.char_race:
				print("parent: "+parent)
				Z=0
				while(True):
					t=roll(1,4)
					match (parent,t[0]):
						case ("ELF", 1): add_trait="Exceptional PER"
						case ("ELF", 2): add_trait="Distance Judgement"
						case ("ELF", 3): add_trait="Missile Skill"
						case ("ELF", 4): add_trait="Soulless"
						case ("DWARF", 1): add_trait="Exceptional HEA"
						case ("DWARF", 2): add_trait="Material Sense"
						case ("DWARF", 3): add_trait="Armor Construction"
						case ("DWARF", 4): add_trait="Great Durability"
						case ("LIZARD", 1): add_trait="Exceptional AGI"
						case ("LIZARD", 2): add_trait="Quickness"
						case ("LIZARD", 3): add_trait="Water Breathing"
						case ("LIZARD", 4): add_trait="Homing"
						case ("ORC", 1): add_trait="Exceptional WIL"
						case ("ORC", 2): add_trait="Enhanced Smell"
						case ("ORC", 3): add_trait="Physical Viciousness"
						case ("ORC", 4): add_trait="Mental Stubborness"
						case _: "ERROR"
					if(add_trait in self.char_trait):
						if(False):print()
					else:
						self.char_trait.append(add_trait)
						if(debug): print("DEBUG: ADDING TRAIT "+add_trait)
						break
					if(len(self.char_trait)==4):
						break
					else:
						print(str(len(self.char_trait))+" "+str(self.char_trait))
					Z+=1
					if(Z>10): break
				
		if(debug): print(self.char_trait)

	def roll_gender(self):
		g=roll(1,3)[0]
		if(g == 1):
			self.char_gender = "MALE"
		elif(g == 2):
			self.char_gender = "FEMALE"
		else:
			self.char_gender = "NONBINARY"

def gen_char(char_class,char_race,char_gender,char_rank,char_family):
	back = characterobj()
	back.roll_char(char_class,char_race,char_gender,char_family)

def roll(num,sides):
	results=[]
	for i in range(num):
		rolled=random.randint(1,sides)
		if(debug): print("DEBUG: ROLLED "+str(rolled))
		results.append(rolled)
	return results


if __name__ == "__main__":
	check_opts()

	global debug
	debug = args.d
	# Dump Args
	if(debug):
		print("DEBUG: NUMBER: "+str(args.n));
		print("DEBUG: CLASS: "+str(args.c));
		print("DEBUG: GENDER: "+str(args.g));
		print("DEBUG: RANK: "+str(args.k));
		print("DEBUG: RACE: "+str(args.r));
		print("DEBUG: FAMILY: "+str(args.f));

	# Set n to int

	global n
	if(isinstance(args.n,int)):
		n=args.n
	else:
		n=args.n[0]

	if(n<=0):
		print("ERROR, NUMBER MUST BE INTEGER GREATER THAN 0")
		quit()


	# Test class

	global char_classes
	global char_class
	if(isinstance(args.c,str)):
		char_class=args.c
	else:
		char_class=args.c[0]
	char_classes = {"ANY","AUGER","MAGE","MARINE","NOMAD","PRIEST","WARRIOR"}
	if(not char_class in char_classes):
		print("ERROR, INVALID CLASS")
		quit()

	# Test rank

	global char_rank
	if(isinstance(args.k,int)):
		char_rank=args.k
	else:
		char_rank=args.k[0]

	if(char_rank<=0):
		print("ERROR, RANK MUST BE INTEGER GREATER THAN 0")
		quit()

	# Test gender

	global char_genders
	global char_gender
	if(isinstance(args.g,str)):
		char_gender=args.g
	else:
		char_gender=args.g[0]
	char_genders = {"ANY","FEMALE","MALE","NONBINARY"}
	if(not char_gender in char_genders):
		print("ERROR, INVALID GENDER")
		quit()

	# Test race

	global char_races
	global char_race
	if(isinstance(args.r,str)):
		char_race=args.r
	else:
		char_race=args.r[0]
	char_races = {"ANY","DWARF","ELF","HUMAN","LIZARD","ORC","MIXED"}
	if(char_race in char_races):
		if(False):print("WORKS")
	else:
		print("ERROR, INVALID RACE")
		quit()

	# Test family

	global char_families
	global char_family
	char_family=args.f
	char_familys = {"ANY","DWARF","ELF","HUMAN","LIZARD","ORC","MIXED"}
	for r in char_family:
		if(r in char_familys):
			if(False): print ("WORKS")
		else:
			print("ERROR, INVALID FAMILY RACE: "+r)
			quit()
	for i in range(n):
		if(debug):
			print("DEBUG: GENERATING CHARACTER "+str(i+1)+" of "+str(n));
		back = characterobj()
		back.roll_char(char_class,char_race,char_gender,char_family)