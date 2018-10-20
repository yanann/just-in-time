# just-in-time
Slackbot that posts estimated travel time for given location

## Context
In business school, we are often scheduling dinners in Slack. Sometimes we would like to know how far away a restaurant is but unfortunately, most of us are still unfamiliar with the area. The current process flow is opening Google Maps to locate and get an estimated time for the destination. This process is inconvenient since it requires opening a new browser and then relaying the information back to the Slack channel.

## Solution
Just-in-time Slack Bot allows users to ask for travel times to event locations near Harvard Business School. Users just have to mention the app and then type out "travel time to X", where X can be an exact address or the name of a restaurant. The bot then uses Google Places and Google Distance Matric to calculate the estimated travel time.

If there are multiple possible matches to a restaurant name, the bot will list the top 5 locations based on Google Places Autocomplete API. Users then have to type in the place they selected.

![](https://github.com/yanann/just-in-time/blob/master/images/screenshot.png | width = 50)
