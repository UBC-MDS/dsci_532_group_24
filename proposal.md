# Project proposal

## Section 1: Motivation and Purpose

The ongoing COVID-19 crisis has highlighted some of the drastic consequences arising from inequalities in access to healthcare among nations, ethnicities, and social classes. Although this global crisis has exposed many of the shortcomings of the healthcare systems that exist even in wealthy countries, there are well-documented reports of the need to address preventable child deaths in Africa. 

According to the 2007 UNICEF report publicly accessible through [UN website](https://www.un.org/en/chronicle/article/reducing-child-mortality-challenges-africa), sub-Saharan Africa alone accounted for almost 50 per cent of child mortality, although it constituted only 11 per cent of the world population. Although there has been significant progress in reducing preventable child deaths between 1999 and 2019, [2020 WHO fact sheet on improving children survival and well-being](https://www.who.int/en/news-room/fact-sheets/detail/children-reducing-mortality) discusses the prevalence of child mortality that persists in Sub-Saharan Africa, which accounts for the highest child mortality rate in the world. For example, in 2019, 86 out of 1000 newborns in The Democratic Republic of the Congo, a nation with 86.79 million people, do not make it to their fifth birthday. In Chad, the number is as high as 117. By contrast, about 99.6% (996 in 1000) of Canadian newborns are still alive when they are five years old. As internal data analysts for an international non-governmental organization (INGO), we are dedicated to using data to understand infant and child mortality across the African continent. 

We will explore, analyze and present the diseases responsible for infant and child deaths in Africa, and produce a data dashboard for both internal and external use. We believe that our work will inform our organization's leadership about where in Africa we should focus our resources, and what disease-specific measures, e.g. medications and vaccines, we should focus on in different countries. Specifically, we aim to understand the following questions: 

 - Which countries in Africa have the most severe infant and child mortality problem? How has each country's situation changed over time?
 - Among major diseases, what are the main causes of infant and child mortality? How has the severity of each cause changed over time?

Furthermore, we also expect the dashboard to be published for a larger audience of donors, government partners and receiver countries. Users of our data dashboard will be able to select the country, year or disease type that they are interested in. This will help them make more informed and targeted decisions. 


## Section 2: Description of the data

We will visualize the annual estimates of child mortality (reported as number of deaths of children aged 0 - 5 years) for African countries, as well as a closer look into some preventable and treatable causes of child mortality. Dataset for total number of child deaths, as well as individual datasets for specific causes of child deaths (e.g. HIV deaths, malaria deaths, measles deaths, and meningitis deaths) are available separately through [Gapminder website](https://www.gapminder.org/data).

Dataset for total number of child deaths (`number_of_child_deaths.csv`) contains observations from 194 countries (arranged into rows in alphabetical order) over 216-year period from 1800 – 2015, inclusive (arranged into columns in chronological order). 

Dataset for each cause of child mortality (`hiv_deaths_in_children_1_59_months_total_deaths.csv`, `malaria_deaths_in_children_1_59_months_total_deaths.csv`, `measles_deaths_in_children_1_59_months_total_deaths.csv`, `meningitis_deaths_in_children_1_59_months_total_deaths.csv`) contains observations from 188 countries over 27-year period from 1990 – 2016, inclusive.  

Of these datasets, we will focus on observations from countries in the African continent over the years 1990 – 2015, inclusive. It may help to note that even though the observations are child mortality reported in total number of cases for the given year, many observations are not whole numbers, as they are estimated figures.

Information on how the Gapminder child mortality datasets are collected and compiled is available on [Gapminder summary documentation](https://www.gapminder.org/data/documentation/gd005/).

The method of approximation used for estimating annual child mortality is described in [a 2013 report by WHO](https://www.who.int/gho/child_health/mortality/ChildCME_method.pdf).



## Section 3: Research questions and usage scenarios

Aiden is a volunteer of an international charity focusing on helping children across the African continent. Recently he has been assigned to a new project to distribute life-saving medication to children in Africa and recruit medical professional volunteers (nurses, doctors etc.) to aid African children in need. 

He wants to explore the dataset in order to identify (1) which countries in Africa may need this help the most, and (2) what the most common preventable and treatable causes of child deaths are in these countries. Aiden finds some resources with helpful visualizations, and tells his supervisor "Nigeria has the highest number of child deaths. We need to go there first!" Unfortunately, his supervisor informs him that recent civil unrest in Nigeria has made it unsafe for the healthcare volunteer team to travel to. His supervisor provides him with a list of countries that are safe for the volunteers.

Aiden goes back for further research, and he comes across an interactive map provided by the [Gapminder organization](https://www.gapminder.org/tools/#$state$marker$color$which=all_causes_deaths_in_children_1_59_months_total_deaths&use=indicator&scaleType=genericLog&spaceRef:null;;;&chart-type=map)! This interactive map even lets Aiden select different causes of child mortality, so he can receive input from the healthcare volunteers on which infectious diseases are more easily preventable and treatable than others. His supervisor is very impressed and applauds him on a job well done! 

She remembers that the volunteer team commented last year that child mortality from measles, malaria, and meningitis were preventable and treatable with improved child vaccination and availablility of antivirals and antibiotics. She asks Aiden if he can add up the total number of child deaths caused by these three diseases for all 20 of the countries that are safe for the volunteers to travel to. Halfway through wrangling data, Aiden wonders if there is any better way to interactively visualize the number of child deaths caused by different diseases (both individually and in total) for each country.

In this case, ‘African Children Health app’ could be a good place to start. In the app, he can visualize the children (aged 0 -5 years) mortality of every country across the Africa from 1990 – 2015, and the diseases responsible for these deaths. He can rank the countries and the causes of child mortality to figure out which candidates countries may require the most help, and what kind of infectious diseases are most serious in the region. 

Using this information from the app, Aiden can do conduct follow-on research to draft a proposal to his supervisor to suggest the type of medications that are necessary and which countries to deploy the volunteer health care providers.

### Sketch of app:

![](app_sketch.PNG)