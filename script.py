#%% Importing library and data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

data = pd.read_csv('data/US_Accidents_Dec19.csv')

#%% State Wise Count of Accidents (Bar Graph)

#Grouping values by State and counting cases in each severity 
count_bystates = data.groupby(['State','Severity']).size().unstack(fill_value=0)

#Plotting bar graph 
fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(111)
count_bystates.plot.bar(ax=ax)
ax.set_xlabel('State')
ax.set_ylabel('Counts')
ax.set_title('State-Wise Counts for Accidents for Each Severity')
plt.show()

#%% Processing text to combine weather conditions seperated by spaces with underscore

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

#%%
weatherdata = data[['Temperature(F)','Weather_Condition']].dropna()
weatherdata['Weather_Condition'] = weatherdata.Weather_Condition.apply(processText)
weather = weatherdata.groupby('Weather_Condition').size().reset_index(name='Count').set_index('Weather_Condition').sort_values(by='Count',ascending=False)

#%% Bar Graph
top_10_reasons = weather.head(n=10)
top_10_reasons.plot.bar()

#%% wordcloud

#text = ' '.join(x for x in weatherdata.Weather_Condition)
text_with_frequencies = dict(zip(weather.index.values.tolist(),weather.Count.tolist()))
wordcloud = WordCloud().generate_from_frequencies(text_with_frequencies)

#%%
text = ' '.join(weatherdata.Weather_Condition.values.tolist())
wordcloud = WordCloud(background_color="white").generate(text)

#%%
fig = plt.figure(figsize=(20,12))
ax = fig.add_subplot(111)
ax.set_title('Wordcloud showing weather conditions that caused the accidents')
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

#%%

wordcloud = WordCloud(background_color="white").generate([x for x in weather.index.values])
plt.title("Wordcloud showing weather conditions that caused the accidents")
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()