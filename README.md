![Bull Street](static/media/sell-your-tackle-logo.png)

# Bull Street

### Use Case

A Swiss based family office has contracted me to build an investment analysis platform so them to analyse dividend paying stocks for their yield bearing investment portfolio, with a strong focus on European companies. There are tools out there that cover the companies they want to look at,but one of the biggest challenges they face is building a shortlist of companies they want to understand better in the first place.

To this end, the platform needs to focus on 3 areas:

1. A stock screener that allows the filtering on stock based on yield bearing criteria, namely yield size, payout ratio and price to earnings ratio
2. Individual stock pages where a breakdown of the companies fundamental performance can be tracked
3. An investment note taking feature. As users perform the necessary financial due diligence, it is important that they can take notes of their findings, and be able to edit and delete them. They must be easily accessible as they are often copied and shared in memos internally

The project is split into a react based frontend which can be found [here](https://www.sellyourtackle.co.uk/). This depository is dedicated to the backend, which has been built using Django's Rest Framework

## Project Scope

The scope of this project is to build a robust backend that can serve structured company financial data over an API


### Site Owner and User Goals

As the site owner and user are the same, their gials are the same. There is no plan for them to license this software outside of their own company

* Discover stocks that fit their investment profile
* Help build a dividend paying stock portfolio for their family office, with a focus on European equities
* Keep track of investment ideas and thoughts on companies they have researched
* Include a wide range of key fundamental data for each company, where available. 

Frontend specific goals, such as logging in, SSO, filters and such are outlined in the frontend documentation found [here](https://www.sellyourtackle.co.uk/)


## Project Challenges

Investment decisions are only as good as the data they are based on. Because of this it was critical to choose a data provider who provides a robust financial data api solution that covered European equities. US copmany financial data is easy to find, and plenty of services already cover it, which is why the customer was not interested in including US data. 

The decision was made to use [End Of Day](https://eodhd.com/) fundamental data API. This API covers most of the end points required, and covered the major European exchanges. ALthough their datapoints were harmonised, there was a lot of work needed to manipulate the companies they covered so that only clean versions of each listing remained. 

Because of this, various management commands had to be built to remove unnecessary stocks from the database once stocks had been imported over the API. Due to limitations in EOD's API, there is no way to filter out these companies before they have been imported.

### Challenge 1