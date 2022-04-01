import json
import os

class Hedgehog():
   
    def __init__(self,exportlocation):
        self.year=2000
        self.activities=[]
        self.courses=[]
        self.people=[]
        self.person=[]
        self.projects=[]
        self.theses=[]
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
            
#     def readCourses(self):
#         assert self.checkinit()==True            
#         with open(self.path+'courses.json', 'r') as f:
#             self.courses = json.load(f)            
                        
#     def readActivities(self):
#         assert self.checkinit()==True            
#         with open(self.path+'activities.json', 'r') as f:
#             self.activities = json.load(f)   
            
#     def readPeople(self):
#         assert self.checkinit()==True            
#         with open(self.path+'people.json', 'r') as f:
#             self.people = json.load(f)    
            
#     def readProjects(self):
#         assert self.checkinit()==True            
#         with open(self.path+'projects.json', 'r') as f:
#             self.projects = json.load(f)             
            
#     def readTheses(self):
#         assert self.checkinit()==True            
#         with open(self.path+'theses.json', 'r') as f:
#             self.theses = json.load(f)