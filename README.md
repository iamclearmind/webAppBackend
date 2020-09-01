# ScreenerBackend

##Description
A Custom backtesting tool for Stock Screening, Backtesting and Signal Generation using [backtrader](https://backtrader.com/)
as a calculation engine. It also includes a flexible data ingestion module currently configured to ingest metastock data
from CSV.

##Simple Run
To ingest data & get a predefined screener output 
1. Goto - ScreenerBackend Directory
2. Type - python3 main.py

ScreenerBackend will ingest the data provided using configrations about datasource like data type, location, handler file
etc from predefined settings in datasource master table in DB.

To get output Screener CSV user must configure the screener_master table in DB, providing data source, startegy location
etc  

##Requirements & Setup
To operate the ScreenerBackend we need to install the requirements and setup the database structure & configurations.
 
The Autointegration module handles all the requirement installation & defualt DB configurations to run the ScreenerBackend

##About

ScreenerBackend contains the following modules performing specific task.
1. DAO Module (Data Acess Object)
1. Data Handler Module
    1. Metastock Handler
1. SPE Module (Strategy Processing Engine)
    1. Screener Engine
    1. Backtest Engine
    1. Custom Indicators
    1. Custom Screeners
    1. Custom Strategies
    1. Data Fetch Module


1. ####DAO Module
    It contains all the configurations & methods used by the ScreenerBackend to interact with database. It contains the
following files:

    1. db_datasource.py
    1. db_properties.py
    1. DAOModule.py
    
    The db_properties.py file contains database connection configuration.
    
    The db_datasource.py file contains function for database connection creation.
    
    The DAOModule.py file contains all functions containing SQL Queries for various tasks ranging from Data Ingestion to
    reading screener configurations for a screener output run. 
    
        Note: Only the DB data fetching methods used by SPE Module are not included in DAOModule.
    
1. ####Data Handler

    Data Handler module is responsible for ingesting Data into the database using configurations stored in datasource_master.
    Data ingestion is done with a custom handler class object specific to a datasource. 

    Ex. Currently to ingest Metastock data from CSV format metastock_handler is used. The handler performs reading,
    filtering, insertion, table creation/management for the specific datasource.

1. ####SPE

    The Strategy Processing Engine (SPE) contains a custom implementation of backtrader backtesting library used to
    calculate the Screener Output, Backtesting Output & the signal generation.
    
    It also includes all the custom indicators, screeners & strategies developed for end use.


## Operating ScreenerBackend

* ####Datasource Handling
    The data ingestion data allows complete flexibilty in handling different types of data sources. This is possible 
    since every datasource must include its handler file. The handler file must contain functions/methods to : -
    * Get list of available Scrips/Stock/Ticker Code & store it  in scrip_master table in DB.
    * Parse Data from available datasource from file formats.

          Note: We can also fetch data from internet source via REST/Websockets/APIs etc by including relevant 
          calls/methods in data_handler file.
    
    To add a new data source enter the configuration in datasource_master with path to source & source_handler file name.
    The new source_handler.py file is to be placed in the "data_handlers" folder.
    
* ####Filtering Scrips
    ScreenerBackend allows for filtering Scrips with both dynamic & permanent static methods.
    
    The permanent static filtering is generally done to exculde some scrips permanently due to various reasons. This is 
    done via adding filter in the source_handler.py file which sets the "isactive" field in scrip_master to 'n'.
    
    Dynamic filtering is implemented in the data fetching methods of data fetch module in SPE. This allows for dynamic
    filters as required. The filter values are stored in "application_properties.py" present in root folder. 
    
* ####Adding Custom Indicators
    ScreenerBackend allows for addition of user build indicators. The indicators are to be placed in "/spe/cust_ind/" 
    folder. The Indicator is a class object derived from the backtrader indicator object.
    
    In standard case a Strategy object is used for interacting with Indicator object. The strategy object calls upon 
    the indicator & handles the output ex. plotting.
    
    For detailed information about creation & plotting of Indicators refer 
    [Backtrader Indicators documentation](https://www.backtrader.com/docu/induse/)

* ####Adding Custom Strategies
    ScreenerBackend allows for addition of Custom Strategies. The Strategies are to be placed in "/spe/strategies/" 
    folder. The Strategy is a class object derived from the backtrader Strategy class object. Strategies are primary
    requirement for Backtesting & Trade Logic generation.
    
    A Strategy object generally contains a indicator upon which a logic is placed to generate buy/sell signals. 

    For detailed information about Strategy creation refer 
    [Backtrader Strategy documentation](https://www.backtrader.com/docu/strategy/)
    
* ####Adding Custom Screeners
    ScreenerBackend allows for addition of Custom Screeners. The Screeners are to be placed in "/spe/screeners/" 
    folder. The Strategy is a class object derived from the backtrader Strategy class object. 
    
    Screeners is a Strategy which applies indicators/conditions on multiple scrips/stocks and export the last datapoints
    of applied idicators/conditions in CSV formatt.
    
    For detailed information about Screener creation refer 
    [Backtrader Strategy documentation](https://www.backtrader.com/docu/strategy/)
    
* ####Screener Run



* ####Backtest Run