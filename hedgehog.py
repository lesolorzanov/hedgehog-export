import json
from mimetypes import add_type
import os

from datetime import datetime

dateregex="%Y-%m-%dT%H:%M:%SZ"

activitysubtypes = {
    "conferenceparticipation":
    {
        "specialinvitedspeaker": { "value": "specialinvitedspeaker", "viewValue": "Special invited speaker", "info": ' ', "mandatory": False },
        "refereedpresentation": { "value": "refereedpresentation", "viewValue": "Refereed presentation", "info": ' ', "mandatory": False },
        "non-refereedpresentation": { "value": "non-refereedpresentation", "viewValue": "Non-refereed presentation", "info": ' ', "mandatory": False },
        "attendee": { "value": "attendee", "viewValue": "Attendee", "info": ' ', "mandatory": False },
        "none": { "value": "none", "viewValue": "none", "info": ' ', "mandatory": False },
    }
}

activityTypes ={
    "conferenceparticipationspecialinvitedspeaker":{
        "type": { "value": "conferenceparticipation", "viewValue": "Conference participation", "info": ' ', "mandatory": True },
        "subtype": { "value": "specialinvitedspeaker", "viewValue": "Special invited speaker", "info": ' ', "mandatory": True },
        "conferencename": { "value": "conferencename", "viewValue": "Conference name", "info": ' ', "mandatory": True },
        "title": { "value": "titleofpresentation", "viewValue": "Title of presentation", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbaspeaker)", "viewValue": "People (CBA speaker)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False }
    },

    "conferenceparticipationrefereedpresentation":{
        "type": { "value": "conferenceparticipation", "viewValue": "Conference participation", "info": ' ', "mandatory": True },
        "subtype": { "value": "refereedpresentation", "viewValue": "Refereed presentation", "info": ' ', "mandatory": True },
        "conferencename": { "value": "conferencename", "viewValue": "Conference name", "info": ' ', "mandatory": True },
        "title": { "value": "titleofpresentation", "viewValue": "Title of presentation", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbaspeaker)", "viewValue": "People (CBA speaker)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False }
    },
    "conferenceparticipationnon-refereedpresentation":{
        "type": { "value": "conferenceparticipation", "viewValue": "Conference participation", "info": ' ', "mandatory": True },
        "subtype": { "value": "non-refereedpresentation", "viewValue": "Non-refereed presentation", "info": ' ', "mandatory": True },
        "conferencename": { "value": "conferencename", "viewValue": "Conference name", "info": ' ', "mandatory": True },
        "title": { "value": "titleofpresentation", "viewValue": "Title of presentation", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbaspeaker)", "viewValue": "People (CBA speaker)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False }
    },
    "conferenceparticipationattendee": {
        "type": { "value": "conferenceparticipation", "viewValue": "Conference participation", "info": ' ', "mandatory": True },
        "subtype": { "value": "attendee", "viewValue": "Attendee", "info": ' ', "mandatory": True },
        "conferencename": { "value": "conferencename", "viewValue": "Conference name", "info": ' ', "mandatory": True },
        "internal": { "value": "people(oneorseveralfromcba)", "viewValue": "People (one or several from CBA)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False }
    },
    "conferenceorganisationconferencename": {
        "type": { "value": "conferenceorganisation", "viewValue": "Conference organisation", "info": ' ', "mandatory": True },
        "conferencename": { "value": "conferencename", "viewValue": "Conference name", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbaorganisers)", "viewValue": "People (CBA organisers)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False },
        "external": { "value": "external;,externalorganizers", "viewValue": "External;, external organizers", "info": ' ', "mandatory": False }
    },

    "seminar(fromcbaasinvitedspeaker)": {
        "type": { "value": "seminar(fromcbaasinvitedspeaker)", "viewValue": "Seminar (from CBA as invited speaker)", "info": ' ', "mandatory": True },
        "title": { "value": "title", "viewValue": "Title ", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbaspeaker)", "viewValue": "People (CBA speaker) ", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False }
    },

    "cbaseminar(internalspeaker)":{
        "type": { "value": "cbaseminar(internalspeaker)", "viewValue": "CBA Seminar (internal speaker)", "info": ' ', "mandatory": True },
        "title": { "value": "title", "viewValue": "Title", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbaspeaker)", "viewValue": "People (CBA speaker)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False }
    },

    "cbaseminar(externalspeaker)":{
        "type": { "value": "cbaseminar(externalspeaker)", "viewValue": "CBA Seminar (external speaker)", "info": ' ', "mandatory": True },
        "title": { "value": "title", "viewValue": "Title", "info": ' ', "mandatory": True },
        "external": { "value": "external;externalspeaker", "viewValue": "External; external speaker", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False },
    },
    "visit":{
        "type": { "value": "visit", "viewValue": "Visit", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbastaff)", "viewValue": "People (CBA staff)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False },
        "external": { "value": "external;host", "viewValue": "External; Host", "info": ' ', "mandatory": False },
        "topic": { "value": "topic", "viewValue": "Topic", "info": ' ', "mandatory": False }
    },
    "visitor":{
        "type": { "value": "visitor", "viewValue": "Visitor", "info": ' ', "mandatory": True },
        "internal": { "value": "host(cbastaff)", "viewValue": "Host (CBA staff)", "info": ' ', "mandatory": True },
        "external": { "value": "external", "viewValue": "Visitor", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": True },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False },
        "topic": { "value": "topic", "viewValue": "Topic", "info": ' ', "mandatory": False },
    },
    "committee":{
        "type": { "value": "committee", "viewValue": "Committee", "info": ' ', "mandatory": True },
        "title": { "value": "title(committeename)", "viewValue": "Title (committee name)", "info": ' ', "mandatory": True },
        "internal": { "value": "people(cbastaff)", "viewValue": "People (CBA staff)", "info": ' ', "mandatory": True },
        "begindate": { "value": "startdate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False }
    },
    "other":{
        "type": { "value": "other", "viewValue": "Other", "info": ' ', "mandatory": True },
        "title": { "value": "title", "viewValue": "Title", "info": ' ', "mandatory": True },
        "internal": { "value": "internal", "viewValue": "CBA People", "info": ' ', "mandatory": False },
        "begindate": { "value": "begindate", "viewValue": "Start date", "info": ' ', "mandatory": True },
        "enddate": { "value": "enddate", "viewValue": "End date", "info": ' ', "mandatory": True },
        "location": { "value": "location", "viewValue": "Location", "info": ' ', "mandatory": False },
        "comment": { "value": "comment", "viewValue": "Comment", "info": ' ', "mandatory": False },
        "images": { "value": "images", "viewValue": "Images", "info": ' ', "mandatory": False },
        "external": { "value": "external", "viewValue": "External person", "info": ' ', "mandatory": False },
        "topic": { "value": "topic", "viewValue": "Topic", "info": ' ', "mandatory": False }
    }
}

def escapeToLatex(char):
    return

def findAndLenGtZero(astring,adict):
    if astring in adict:
        if len(adict[astring])>0:
            return True
    return False


def activityStructure(activitytype,subtype):
    combined=activitytype+subtype
    if combined in activityTypes:
        return activityTypes[combined]
    else:
        return None
    
    

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
        if(oid in self.peopleMap):
            person=self.peopleMap[oid]
            if "name" in person:
                return person["name"]
            else:
                return oid
        else:
            return oid+" oid not found!"
             
    def printExternal(self,ext):
        extstring=""
        if "honorific" in ext:
            extstring+=ext['honorific']+". "

        extstring+=ext["name"]+", "
        
        for k in ["affiliation","institution","city","country"]:
            if k in ext:
                extstring+=ext[k]+', '
                
        extstring=extstring[:-1]+"; "
        
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
        _id=proj["_id"]["$oid"]
        
        pstring ="\\item \n"
        pstring+="\\label{ proj:"+str(_id)+" } \n"
        pstring+="\\textbf{"+proj['title']+" } \\\\ \n"
        
        if(len(proj["people"])>0):
            peoplestring=""
            for oid in proj["people"]:
                peoplestring+=self.printPerson(oid)+", "
            peoplestring=peoplestring[:-2]
            pstring+=peoplestring+" \n"
        
        if(len(proj["external"])>0):
            extstring="\\ppartner {"
            for ext in proj["external"]:
                extstring+=self.printExternal(ext)
            extstring+="}\n"
            pstring+=extstring
            
    
        if "funding" in proj:
            pstring+="\\ffunding{ "+proj['funding']+" }\n"
            
        pstring+="\\pperiod{"

        if "enddate" in proj:
            pstring+=self.printDates(proj['begindate']['$date'],proj['enddate']['$date'])
        else:
            pstring+=proj['begindate']['$date'].split("T")[0]+" - Current"
        pstring+="\}\n"   
        
        pstring+="\\aabstract{ "+proj['description']+"} "  
        if "images" in proj:
            if len(proj["images"])>0:
                pstring+="See Figure~\\ref {fig:"+str(_id)+" }." 
                                
        pstring+="}\n" 
        
        
        if findAndLenGtZero("images", proj):
            pstring+="\\begin{figure*}[!h]\n" 
            pstring+="\\centering\n"
            pstring+="\\includegraphics[width=0.55\textwidth]{ "
            pstring+=self.imageDir+"/"+proj['images'][0]+"}\n"
            pstring+="\\caption{ "+proj['title']+" }\n"
            pstring+="\\label{fig:"+str(_id)+" }." 
            pstring+="\\end{figure*}\n"
                
        return pstring

    def printThesis(self,t):
        thes=self.theses[t]
        """
        thesisTypes =[
            {"value":'bachelor',  "viewValue": 'Bachelor',  "info":"Habitually, bachelor theses have: One or two students; Supervisor; Reviewer; Abstract"},
            {"value":'master',    "viewValue": 'Master',    "info":"Habitually, master theses have: One or two students; Supervisor; Reviewer; Abstract"},
            {"value":'licenciate',"viewValue": 'Licenciate',"info":"Habitually, licenciate thesis have: One student; Supervisor; Co-supervisors; Opponent;Committee; Chair; Publisher;DiVA link; Abstract"},
            {"value":'phd',       "viewValue": 'PhD',       "info":"Habitually, Doctoral thesis have: One student; Supervisor; Co-supervisors; Opponent; Committee; Chair; Publisher;DiVA link; Abstract"}
        ]
        """

        tstring ="\\item\n"
        if "defensedate" in thes:
            tstring+="{\\em Date:} "
            tstring+=thes['defensedate']['$date'].split("T")[0]+"~\\\\\n"

        if "title" in thes:
            tstring+="{\\bf "
            tstring+=thes['title']+"} \\\\\n"

        if findAndLenGtZero("student",thes):
            tstring+="{\\em Student: }"

            if type(thes["student"]) is list:
                for s in thes["student"]:
                    tstring+="{\\bf "+self.printPerson(s)+", "
                tstring+="}\\\\\n"
            else:
                tstring+="{\\bf"+self.printPerson(thes["student"])+"}\\\\\n"


        if findAndLenGtZero("studentexternal",thes):
            tstring+="{\\em Student: }"
            if type(thes["studentexternal"]) is list:
                for s in thes["studentexternal"]:
                    tstring+="{\\bf "+s+", "
                tstring+="}\\\\\n"
            else:
                tstring+="{\\bf"+thes["studentexternal"]+"}\\\\\n"


        if findAndLenGtZero("supervisor",thes):
            tstring+="{\\em Supervisor: } "
            if type(thes["supervisor"]) is list:
                for s in thes["supervisor"]:
                    tstring+=self.printPerson(s)+", "
                tstring+="\\\\\n"
            else:
                tstring+=self.printPerson(thes["supervisor"])+" \\\\\n"

        if findAndLenGtZero("assistantsupervisors",thes):
            tstring+="{\\em Assistant Supervisors: } "
            if type(thes["assistantsupervisors"]) is list:
                for s in thes["assistantsupervisors"]:
                    tstring+=self.printPerson(s)+", "
                tstring+="\\\\\n"
            else:
                tstring+=self.printPerson(thes["assistantsupervisors"])+"}\\\\\n"
            

        if findAndLenGtZero("assistantsupervisorsexternal",thes):
            tstring+="{\\em External Assistant Supervisors: }"
            if type(thes["assistantsupervisors"]) is list:
                for s in thes["assistantsupervisorsexternal"]:
                    tstring+=s+", "
            else:
                tstring+=thes["assistantsupervisorsexternal"]
            tstring+=" \\\\\n"

        if "opponent" in thes:
            tstring+="{\\em Opponent:} "+self.printExternal(thes["opponent"])
            tstring+=" \\\\\n"

        if findAndLenGtZero("committee",thes):
            tstring+="{\\em Committee:} \n"
            for i in range(len(thes["committee"])):
                tstring+="("+str(i)+") "+self.printExternal(thes["committee"][i])+" \n"
            tstring+=" \\\\\n"

        if "chair" in thes:
            tstring+="{\\em Chair:}"+self.printPerson(thes["chair"])
            tstring+=" \\\\\n"

        if "publisher" in thes:
            tstring+="{\\em Publisher:} "+thes["publisher"] 
            tstring+=" \\\\\n"

        if "diva" in thes:
            tstring+="{\\em DiVA:} "+thes["diva"] 
            tstring+=" \\\\\n"

        if "abstract" in thes:
            tstring+="{\\em Abstract:}\n "+thes["abstract"] 
            tstring+=" \\\\\n"

        return tstring

    def printActivity(self,a,printimage=False):
        #one of the most difficult ones :(
        act=self.activities[a]
        atype=act["type"]
        asubtype=""
        _id=act["_id"]["$oid"]
        if "subtype" in act:
            asubtype=act["subtype"]

        #get type, and pray
        actstruct=activityStructure(atype,asubtype)
        if actstruct is None:
            print("could not find activity structure for activity",act["_id"]["$oid"])
            return

        actstring="%-- activity: "+_id+" \n"

        # keys=list(actstruct.keys())

        if ("title" in act):# and ("title" in keys):
            actstring+="{\\bf "+act["title"]+" } \\\\ \n"
            # keys.remove("title")
        if ("conferencename" in act):# and ("conferencename" in keys):
            actstring+="{\\em "+actstruct["conferencename"]["viewValue"]+" :} "+act["conferencename"]+"  \\\\ \n"
            # keys.remove("conferencename")

        # if "subtype" in keys:
        #     keys.remove("subtype")
        
                       
        if findAndLenGtZero("internal",act):
            actstring+="{\\em "+actstruct["internal"]["viewValue"]+" :}"
            for internal in act["internal"]:                       
                actstring+="{\\em :}"+self.printPerson(internal)
            actstring+=" \\\\\n"
        elif findAndLenGtZero("external",act):
            actstring+="{\\em "+actstruct["external"]["viewValue"]+" :}"
            for external in act["external"]:                       
                actstring+="{\\em :}"+self.printExternal(external)
            actstring+=" \\\\\n"
        elif findAndLenGtZero("images",act) and printimage:            
            actstring+="\\begin{figure*}[!h]\n" 
            actstring+="\\centering\n"
            actstring+="\\includegraphics[width=0.55\textwidth]{ "
            actstring+=self.imageDir+"/"+act['images'][0]+"}\n"
            actstring+="\\caption{ "+act['title']+" }\n"
            actstring+="\\label{fig:"+str(_id)+" }." 
            actstring+="\\end{figure*}\n"
            
        elif key == "begindate":
            if "enddate" in act:
                actstring+=self.printDates(act['begindate']['$date'],act['enddate']['$date'])
                keys.remove("enddate")
            else:
                actstring+=act['begindate']['$date'].split("T")[0]
            actstring+="\\\\ \n"   
        else:
            actstring+="{\\em"+actstruct[key]["viewValue"]+" :}"+str(act[key])+"\\\\ \n"

        return actstring




            
    def findAllForYear(self,year=None,verbose=False):
        
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
            if verbose:
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
            if verbose:
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
            if verbose:
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
            if verbose:
                print("could not parse projects:\n")
                for c in probcourses:                
                     print(self.courses[c])


        
        
            
            