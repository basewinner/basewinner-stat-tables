# Basewinner Offense

This app will enable you to navigate to three different React tables to access unique and proprietary MLB stats.

## Database Schema and API

The raw data that is used in this project is scraped from fangraphs.com. We use Pandas to transform the some of raw data into Basewinner ratings and numbers.

The data is then stored in a SQlite database. The ORM used is Peewee.

Here is the database schema for the table.

![](src/pictures/basewinner-offense-schema.jpg)

### Links to API

Season batting : https://basewinner.com/batting/batters.json

By Week batting : https://www.basewinner.com/batting/aggregated_batting.json
