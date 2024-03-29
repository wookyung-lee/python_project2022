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
for out1 in outlier1:
    hp = hp.loc[hp['Blood_status'] != out1]

# unit ambiguous labels to one label
hp["Hair_colour"] = hp["Hair_colour"].replace(["Blond", "White-blond", "Silvery-blonde", "White blond", "Straw blond", "Reddish-blonde", "Dirty-blonde", "Sandy", "Straw-coloured"], "Blonde")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Grey", "Silver", "Silver| formerly auburn", "Silver| formerly black", "White (balding)", "Iron grey", "White"], "Silver / White / Grey")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Red ", "Ginger", "Red brown", "Brown/greying", "Auburn"], "Red")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Bald", "Colourless and balding"], "Bald")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Black", "Jet-black", "Colourless and balding"], "Dark")
hp["Hair_colour"] = hp["Hair_colour"].replace(["Mousy brown", "Reddish-brown", "Tawny", "Mousy", "Light brown flecked with grey"], "Brown")

# remove rows with certain labels, which in this case are outliers
outlier2 = ["Variable", "Green"]
for out2 in outlier2:
    hp = hp.loc[hp['Hair_colour'] != out2]

# unit ambiguous labels to one label
hp["Eye_colour"] = hp["Eye_colour"].replace(["Bright green", "Gooseberry"], "Green")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Bright brown", "Scarlet ", "Ruddy", "Hazel"], "Brown")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Black"], "Dark")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Bright Blue", "Grey/Blue[", "Astonishingly blue"], "Blue")
hp["Eye_colour"] = hp["Eye_colour"].replace(["Pale silvery", "Silvery", "Dark Grey"], "Grey")

# remove rows with certain labels, which in this case are outliers
outlier3 = ["One dark, one electric blue", "Pale, freckled", "Yellowish", "Yellow"]
for out3 in outlier3:
    hp = hp.loc[hp['Eye_colour'] != out3]

# unit ambiguous labels to one label
hp.Loyalty = hp.Loyalty.apply(lambda x: "Dumbledore's Army" if not pd.isnull(x) and ("Dumbledore" in x) else x) 
hp.Loyalty = hp.Loyalty.apply(lambda x: "Dumbledore's Army" if not pd.isnull(x) and ("Phoenix" in x) else x) 
hp.Loyalty = hp.Loyalty.apply(lambda x: "Lord Voldemort" if not pd.isnull(x) and ("Voldemort" in x) else x)
hp["Loyalty"] = hp["Loyalty"].replace(["Minister of Magic"], "Ministry of Magic")
hp["Loyalty"] = hp["Loyalty"].replace(["Hogwarts School of Witchcraft and Wizardry"], "Hogwarts School")

# remove rows with certain labels, which in this case are outliers
outlier4 = ["Gellert Grindelwald's Acolytes"]
for out4 in outlier4:
    hp = hp.loc[hp['Loyalty'] != out4]

# preparing lists to insert the data in order of 'Gender', 'Blood status', 'Hair colour', 'Eye colour', 'Loyalty' 
# create 2D house lists of traits in each hous [['Gender'], ['Blood status'], ['Hair colour'], ['Eye colour'], ['Loyalty']]
gryffindor = [] 
hufflepuff = [] 
ravenclaw = [] 
slytherin = []

# get the list of houses in order to sort them according to the gender, blood status, hair colour, eye colour, and loyalty
houselist = np.unique(hp.House.values.tolist())
houselist = houselist[1:5] # remove 'Durmstrang Institute' and 'nan'

# get the unique gender values
gender_index = 0 # for future indexing of each house list
gender = np.unique(hp.Gender.values.tolist())
gender = [x for x in gender if str(x) != 'nan'] # remove 'nan'

# get the unique blood status values
bloodstatus_index = 1 # for future indexing of each house list
bloodstatus = np.unique(hp.Blood_status.values.tolist())
bloodstatus = [x for x in bloodstatus if not ' or ' in str(x)] # remove strings with ' or '
bloodstatus = [x for x in bloodstatus if not ' or ' in str(x)] # remove strings with ' or '
bloodstatus = [x for x in bloodstatus if str(x) != 'nan'] # remove 'nan'

# get the unique hair colour values
haircolour_index = 2 # for future indexing of each house list
haircolour = np.unique(hp.Hair_colour.values.tolist())
haircolour = [x for x in haircolour if str(x) != 'nan'] # remove 'nan'

# get the unique eye colour values
eyecolour_index = 3 # for future indexing of each house list
eyecolour = np.unique(hp.Eye_colour.values.tolist())
eyecolour = [x for x in eyecolour if str(x) != 'nan'] # remove 'nan'

# get the unique loyalty values
loyalty_index = 4 # for future indexing of each house list
loyalty = np.unique(hp.Loyalty.values.tolist())
loyalty = [x for x in loyalty if str(x) != 'nan'] # remove 'nan'

def appendfunc(list_g,  list_h, list_r, list_s, row):
    '''append the number of people that share the same trait (e.g., gender, hair colour) & house to respective lists
    Args: list_g(list) - list for gryffindor to which row gets appended
          list_h(list) - list for hufflepuff to which row gets appended
          list_r(list) - list for ravenclaw to which row gets appended
          list_s(list) - list for slytherin to which row gets appended
          row(int) - number of people with the same trait & house '''
    
    if house == 'Gryffindor':
        list_g.append(row) 
    elif house == 'Hufflepuff':
        list_h.append(row)
    elif house == 'Ravenclaw':
        list_r.append(row)
    elif house == 'Slytherin':
        list_s.append(row)

def appendfunc2(list_g,  list_h, list_r, list_s):
    '''append the lists containing the number of people with the same trait (e.g., gender, hair colour) & house to respective house list ("gryffindor", "hufflepuff", "ravenclaw", "slytherin"). The house lists are then 2D lists. 
    Args: list_g(list) - list for gryffindor, containing amount of people with same trait, which gets appended to gryffindor
          list_h(list) - list for hufflepuff, containing amount of people with same trait, which gets appended to hufflepuff
          list_r(list) - list for ravenclaw, containing amount of people with same trait, which gets appended to ravenclaw
          list_s(list) - list for slytherin, containing amount of people with same trait, which gets appended to slytherin '''
    
    gryffindor.append(list_g)
    hufflepuff.append(list_h)
    ravenclaw.append(list_r)
    slytherin.append(list_s)

# inserting data into 2D list for gender with index 0
gryffindor_gender = [] # number of ['Female', 'Male'] in Gryffindor
hufflepuff_gender = [] # number of ['Female', 'Male'] in Hufflepuff
ravenclaw_gender = []  # number of ['Female', 'Male'] in Ravenclaw
slytherin_gender = []  # number of ['Female', 'Male'] in Slytherin

for house in houselist: 
    for gen in gender:
    
        # reduce the dataframe from hp to df so that the column is house and row is gen
        df = hp.loc[(hp['House'] == house) & (hp['Gender'] == gen)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df
        # save amount of different genders for the respective houses
        appendfunc(gryffindor_gender, hufflepuff_gender, ravenclaw_gender, slytherin_gender, num_row_df)

# add list containing the information of the gender to the respective house list
appendfunc2(gryffindor_gender, hufflepuff_gender, ravenclaw_gender, slytherin_gender)

# inserting data into 2D list for bloodstatus with index 1
gryffindor_bloodstatus = [] # number of people with ['Half-blood', 'Muggle-born', 'Pure-blood'] in Gryffindor
hufflepuff_bloodstatus = [] # number of people with ['Half-blood', 'Muggle-born', 'Pure-blood'] in Hufflepuff
ravenclaw_bloodstatus = []  # number of people with ['Half-blood', 'Muggle-born', 'Pure-blood'] in Ravenclaw
slytherin_bloodstatus = []  # number of people with ['Half-blood', 'Muggle-born', 'Pure-blood'] in Slytherin

for house in houselist: 
    for blood in bloodstatus:
        
        # reduce the dataframe from hp to df so that the column is house and row is blood
        df = hp.loc[(hp['House'] == house) & (hp['Blood_status'] == blood)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df
        # save amount of different blood status for the respective house
        appendfunc(gryffindor_bloodstatus, hufflepuff_bloodstatus, ravenclaw_bloodstatus, slytherin_bloodstatus, num_row_df)

# add lists containing the information of the blood status to the respective house list
appendfunc2(gryffindor_bloodstatus, hufflepuff_bloodstatus, ravenclaw_bloodstatus, slytherin_bloodstatus)

# inserting data into 2D list for haircolour with index 2
gryffindor_haircolour = [] # number of people with the hair colour of ['Bald', 'Blonde', 'Brown', 'Dark', 'Red', 'Silver / White / Grey'] in Gryffindor
hufflepuff_haircolour = [] # number of people with the hair colour of ['Bald', 'Blonde', 'Brown', 'Dark', 'Red', 'Silver / White / Grey'] in Hufflepuff
ravenclaw_haircolour = []  # number of people with the hair colour of ['Bald', 'Blonde', 'Brown', 'Dark', 'Red', 'Silver / White / Grey'] in Ravenclaw
slytherin_haircolour = []  # number of people with the hair colour of ['Bald', 'Blonde', 'Brown', 'Dark', 'Red', 'Silver / White / Grey'] in Slytherin

for house in houselist: 
    for hair in haircolour:
        
        # reduce the dataframe from hp to df so that the column is house and row is hair
        df = hp.loc[(hp['House'] == house) & (hp['Hair_colour'] == hair)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df    
        # save amount of different hair colours for the respective house
        appendfunc(gryffindor_haircolour, hufflepuff_haircolour, ravenclaw_haircolour, slytherin_haircolour, num_row_df)

# add list containing the information of the hair colour to the respective house list
appendfunc2(gryffindor_haircolour, hufflepuff_haircolour, ravenclaw_haircolour, slytherin_haircolour)

# inserting data into 2D list for haircolour with index 3
gryffindor_eyecolour = [] # number of people with the eye colour of  ['Blue', 'Brown', 'Dark', 'Green', 'Grey', 'Hazel'] in Gryffindor
hufflepuff_eyecolour = [] # number of people with the eye colour of ['Blue', 'Brown', 'Dark', 'Green', 'Grey', 'Hazel'] in Hufflepuff
ravenclaw_eyecolour = []  # number of people with the eye colour of ['Blue', 'Brown', 'Dark', 'Green', 'Grey', 'Hazel'] in Ravenclaw
slytherin_eyecolour = []  # number of people with the eye colour of ['Blue', 'Brown', 'Dark', 'Green', 'Grey', 'Hazel'] in Slytherin

for house in houselist: 
    for eye in eyecolour:
        
        # reduce the dataframe from hp to df so that the column is house and row is eye
        df = hp.loc[(hp['House'] == house) & (hp['Eye_colour'] == eye)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df 
        # save amount of different eye colours for the respective house
        appendfunc(gryffindor_eyecolour, hufflepuff_eyecolour, ravenclaw_eyecolour, slytherin_eyecolour, num_row_df)

# add list containing the information of the eye colour to the respective house list
appendfunc2(gryffindor_eyecolour, hufflepuff_eyecolour, ravenclaw_eyecolour, slytherin_eyecolour)

# inserting data into 2D list for haircolour with index 4
gryffindor_loyalty = [] # number of supporter of ["Dumbledore's Army", 'Hogwarts School', 'Lord Voldemort', 'Ministry of Magic'] in Gryffindor
hufflepuff_loyalty = [] # number of supporter of ["Dumbledore's Army", 'Hogwarts School', 'Lord Voldemort', 'Ministry of Magic'] in Hufflepuff
ravenclaw_loyalty = []  # number of supporter of ["Dumbledore's Army", 'Hogwarts School', 'Lord Voldemort', 'Ministry of Magic'] in Ravenclaw
slytherin_loyalty = []  # number of supporter of ["Dumbledore's Army", 'Hogwarts School', 'Lord Voldemort', 'Ministry of Magic'] in Slytherin

for house in houselist: 
    for loyal in loyalty:
    
        # reduce the dataframe from hp to df so that the column is house and row is loyal
        df = hp.loc[(hp['House'] == house) & (hp['Loyalty'] == loyal)]
        num_row_df = df.shape[0] # gives number of the row of the reduced dataframe df   
        # save amount of different loyalty for the respective house
        appendfunc(gryffindor_loyalty, hufflepuff_loyalty, ravenclaw_loyalty, slytherin_loyalty, num_row_df)
        
# add list containing the information of the loyalty to the respective house list
appendfunc2(gryffindor_loyalty, hufflepuff_loyalty, ravenclaw_loyalty, slytherin_loyalty)

def legend(fig, label):
    '''define legend as a function to reduce the line number
    Arg: fig(figure): frame of the plot 
         label(list): label for the legend '''
    fig.legend(labels=label,   # the labels for each line
                    loc="center",            # position of legend
                    borderaxespad=0.1,       # small spacing around legend box
                    fontsize=12              # to make the legend fit the plot
                    )

def plot(n):
    '''The plot is about gender when n=0, bloodstatus when n=1, haircolour when n=2, eyecolour when n=3, loyalty when n=4
    Arg: n(int): number, which indicates which plot is chosen to be shown'''

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
    
    plt.show()