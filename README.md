# Data Analysis and Log Monitoring of Clash of Clans War Data

### Overview

I created this program to allow for people in my clan to look at the current war stats for clanmates, as well as easily visualize trends. I chose to utilize Pandas for data manipulation and chart creation.
An example chart with war data is shown below.

![Image](/images/example.png)

In a war, each member can attack up to two times and can get up to 200% destruction and 6 stars total. I created custom columns by manipulating the JSON response provided by the official Clash of Clans API
to better show relevant stats for each member. Additionally, the chart automatically color codes people who have no attacked yet as red, people who have attacked once as yellow, and people who have completed
all of their attacks as green, making it easy to determine who needs to be reminded to play. I have a CRON task set up to run the script once a day to collect relevant information and log the event. I can take
the JSON files that are generated from the task and automatically export them as Excel tables for my clanmates, or for further analysis with Pandas.

I also wanted to visualize the log data, and check for any errors. I wrote another script to analyze this data and some of the results are shown below.

![Image](.images/distribution) ![Image](.images/hourly) ![Image](.images/types)
