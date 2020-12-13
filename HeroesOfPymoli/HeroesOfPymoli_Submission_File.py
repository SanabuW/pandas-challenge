#!/usr/bin/env python
# coding: utf-8

# In[80]:


#import dependencies
import pandas as pd
import os


# In[81]:


#import csv into a df for use with Pandas
filepath = os.path.join("Resources","purchase_data.csv")
sourcedf = pd.read_csv(filepath, encoding = "UTF-8")


# In[82]:


#review dataset
#see overview
sourcedf


# In[83]:


#list all columns
columnsdf = pd.DataFrame(sourcedf.columns)
columnsdf


# In[84]:


#list data types per column
sourcedf.dtypes


# In[85]:


#Check for null values
sourcedf.count()


# In[86]:


#Look to see if consolidation is necessary in "Gender" values
genderList = sourcedf["Gender"].unique()
genderList
#Confirmed that all values are exclusive of each other


# In[87]:


#Data review: 
    #780 rows × 7 columns
    #Source data is a register of transactions. Each row is a uniqe transaction 
    #Unique player IDs are in col "SN"
    #Purchase ID column matches index no.
    #No null values present
    #All data types OK
    #No extraneous label values in "Gender"
#OK to proceed to calculations


# In[88]:


#Player count
#get count of all unique players. First store single value into variable
playerCount = sourcedf["SN"].nunique()
#non-string reference version using .iloc: playerCount = sourcedf.iloc[:,1].nunique()

#place variable into dataframe for display
playerCountdf = pd.DataFrame({"Total Players":[playerCount]})
playerCountdf


# In[89]:


#Purchasing Analysis (Total)
#Get all values first and assign to variables, then assign variables into dataframe
#Get count of all unique items
itemCount = sourcedf["Item ID"].nunique()
#Get average of Price column
averagePurchPrice = sourcedf["Price"].mean()
#Get Total Number of Purchases as a row count of Purchase ID
numberOfPurchases = sourcedf["Purchase ID"].count()
#Get Total Revenue as a sum of all values in Price
totalRev = sourcedf["Price"].sum()

#place variables into dataframe
purchSummary = pd.DataFrame({"No. of Unique Items":[itemCount], 
                             "Avg. Purchase Price":[averagePurchPrice],
                             "Total Number of Purchases":[numberOfPurchases],
                             "Total Revenue":[totalRev]
                            })

#Format as necessary with .map()
purchSummary["Avg. Purchase Price"]=purchSummary["Avg. Purchase Price"].map("${:,.2f}".format)
purchSummary["Total Revenue"]=purchSummary["Total Revenue"].map("${:,.2f}".format)
#display summary dataframe
purchSummary


# In[49]:


#Gender Demographics
#use playerCount for total player count

#Percentage and Count of Male Players
#find male players. Filter out male players players by gender
malePlayers = sourcedf.loc[sourcedf["Gender"] == "Male","SN"]
#Get unique count name of players
malePlayersCount = malePlayers.nunique()
#Get percentage of male players
malePercentage = malePlayersCount/playerCount

#Percentage and Count of Female Players
#find female players. Filter out female players players by gender
femalePlayers = sourcedf.loc[sourcedf["Gender"] == "Female","SN"]
#Get unique count name of players
femalePlayersCount = femalePlayers.nunique()
#Get percentage of male players
femalePercentage = femalePlayersCount/playerCount


#Percentage and Count of Other / Non-Disclosed
#find male players. Filter out male players players by gender
otherPlayers = sourcedf.loc[sourcedf["Gender"] == "Other / Non-Disclosed","SN"]
#Get unique count name of players
otherPlayersCount = otherPlayers.nunique()
#Get percentage of male players
otherPercentage = otherPlayersCount/playerCount


#Assemble summary table
genderDemoSummary = pd.DataFrame({"Total Count":[malePlayersCount, femalePlayersCount, otherPlayersCount], 
                             "Percentage of Players":[malePercentage, femalePercentage, otherPercentage]
                            })

#Set index labels using list
genderDemoSummary.index = ["Male","Female","Other / Non-Disclosed"]


#format percentages
#multiply by 100 to compensate for finding percentages from arithmetic
genderDemoSummary["Percentage of Players"] = genderDemoSummary["Percentage of Players"] * 100
#format
genderDemoSummary["Percentage of Players"] = genderDemoSummary["Percentage of Players"].map("{:,.2f}%".format)
genderDemoSummary


# In[32]:


#Purchasing Analysis (Gender)
genderGroupdf= sourcedf.groupby(["Gender"])

#Find Purchase Count with .count() on any col
genderGroupCountdf = genderGroupdf["Purchase ID"].count()

#Average Purchase Price with .mean on "Price"
genderGroupAvgdf = genderGroupdf["Price"].mean()

#Total Purchase Value with .sum on "Price"
genderGroupSumdf = genderGroupdf["Price"].sum()

#Average Purchase Total per Person by Gender by dividing genderGroupSumdf series by unique player--
#counts by gender
genderAvgPerPersonByGenderdf = genderGroupSumdf/[femalePlayersCount, malePlayersCount, otherPlayersCount]

#Create summary table
purchAnalysisSummary = pd.DataFrame({"Purchase Count":genderGroupCountdf,
                                     "Avg Purchase Price":genderGroupAvgdf,
                                     "Total Purchase Value":genderGroupSumdf,
                                     "Avg Total Purchase per Person":genderAvgPerPersonByGenderdf
                            })
#Format summary table
purchAnalysisSummary["Avg Purchase Price"] = purchAnalysisSummary["Avg Purchase Price"].map("${:,.2f}".format)
purchAnalysisSummary["Total Purchase Value"] = purchAnalysisSummary["Total Purchase Value"].map("${:,.2f}".format)
purchAnalysisSummary["Avg Total Purchase per Person"] = purchAnalysisSummary["Avg Total Purchase per Person"].map("${:,.2f}".format)

#Display summary table
purchAnalysisSummary


# In[33]:


#Age Demographics
#The below each broken into bins of 4 years (i.e. <10, 10-14, 15-19, etc.) 	
    #find max age
sourcedf["Age"].max()



# In[34]:


#set up bins
binVals = [0, 9.999, 14, 19, 24, 29, 34, 39, 49]
binLabels = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

#use .cut to break up into bins
sourcedf["Age Ranges"] = pd.cut(sourcedf["Age"], binVals, labels = binLabels)

#move Age Ranges to be the index
sourcedfAgeIndex = sourcedf.set_index("Age Ranges")

#group by age
sourcedfAgeIndexGroup = sourcedfAgeIndex.groupby(["Age Ranges"])

#Find player count of each age group
#Find unique players of each age group
sourcedfAgeUniquePlayers = sourcedfAgeIndexGroup["SN"].nunique()

#Find percentages
agePercentages = sourcedfAgeUniquePlayers/playerCount * 100

#Create age demo summary table
ageDemoSummary = pd.DataFrame({"Total Count":sourcedfAgeUniquePlayers,
                              "Percentage of Players":agePercentages})

#Format age demo summary table
ageDemoSummary["Percentage of Players"] = ageDemoSummary["Percentage of Players"].map("{:,.2f}%".format)
ageDemoSummary


# In[36]:


#Purchasing Analysis (Age)

#group by age
sourcedfAgeIndexGroup= sourcedfAgeIndex.groupby(["Age Ranges"])

#Find Purchase Count with .count() on Purchase ID
sourcedfAgeIndexCount = sourcedfAgeIndexGroup["Purchase ID"].count()

#Find Average Purchase Price with .mean() on Price
sourcedfAgeAvg = sourcedfAgeIndexGroup["Price"].mean()    

#Find Total Purchase Value with .sum() on Price
sourcedfAgeSum = sourcedfAgeIndexGroup["Price"].sum()

#Average Purchase Total per Person by Age Group by dividing genderGroupSumdf series by number of unique--
#buyers per age group
#Find unique SN's per age group
sourcedfAgeUniques = sourcedfAgeIndexGroup["SN"].nunique()
avgPurchaseTotalAge = sourcedfAgeSum/sourcedfAgeUniques

#Create summary table
ageSummary = pd.DataFrame({"Purchase Count":sourcedfAgeIndexCount,
                                     "Avg Purchase Price":sourcedfAgeAvg,
                                     "Total Purchase Value":sourcedfAgeSum,
                                     "Avg Total Purchase per Person":avgPurchaseTotalAge
                            })
#Format summary table
ageSummary["Avg Purchase Price"] = ageSummary["Avg Purchase Price"].map("${:,.2f}".format)
ageSummary["Total Purchase Value"] = ageSummary["Total Purchase Value"].map("${:,.2f}".format)
ageSummary["Avg Total Purchase per Person"] = ageSummary["Avg Total Purchase per Person"].map("${:,.2f}".format)

#Display summary table
ageSummary



# In[40]:


#Top Spenders

#Group transactions by purchaser
playerGroup = sourcedf.groupby(["SN"])

#Find Purchase Count with .count
playerGroupCount = playerGroup["Purchase ID"].count()

#Find Average purchase price with .mean "Price"
playerGroupAvg = playerGroup["Price"].mean()

#Find Total Purchased for each player with .sum on "Price"
playerGroupSum = playerGroup["Price"].sum()



#build Summary table
#Create summary table
playerSummary = pd.DataFrame({"Purchase Count":playerGroupCount,
                                     "Avg Purchase Price":playerGroupAvg,
                                     "Total Purchase Value":playerGroupSum
                            })

#Sort by decreasing by "Total Purchase Value" with .sort_values
sortPlayerSummary = playerSummary.sort_values("Total Purchase Value", ascending=False)

#Format summary table
sortPlayerSummary.index = sortPlayerSummary.index.map("{:<}".format)
sortPlayerSummary["Avg Purchase Price"] = sortPlayerSummary["Avg Purchase Price"].map("${:.2f}".format)
sortPlayerSummary["Total Purchase Value"] = sortPlayerSummary["Total Purchase Value"].map("${:.2f}".format)

#Get the top 5 spenders
#pull first 5 with .iloc
sortPlayerSummaryTop = sortPlayerSummary.iloc[0:5,]
sortPlayerSummaryTop


# In[91]:


#Most Popular Items
#retrieve Dataframe
itemsOnlydf = pd.DataFrame({"Item ID":sourcedf["Item ID"],
                                     "Item Name":sourcedf["Item Name"],
                                     "Price":sourcedf["Price"]
                            })

#Group transactions by purchaser
itemGroup = sourcedf.groupby(["Item ID","Item Name"])


#Find Purchase Count with .count
itemGroupCount = itemGroup["Purchase ID"].count()

#Get Item Prices
itemGroupPrices = itemGroup["Price"].mean()

#Find Total Purchased for each player with .sum on "Price"
itemGroupSum = itemGroup["Price"].sum()


#build Summary table
#Create summary table
itemSummary = pd.DataFrame({"Purchase Count":itemGroupCount,
                                     "Item Price":itemGroupPrices,
                                     "Total Purchase Value":itemGroupSum
                            })


#Sort by decreasing by "Purchase Count" with .sort_values
sortItemSummary = itemSummary.sort_values("Purchase Count", ascending=False)
#Format summary table
sortItemSummary["Item Price"] = sortItemSummary["Item Price"].map("${:.2f}".format)
sortItemSummary["Total Purchase Value"] = sortItemSummary["Total Purchase Value"].map("${:.2f}".format)
#Get the top 5 items
#pull first 5 items with .iloc
sortItemSummaryTop = sortItemSummary.iloc[0:5,]
sortItemSummaryTop



# In[93]:


#Most Profitable Items
#use itemSummary and reorder by "Total Purchase Value"
sortProfitableItemSummary = itemSummary.sort_values("Total Purchase Value", ascending=False)
#Format summary table
sortProfitableItemSummary["Item Price"] = sortProfitableItemSummary["Item Price"].map("${:.2f}".format)
sortProfitableItemSummary["Total Purchase Value"] = sortProfitableItemSummary["Total Purchase Value"].map("${:.2f}".format)
#pull first 5 profitable items with .iloc
sortProfitItemSummaryTop = sortProfitableItemSummary.iloc[0:5,]
sortProfitItemSummaryTop


# In[ ]:




