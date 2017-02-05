#!/usr/bin/Python
import sys
import os
import re
import random

#Applicant Object
class Applicant:
    def __init__(self):
        self.name=''
        self.email=''
        self.degree=0  #1 = Bachelors, 2=Master's, 3=PhD etc.
        self.tech_skills = []
        self.has_github = 0

#Open all files in a directory 'resume_data'
#os.chdir(os.path.dirname(os.getcwd()))
for filename in os.listdir(os.path.join(os.getcwd(), 'resume_data/')):
    #Gather data about Applicant
    path = os.path.join('../', os.getcwd())
    path = os.path.join(path, 'resume_data/')
    f = open (os.path.join(path, filename), 'r')

    temp = Applicant()

    #Assuming name is first line
    text = f.readlines()
    temp.name = text[0]
    for line in text[1:]:
        #Parse for email
        res = re.search("([^@|\s]+@[a-zA-Z]+\.[a-zA-Z\.]+)", line, re.I)
        if(res):
            temp.email = res.group(1)

        #Parse for bachelor's degree
        res = re.search("(B\.A\.|Bachelor's|Bachelors|Bachelor|B\.S\.|A\.B\.|Sc\.B\.|AB|ScB|BS|BSc|BA)", line, re.I)
        if(res):
            temp.degree = 1

        #Parse for Master's degree
        res = re.search("(M\.A\.|Master's|Masters|Master|M\.S\.|A\.M\.|Sc\.M\.|AM|ScM|MS|MSc|MA)", line, re.I)
        if(res):
            temp.degree = 2

        #Parse for tech skills
        line = line.lower()
        skills = ["java","python","go","golang","c","c\+\+","c#","c/c\+\+",
                    "ruby","javascript","jquery","html","css","sql","nosql","php",
                    "perl","rails","mvc","django","apache","aws","heroku","spark",
                    "kafka","redis","cassandra","mongodb","rabbitmq","meteor.js",
                    "meteor","node.js","react.js","d3.js","mysql","sympfony","numpy",
                    "hadoop","rest","restful","json","xml","ios","gradle","maven","android",
                    "pyramid","bash","tensorflow","r","matlab",'rust','.net',"tornado","unix",
                    "linux","git","vcs","statistics","machine learning","distributed systems",
                    "networking","operating systems","algorithms","data structures","scala",
                    "coffeescript","framer.js","swift","objective-c","mongo"]
        for skill in skills:
            res = re.search("[^\w-]"+skill, line, re.I)
            if(res):
                temp.tech_skills+=[skill]
        temp.tech_skills = list(set(temp.tech_skills))

        #Parse for github
        res = re.search("(github|Github)", line, re.I)
        if(res):
            temp.has_github = 1

    f.close()

    #Decide if Accept or Reject
    outcome = random.randint(0,1)
    #Update the stats file
    f = open("stats.txt", 'r')
    text = []
    for line in f.readlines():
        line = line.split()
        text += [[line[0],line[1],line[2]]]
    f.close()

    f = open("stats.txt", 'w')
    for index in range(len(text)):
        if(index == 0):
            skill = 1
        else:
            skill = text[index][0] in temp.tech_skills
        if(skill):
            skill = 1
        else:
            skill = 0
        s = "%s %d %d\n" %(text[index][0], int(text[index][1]) + skill*(1-outcome), int(text[index][2]) + skill*outcome)
        f.write(s)
    f.close()

    #Update user email list
    if(outcome == 0):
        f = open("reject_email.txt", 'w')
    else:
        f = open("accept_email.txt", 'w')
    s = "%s\n" %(temp.email)
    f.write(s)
    f.close()

    #Delete the file from resume_data
    os.remove(os.path.join(path, filename))
    temp.tech_skills = []

print "Parser has ended."
sys.stdout.flush()
