import json
import os

from datetime import datetime

dateregex="%Y-%m-%dT%H:%M:%SZ"

def escapeToLatex(char):
    return
    

class Hedgehog():
   
    def __init__(self,exportlocation):
        self.year=2000
        
        self.activities=[]
        self.courses=[]
        self.people=[]
        self.peopleMap={}
        self.person=[]
        self.projects=[]
        self.theses=[]
        self.imageDir="images"
        
        self.activities_valid_indices=[]
        self.courses_valid_indices=[]
        self.people_valid_indices=[]
        self.projects_valid_indices=[]
        self.theses_valid_indices=[]
        
        self.path=""
        self.initialized=False
        
        if not os.path.isdir(exportlocation):
            print("Can't find "+exportlocation)
        else:
            self.path=exportlocation
            self.initialized=True
            
            self.readjson("activities")
            self.readjson("courses")
            self.readjson("people")
            self.readjson("projects")
            self.readjson("theses")


    def __getitem__(self, key):
        return getattr(self, key)
            
    def checkinit(self):
        if not self.initialized:
            pathx="None"
            if self.path:
                pathx=self.path
            print("You need to initialize a Hedghog object, with a loction to the exported json files. Current location is "+pathx)
            return False
        else:
            return True
        
        
    def readjson(self,name):
        assert self.checkinit()==True
        assert type(name) is str, "Name must be string"
            
        with open(self.path+name+'.json', 'r') as f:
            setattr(self,name,json.load(f))
            
        #make a people map
        for p in self.people:
            self.peopleMap[p["_id"]['$oid']]=p
            
            
    def printPerson(self,oid):
        person=self.peopleMap[oid]
        if "name" in person:
            return person["name"]
        else:
            return oid
        
        
    def printExternal(self,ext):
        extstring=""
        if "honorific" in ext:
            extstring+=f"{ext['honorific']} "

        extstring+=f'{ext["name"]},'
        
        for k in ["affiliation","institution","city","country"]:
            if k in ext:
                extstring+=f'{ext[k]},'
                
        extstring=extstring[:-1]+". "
        
        return extstring


    def printDates(self, begin ,end):
        yb=datetime.strptime(begin,dateregex).year
        ye=datetime.strptime(end,dateregex).year
        datestr=begin.split("T")[0]+" - "
        if ye<=self.year:
            datestr+=end.split("T")[0]
        elif ye> self.year:
            datestr+="Current"
            
        return datestr
        
            
            
    def printProject(self,p):
        proj=self.projects[p]
        
        pstring =f"{bs}item \n"
        pstring+=f"{bs}label{{ proj:{p} }} \n"
        pstring+=f"{bs}textbf{{ {proj['title']} }} \\ \n"
        
        if(len(proj["people"])>0):
            peoplestring=""
            for oid in proj["people"]:
                peoplestring+=self.printPerson(oid)+", "
            peoplestring=peoplestring[:-2]
            pstring+=f"{peoplestring} \n"
        
        if(len(proj["external"])>0):
            extstring=f"\ppartner {{"
            for ext in proj["external"]:
                extstring+=self.printExternal(ext)
            extstring+=f"}}\n"
            pstring+=extstring
            
    
        if "funding" in proj:
            pstring+=f"{bs}ffunding{{ {proj['funding']} }}\n"
            
        pstring+=f"{bs}pperiod{{"
        if "enddate" in proj:
            pstring+=self.printDates(proj['begindate']['$date'],proj['enddate']['$date'])
        else:
            pstring+=proj['begindate']['$date'].split("T")[0]+" - Current"
        pstring+=f"}}\n"   
        
        pstring+=f"{bs}aabstract{{ {proj['description']} "  
        if "images" in proj:
            if len(proj["images"])>0:
                pstring+=f"See Figure~\ref {{fig:{p} }}." 
                                
        pstring+=f"}}\n" 
        
        if "images" in proj:
            if len(proj["images"])>0:
                pstring+=f"{bs}begin{{figure*}}[!h]\n" 
                pstring+=f"{bs}centering\n"
                pstring+=f"{bs}includegraphics[width=0.55\textwidth]{{ {self.imageDir}/{proj['images'][0]} }}\n"
                pstring+=f"{bs}caption{{ {proj['title']} }}\n"
                pstring+=f"{bs}label{{fig:{p} }}\n"
                pstring+=f"{bs}end{{figure*}}\n"
                
        return pstring


        
        

        
        
            
            
    def findAllForYear(self,year=None):
        
        inyear=year
        if year is None:
            inyear=self.year
        print(f"The year is{inyear}")
        
        # |  __ \         (_)         | |      
        # | |__) | __ ___  _  ___  ___| |_ ___ 
        # |  ___/ '__/ _ \| |/ _ \/ __| __/ __|
        # | |   | | | (_) | |  __/ (__| |_\__ \
        # |_|   |_|  \___/| |\___|\___|\__|___/
        #                _/ |                  
        #               |__/                  
               
        self.projects_valid_indices=[]
        probprojs=[]
        for p in range(len(self.projects)):
            proj=self.projects[p]
            try:
                y=datetime.strptime(proj["begindate"]['$date'],dateregex).year
                if y==self.year:
                    self.projects_valid_indices.append(p)
            except:
                probprojs.append(p)

        if(len(probprojs)>0):
            print(f"there were {len(probprojs)} problems.")
            print("could not parse projects:\n")
            for p in probprojs:                
                 print(self.projects[p])
                    
                    
        #      /\       | | (_)     (_) | (_)          
        #     /  \   ___| |_ ___   ___| |_ _  ___  ___ 
        #    / /\ \ / __| __| \ \ / / | __| |/ _ \/ __|
        #   / ____ \ (__| |_| |\ V /| | |_| |  __/\__ \
        #  /_/    \_\___|\__|_| \_/ |_|\__|_|\___||___/
                
        self.activities_valid_indices=[]
        probacts=[]
        for a in range(len(self.activities)):
            act=self.activities[a]
            try:
                y=datetime.strptime(act["begindate"]['$date'],dateregex).year
                if y==self.year:
                    self.activities_valid_indices.append(a)
            except:
                probacts.append(a)

        #myhedgehog.projects=projects

        if(len(probacts)>0):
            print(f"there were {len(probacts)} problems.")
            print("could not parse activities:\n")
            for a in probacts:                
                 print(self.activities[a])
                    
                    
        #   ________            
        #  |__   __| |             (_)    
        #     | |  | |__   ___  ___ _ ___ 
        #     | |  | '_ \ / _ \/ __| / __|
        #     | |  | | | |  __/\__ \ \__ \
        #     |_|  |_| |_|\___||___/_|___/

        self.theses_valid_indices=[]
        probtheses=[]
        for t in range(len(self.theses)):
            thesis=self.theses[t]
            try:
                y=datetime.strptime(thesis["defensedate"]['$date'],dateregex).year
                if y==self.year:
                    self.theses_valid_indices.append(t)
            except:
                probtheses.append(t)

        #myhedgehog.projects=projects

        if(len(probtheses)>0):
            print(f"there were {len(probtheses)} problems.")
            print("could not parse theses:\n")
            for t in probtheses:                
                 print(self.theses[t])
                    
                    
        #   _____                               
        #  / ____|                              
        # | |     ___  _   _ _ __ ___  ___  ___ 
        # | |    / _ \| | | | '__/ __|/ _ \/ __|
        # | |___| (_) | |_| | |  \__ \  __/\__ \
        #  \_____\___/ \__,_|_|  |___/\___||___/
                    
            
        self.courses_valid_indices=[]
        probcourses=[]
        for c in range(len(self.courses)):
            course=self.courses[c]
            try:
                y=datetime.strptime(course["begindate"]['$date'],dateregex).year
                if y==self.year:
                    self.courses_valid_indices.append(c)
            except:
                probcourses.append(c)

        #myhedgehog.projects=projects

        if(len(probcourses)>0):
            print(f"there were {len(probcourses)} problems.")
            print("could not parse projects:\n")
            for c in probcourses:                
                 print(self.courses[c])
                    

        
        
            
            