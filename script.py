#%% Importing library and data

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud

data = pd.read_csv('data/US_Accidents_Dec19.csv')

#%% State Wise Count of Accidents (Bar Graph)

#Grouping values by State and counting cases in each severity 
count_bystates = data.groupby(['State','Severity']).size().unstack(fill_value=0)

#Plotting bar graph 
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)
count_bystates.plot.bar(ax=ax)

#Adding formatting elements to the graph
ax.set_xlabel('State',fontsize=15,color='red')
ax.set_ylabel('Counts',fontsize=15,color='red')
ax.set_title('State-Wise Counts for Accidents for Each Severity',fontdict={'fontsize': 25, 'fontweight' : 'bold', 'verticalalignment': 'center', 'horizontalalignment': 'center'})
ax.legend(['Small Incident (Caused Short Delay)','Severe','Very Severe','Most Severe (Caused Long Delay)'])
plt.show()

fig.savefig('graphs/State-WiseCounts.png')

#%% Processing text to remove spaces from weather conditions text seperated by spaces 

def processText(text):
    try:
        textlist = text.split('/')
        for i in range(len(textlist)):
            textlist[i]=textlist[i].split(' ')
            if '' in textlist[i]:
                textlist[i].remove('')
            textlist[i] = ''.join(textlist[i])
        text = '/'.join(textlist)
        return text
    except Exception as e:
        print(text)
        print(e)

#%% get weather data  and preprocess before constructing word Cloud
        
weatherdata = data[['Temperature(F)','Weather_Condition']].dropna()
weatherdata['Weather_Condition'] = weatherdata.Weather_Condition.apply(processText)

#%% Bar Graph
weather = weatherdata.groupby('Weather_Condition').size().reset_index(name='Count').set_index('Weather_Condition').sort_values(by='Count',ascending=False)
top_10_reasons = weather.head(n=10)

fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)
top_10_reasons.plot.bar(ax=ax)

ax.set_xlabel('Top Weather Conditions',fontsize=15,color='red')
ax.set_ylabel('Count of Accidents',fontsize=15,color='red')
ax.set_title('Top 10 Weather Conditions in which Most Accidents Occured',fontdict={'fontsize': 25, 'fontweight' : 'bold', 'verticalalignment': 'center', 'horizontalalignment': 'center'})
ax.legend().remove()
plt.tight_layout()
plt.show()

fig.savefig('graphs/Top10Reasons.png')

#%% Building word cloud with text from all weather conditions
text = ' '.join(weatherdata.Weather_Condition.values.tolist())
wordcloud = WordCloud(background_color="white").generate(text)

fig = plt.figure(figsize=(20,12))
ax = fig.add_subplot(111)
ax.set_title('Wordcloud using all Text Weather Conditions',fontdict={'fontsize': 25, 'fontweight' : 'bold', 'verticalalignment': 'center', 'horizontalalignment': 'center'})
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

fig.savefig('graphs/WordCloudAllText.png')
#%% wordcloud with word frequencies

text_with_frequencies = dict(zip(weather.index.values.tolist(),weather.Count.tolist()))
wordcloud = WordCloud().generate_from_frequencies(text_with_frequencies,max_font_size=68)

fig = plt.figure(figsize=(20,12))
ax = fig.add_subplot(111)
ax.set_title('Wordcloud using Weather Condition Frequencies',fontdict={'fontsize': 25, 'fontweight' : 'bold', 'verticalalignment': 'center', 'horizontalalignment': 'center'})
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

fig.savefig('graphs/WordClouTextFrequencies.png')