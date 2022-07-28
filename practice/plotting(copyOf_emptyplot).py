# import all necessary libaries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# refining dataframe
# read the files
hp = pd.read_csv('dataset/Characters.csv', delimiter = ";")

# reduce the dataframe to the necessary size
hp = hp[['Gender', 'House', 'Blood status', 'Hair colour', 'Eye colour', 'Loyalty']]

# replace some column labels so that it is easier to code e.g. when using hp.Blood_status.values.tolist()
hp.columns = hp.columns.str.replace("Blood status", "Blood_status")
hp.columns = hp.columns.str.replace("Hair colour", "Hair_colour")
hp.columns = hp.columns.str.replace("Eye colour", "Eye_colour")

# unit ambiguous labels to one label
hp["Blood_status"] = hp["Blood_status"].replace(["Pure-blood or Half-blood", "Pure-blood or half-blood", "Half-blood or pure-blood"], "Pure-blood or half-blood")
hp["Blood_status"] = hp["Blood_status"].str.strip(']').str.strip('[')

# remove rows with certain labels, which in this case are outliers
outlier1 = ["Unknown", "Part-Human (Half-giant)", "Quarter-Veela", "Part-Goblin", "Squib", "Muggle"]
for i in outlier1:
    hp = hp.loc[hp['Blood_status'] != i]

# unit ambiguous labels to one label
hp["Hair_colour"] = hp["Hair_colour"].replace(["Blond", "White-blond", "Silvery-blonde", "White blond", "Straw blond", "Reddish-blonde", "Dirty-blonde", "Sandy", "Straw-coloured"], "Blonde")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Grey", "Silver", "Silver| formerly auburn", "Silver| formerly black", "White (balding)", "Iron grey", "White"], "Silver / White / Grey")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Red ", "Ginger", "Red brown", "Brown/greying", "Auburn"], "Red")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Bald", "Colourless and balding"], "Bald")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Black", "Jet-black", "Colourless and balding"], "Dark")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Mousy brown", "Reddish-brown", "Tawny", "Mousy", "Light brown flecked with grey"], "Brown")

# remove rows with certain labels, which in this case are outliers
outlier2 = ["Variable", "Green"]
for i in outlier2:
    hp = hp.loc[hp['Hair_colour'] != i]

# unit ambiguous labels to one label
hp["Eye_colour"] = hp["Eye_colour"].replace(["Bright green", "Gooseberry"], "Green")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Bright brown", "Scarlet ", "Ruddy", "Hazel"], "Brown")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Black"], "Dark")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Bright Blue", "Grey/Blue[", "Astonishingly blue"], "Blue")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Pale silvery", "Silvery", "Dark Grey"], "Grey")

# remove rows with certain labels, which in this case are outliers
outlier3 = ["One dark, one electric blue", "Pale, freckled", "Yellowish", "Yellow"]
for i in outlier3:
    hp = hp.loc[hp['Eye_colour'] != i]

# unit ambiguous labels to one label
hp.Loyalty = hp.Loyalty.apply(lambda x: "Dumbledore's Army" if not pd.isnull(x) and ("Dumbledore" in x) else x) 
hp.Loyalty = hp.Loyalty.apply(lambda x: "Dumbledore's Army" if not pd.isnull(x) and ("Phoenix" in x) else x) 
hp.Loyalty = hp.Loyalty.apply(lambda x: "Lord Voldemort" if not pd.isnull(x) and ("Voldemort" in x) else x)
hp["Loyalty"] = hp["Loyalty"].replace(["Minister of Magic"], "Ministry of Magic")
hp["Loyalty"] = hp["Loyalty"].replace(["Hogwarts School of Witchcraft and Wizardry"], "Hogwarts School")

# remove rows with certain labels, which in this case are outliers
outlier4 = ["Gellert Grindelwald's Acolytes"]
for i in outlier4:
    hp = hp.loc[hp['Loyalty'] != i]

# preparing lists to insert the data in order of 'Gender', 'Blood status', 'Hair colour', 'Eye colour', 'Loyalty' 
# create 2D house lists of traits in each hous [['Gender'], ['Blood status'], ['Hair colour'], ['Eye colour'], ['Loyalty']]
gryffindor = [] 
hufflepuff = [] 
ravenclaw = [] 
slytherin = []

# get the list of houses in order to sort them according to the gender, blood status, hair colour, eye colour, and loyalty
houselist = np.unique(hp.House.values.tolist())
houselist = houselist[1:5] # remove 'Durmstrang Institute' and 'nan'

gender_index = 0 # for future indexing of each house list
gender = np.unique(hp.Gender.values.tolist())
gender = [x for x in gender if str(x) != 'nan'] # remove 'nan'

bloodstatus_index = 1
bloodstatus = np.unique(hp.Blood_status.values.tolist())
bloodstatus = [x for x in bloodstatus if not ' or ' in str(x)] # remove strings with ' or '
bloodstatus = [x for x in bloodstatus if not ' or ' in str(x)] # remove strings with ' or '
bloodstatus = [x for x in bloodstatus if str(x) != 'nan'] # remove 'nan'

haircolour_index = 2
haircolour = np.unique(hp.Hair_colour.values.tolist())
haircolour = [x for x in haircolour if str(x) != 'nan'] # remove 'nan'

eyecolour_index = 3
eyecolour = np.unique(hp.Eye_colour.values.tolist())
eyecolour = [x for x in eyecolour if str(x) != 'nan'] # remove 'nan'

loyalty_index = 4
loyalty = np.unique(hp.Loyalty.values.tolist())
loyalty = [x for x in loyalty if str(x) != 'nan'] # remove 'nan'

gryffindor = [[],[],[],[],[]] # number of ['Female', 'Male'] in Gryffindor
hufflepuff = [[],[],[],[],[]] # number of ['Female', 'Male'] in Hufflepuff
ravenclaw = [[],[],[],[],[]]  # number of ['Female', 'Male'] in Ravenclaw
slytherin = [[],[],[],[],[]] # number of ['Female', 'Male'] in Slytherin

def func(df, num_row_df):
    num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df 

    templist_g = [] 
    templist_h = [] 
    templist_r = [] 
    templist_s = []

    if house == 'Gryffindor':
        templist_g.append(num_row_df) # e.g. num_row_df = number of i = 'Gryffindor, j = 'Female'
        gryffindor.append(templist_g)
    elif house == 'Hufflepuff':
        templist_h.append(num_row_df) # e.g. num_row_df = number of i = 'Gryffindor, j = 'Female'
        hufflepuff.append(templist_h)
    elif house == 'Ravenclaw':
        templist_r.append(num_row_df) # e.g. num_row_df = number of i = 'Gryffindor, j = 'Female'
        ravenclaw.append(templist_r)
    elif house == 'Slytherin':
        templist_s.append(num_row_df) # e.g. num_row_df = number of i = 'Gryffindor, j = 'Female'
        slytherin.append(templist_s)

for house in houselist:     
    for gen in gender:
    
        # reduce the dataframe from hp to df so that the column is house and row is gen
        df = hp.loc[(hp['House'] == house) & (hp['Gender'] == gen)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df 

        func(df, num_row_df)


for house in houselist: 
    for blood in bloodstatus:
        
        # reduce the dataframe from hp to df so that the column is house and row is blood
        df = hp.loc[(hp['House'] == house) & (hp['Blood_status'] == blood)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df
            
        func(house, num_row_df)

for house in houselist: 
    for hair in haircolour:
        
        # reduce the dataframe from hp to df so that the column is house and row is hair
        df = hp.loc[(hp['House'] == house) & (hp['Hair_colour'] == hair)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df
            
        func(house, num_row_df)

for house in houselist: 
    for eye in eyecolour:
        
        # reduce the dataframe from hp to df so that the column is house and row is eye
        df = hp.loc[(hp['House'] == house) & (hp['Eye_colour'] == eye)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df
            
        func(house, num_row_df)

for house in houselist: 
    for loyal in loyalty:
    
        # reduce the dataframe from hp to df so that the column is house and row is loyal
        df = hp.loc[(hp['House'] == house) & (hp['Loyalty'] == loyal)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df
            
        func(house, num_row_df)

def legend(fig, label):
    fig.legend(labels=label,   # the labels for each line
                    loc="center",            # position of legend
                    borderaxespad=0.1,       # small spacing around legend box
                    fontsize=12              # to make the legend fit the plot
                    )

def plot(n):
    '''plot is about gender, bloodstatus, haircolour, eyecolour, or loyalty depending on the house.
    the plot is about gender when n= 0, bloodstatus when n= 1, haircolour when n= 2, eyecolour when n= 3, loyalty when n = 4'''

    fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize=(10,10))
    try: 
        for row in [0,1]:
            for col in [0,1]:
                        if row == 0 and col == 0:   # upper left plot
                            x = gryffindor[n]       # e.g. if n = 0, it will be indicating to list of ['Female', 'Male'] in Gryffindor, 
                            title = 'Gryffindor'    # which is in index 0 in the list gryffindor
                        elif row == 0 and col == 1: # upper right plot
                            x = hufflepuff[n]
                            title = 'Hufflepuff'
                        elif row == 1 and col == 0: # botton left plot
                            x = ravenclaw[n]
                            title = 'Ravenclaw'
                        else:                       # bottom right plot
                            x = slytherin[n]
                            title = 'Slytherin'

                        axs[row, col].pie(x, shadow=True, startangle = 90) # create pie plots
                        axs[row, col].set_title(title) 

            if n == gender_index: 
                fig.suptitle("Gender distribution", fontsize=15)
                legend(fig, gender)
            elif n == bloodstatus_index:
                fig.suptitle("Blood status distribution", fontsize=15)
                legend(fig, bloodstatus)
            elif n == haircolour_index:
                fig.suptitle("Hair colour distribution", fontsize=15)
                legend(fig, haircolour)
            elif n == eyecolour_index:
                fig.suptitle("Eye colour distribution", fontsize=15)
                legend(fig, eyecolour)
            elif n == loyalty_index:
                fig.suptitle("Loyalty distribution", fontsize=15)
                legend(fig, loyalty)
    except IndexError:
        print("n should be in range from 0 to 4.") # in case n is out of range from 0 to 4
       

# use explode, explode = (0.05, 0.05, 0.05, 0.05, 0.05)
# donut plot 
    # draw circle
    # centre_circle = plt.Circle((0, 0), 0.70, fc='black') # readjust color depending on background
    # fig = plt.gcf()
    # # Adding Circle in Pie chart
    # fig.gca().add_artist(centre_circle)

plot(0)
# plot(1)
# plot(2)
# plot(3)
# plot(4)

plt.show()