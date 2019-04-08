# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 21:50:54 2018
@author: Anjukutty Joseph
"""
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

# main() - this function 1) read adult dataset. 2) Print menu and accept user input 
#          3) Call the function which does functionality of corresponding menu option.

def main():    
     
    # Read data.
    adultData = pd.read_csv("C:\\Anjukutty\\CIT\\Python\\Assignment\\adult.csv")    
    choice =0
    while(choice !=5):
        try:
            menu = "Please select one of the following options: \n\n\
 1. Most educated countries \n 2. Marital status\n 3. Class analysis \n 4. Income prediction \n 5. Exit \n "
            choice = int(input(menu))
            if choice==1:
                educatedCountries(adultData)
            elif choice ==2:
                maritalStatus(adultData)
            elif choice ==3:
                workClassAnalysis(adultData)
            elif choice ==4:
                incomeAnalysis(adultData)
            elif choice <1:
                print("Inavlid input!. Please enter a valid choice between 1 to 5")
            elif choice >5:
                print("Inavlid input!. Please enter a valid choice between 1 to 5")
        except:
            print("Please enter a valid choice between 1 to 5")
           

# This function implement menu option1. 
def educatedCountries(data):       
    try:
         dataGrpByCountry = data[['native-country','education-num']].groupby('native-country')         
         print("Total countries represented are:", dataGrpByCountry.size().count())
         print("Least respondents when grouped by country:",dataGrpByCountry.size().min())
         print("Maximum respondents when grouped by country:",dataGrpByCountry.size().max())                 
         meanEduPerCountry = dataGrpByCountry['education-num'].mean().sort_values(ascending=False) 
         noRankCountries = int(input("How many ranked countries you want to return?"))   
         print(meanEduPerCountry[0:noRankCountries])        
         ax = meanEduPerCountry[0:noRankCountries].plot.barh()
         ax.set_xlabel("Average Education level") 
         plt.show()
    except:
         print("Please enter a valid choice")   
    
# This function implement menu option2.            
def maritalStatus(data):
    
    dataGrpByMrtStatus = data[['marital-status','education-num']].groupby('marital-status')
    details= dataGrpByMrtStatus.describe() # details is a dataframe     
    
    plt.plot(details['education-num','25%'])
    plt.plot(details['education-num','50%'])
    # plt.plot(details.sort_values([('education-num','75%')]))
    plt.plot(details['education-num','75%'])
    
    plt.xlabel("Marital Status")
    plt.ylabel("Education")
    plt.title("Relationship between Education and Marital Status")
    plt.legend(["1st quartile","2nd quartile","3rd quartile"])
    plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.savefig("maritalStatusEdu.png")  
    plt.show()
    
# This function implement menu option3. 
def workClassAnalysis(data):
    # Group adult data by workclass
    dataGrpWorkClass = data[['education-num','Income','workclass']].groupby(["workclass"])
    # Create a list of workClass
    workClassList = ["Federal-gov","Local-gov","State-gov","Private","Self-emp-inc","Never-worked","Self-emp-not-inc","Without-pay"]
    # Take two workclass which user want to compare
    try:
        # Take two workclass from user
        workclass1,workclass2 = input("""Select any two numbers corresponding to workclass you wish to analyse from below list. Please seperate your choice with a space and hit enter. For example, if your choice is Private and Without-pay enter "4 8" \n\n1.Federal-gov\n2.Local-gov\n3.State-gov\n4.Private\n5.Self-emp-inc\n6.Never-worked\n7.Self-emp-not-inc\n8.Without-pay\n""").split()
        workclass1 = int(workclass1)
        workclass2 = int(workclass2)        
        menu = "Please select number for criteria of analysis\n1. Education Level \n2. Income\n"
        userSelection = int(input(menu))    
        
        # save meanincome and mean education in adultdata by workclass in dictionary.         
        for wclass in workClassList:        
            if  workClassList[workclass1-1] == wclass:
                federalClass = dataGrpWorkClass.get_group(wclass)
                dict1= {"WorkClass": wclass,
                        "MeanEducation":federalClass['education-num'].mean(),
                        "MeanIncome": federalClass['Income'].mean()
                       }
            if  workClassList[workclass2-1] == wclass:          
                privateClass = dataGrpWorkClass.get_group(wclass)
                dict2 = {"WorkClass": wclass,
                        "MeanEducation":privateClass['education-num'].mean(),
                        "MeanIncome": privateClass['Income'].mean()
                       }
        # plot graph for Education#
        if userSelection ==1:
          plt.bar([dict1['WorkClass'], dict2['WorkClass']], [dict1["MeanEducation"],dict2["MeanEducation"]])
          plt.ylabel("Mean Education")  
       # Plot graph for Income
        elif userSelection ==2:
          plt.bar([dict1['WorkClass'], dict2['WorkClass']], [dict1["MeanIncome"],dict2["MeanIncome"]])
          plt.ylabel("Mean Income")
        plt.xlabel("WorkClass")
        plt.title("WorkClass Analysis")
        plt.show()
    except ValueError:
        print("Input error - please check your input and try again")
    except Exception as e: 
        print(e)
        
# This function implement menu option4.
def incomeAnalysis(adultData):    
    try:
        # plot Income aganist workclass
        workClassGroup = adultData.groupby(["workclass"])['Income'].mean().sort_values()
        ax = workClassGroup.plot(kind = "bar")
        ax.set_ylabel("Average Income level") 
        plt.show()
        
        # plot Income aganist education   
        adultData=adultData.sort_values("education-num")
        workClassGroup = adultData.groupby(["education"], sort = False)['Income'].mean()         
        ax= workClassGroup.plot(kind = "bar")
        ax.set_ylabel("Average Income level") 
        plt.show()
        
        
        # Plot Income aganist occupation     
        workClassGroup = adultData.groupby(["occupation"])['Income'].mean()
        ax=workClassGroup.plot(kind = "bar")
        ax.set_ylabel("Average Income level") 
        plt.show()
        
        #  Income Vs Age
        workClassGroup = adultData.groupby(["age"])['Income'].mean()
        ax=workClassGroup.plot()
        ax.set_ylabel("Average Income level") 
        plt.show()
        
        # Expected a direct relationship between hours and income.
        # But there is no significant pattern. 
        workClassGroup= adultData.groupby(["hours-per-week"])["Income"].mean()        
        ax=workClassGroup.plot()
        ax.set_ylabel("Average Income level") 
        plt.show()      
       
        # marital status and income
        workClassGroup = adultData.groupby(['marital-status'])['Income'].mean().sort_values()
        workClassGroup.plot(kind = "bar")
        plt.ylabel("Average Income level")
        plt.show()
        
        # income and gender
        workClassGroup = adultData.groupby(["sex"])['Income'].mean()
        workClassGroup.plot(kind = "bar")
        plt.show()      
       
        #income Vs edication & sex& race
        fig = sns.lmplot(x = 'education-num', y= 'Income', hue = 'sex', col= 'race',
                          col_wrap =3, sharex = False, line_kws = {'linewidth':5},
                          data = adultData)
        fig.savefig("C:\Anjukutty\CIT\Python\Assignment\p.png")
        plt.show()
        
    except Exception as e: 
        print(e)
        
# call man function 
main()