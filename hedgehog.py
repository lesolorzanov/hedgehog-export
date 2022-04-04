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
            