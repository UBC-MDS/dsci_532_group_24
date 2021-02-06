##Reflection

On our latest version, there are three tabs in total. The very first one shown in the app is ‘Sanpshot’. Based on the function we built on milestone 2. We change the color scheme of the country bar char to coordinate with our heating map. We also add a new statistic type, death per thousand 0-4 years-old, to give users more information about the African kids’ health, since sometimes the total number of deaths is misleading, given the fact that the country with higher population always has higher mortality. Then we add ‘Trend’ tab on our app to show the overall tendency of mortality of different countries and caused by different diseases over the years. Users could select the range of years, countries, and diseases easily they are interested in. 

During this project, we received many valuable feedbacks from Joel, Analise and group 23. Among these feedbacks, one feedback from Analise is particularly valuable. Based on our original layout, there is a symmetric design, where map is in the middle, two bar charts are located each side of the map respectively and the three controllers are on each top of the chart. It is misleading which could give a sense to users that each controller can control one char only. However, we three charts can change at the same time based on every control. We then changed our layout, and now we believe that the function of the controllers is more intuitive. 

The one chart we plant in milestone 2 stacked bar chart is not added in our final app. We found if we add the proportion of the countries in each single disease bar, the bar would be very crowded, since we have so many countries. If users are interested in comparing many countries at the same time, staked bar char is not an ideal choice.

Overall, we made a dashboard which is the same with our original plan and it is easy to use. There are 4 reason we choose to use Python to finalize our dashboard instead of R,
1. All three of us prefer Python language.
2. Heroku deployment in R is painful.
3. We hate the ‘list’ in R.
4. We prefer the color scheme of Plotly maps in Python version.
