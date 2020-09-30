#use to clean raw XML output from MS Access, and convert to data frame



import pandas as pd
import numpy as np

# read data
data = pd.read_csv('output.xml')
# clean data

#check attributes

attrs = []

with open("output.xml", "r") as f:
    list2 = []
    for item in f:
        if '<attr name=' in item:
            attrs.append(item)

print(set(attrs))

#clean and parse data

df = pd.DataFrame()
#i = 0
action = 0
with open("output.xml", "r") as f:
    resources = []
    #iterate over each line
    for item in f:

    	#clean data
        item = item.replace('   ', '')
        item = item.replace('<value>', '')
        item = item.replace('</value>', '')

        #check which attribute
        if '<searchResultEntry dn=' in item:
            action = 0
            department = ""
            title = ""
            manager = ""
            dn = ""
            ccode = ""
            bufugu = ""
            business = ""
            resources = []
            l = item.split('"')[1::2]
            dn = l[0]


        #set action depending on attibute
        if '<attr name="memberOf">' in item:
            action = 1
            continue
        if '<attr name="department">' in item:
            action = 2    
            continue
        if '<attr name="title">' in item:
            action = 3     
            continue
        if '<attr name="manager">' in item:
            action = 4
            continue
        if '<attr name="extensionAttribute11">' in item:
            action = 5
            continue
        if '<attr name="extensionAttribute6">' in item:
            action = 6
            continue
        if '<attr name="extensionAttribute13">' in item:
            action = 7
            continue
        
        
        if action ==2:
            department = item
            action = 0
        if action ==3:
            title = item
            action = 0
        if action ==4:
            manager = item
            action = 0
            
        if action ==5:
            ccode = item
            action = 0
        if action ==6:
            bufugu = item
            action = 0
        if action ==7:
            business = item
            action = 0
            
        #if resource append to new row  
        if action ==1:
            if '</attr>' in item:
                action = 0
            else:
                resources.append(item)
        
        #if new employee restart    
        if '</searchResultEntry>' in item:
            if resources == []: #checking every employee has access to something
                print("fix this")
                break
            action = 0

            #write each resource from last employee to data frame
            for each in resources:
                df = df.append({'dn':dn,'manager':manager, 'title':title,'bufugu':bufugu,'ccode':ccode,'business':business,'department':department, 'resource':each}, ignore_index=True)

                #print("{} ----{} ----{} ----{} ----{}".format(dn,manager,title,department,each))
                #     print(manager)
           #     i+= 1
        #if i == 100:
         #   break
        #i+= 1
        #print(i)
#print(df.head())   

#save to csv 
df.to_csv('cleaned.csv')
#print(df.describe())
df.head()