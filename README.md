# steam_bi
Fetch and feed data available from Steam's API to industry leading data visualization tools like [Apache Superset](https://superset.apache.org/) and [Microsoft Powerbi](https://powerbi.microsoft.com/en-us/)

## How it Works
1. There is a python script located in python/ that can be ran to gather data from Steam's API
2. Steam Data can then either be written locally as .json files or can be sent to a MySQL database (recommended)
3. Dashboards consisting of Steam data can then be interacted with either in Apache Superset or Microsoft PowerBI

**Note:** Although we think it is totally worth it: There is much more configuration overhead required if intending to use Apache Superset -- especially so for someone not familar with Docker or data visualization tools in general.  

## How to Get Started
### Python
1. Install python
    - Version used: Python 3.10.3
2. Create python virtual environment
    - ```python -m venv venv```
3. Rename config.yaml.sample -> config.yaml
    - Replace steamid and key with your own values
    - The default destination is 'json'
    - 'mysql' can be used as an alternative destination, just fill out the values in the mysql section
4. Activate python virtual environment
    - ```./venv/Scripts/activate```
5. Install dependencies
    - ```pip install -r requirements.txt```

-- If you're not intending to use MySQL or Superset, you can move on to [How to Run](#how-to-run) otherwise continue below to [MySQL](#mysql)

### MySQL
1. Install/Run MySQL
    - For testing I use MySQL running as a docker container: https://hub.docker.com/_/mysql
2. Create the steam_bi database
    - I used https://dev.mysql.com/downloads/workbench/
    - There is a create_db.sql script in the sql/ folder

-- If you're not intending to use Superset, you can move on to [How to Run](#how-to-run) otherwise continue below to [Superset](#superset)  

### Superset
1. Install/Run Superset
    - https://superset.apache.org/docs/installation/installing-superset-using-docker-compose
2. Run the [python](#how-to-run) script
3. Connect to MySQL DB
    - https://superset.apache.org/docs/databases/mysql
4. Create a dashboard (working on supplying one in the repos)
    - https://superset.apache.org/docs/creating-charts-dashboards/creating-your-first-dashboard
    
### PowerBI
1. Install PowerBI Desktop: https://apps.microsoft.com/store/detail/power-bi-desktop/9NTXR16HNW1T?hl=en-us&gl=US
2. Install MySQL Connector/NET 8.0.16: 
    - This is a direct link to the most recent version that works: https://downloads.mysql.com/archives/get/p/6/file/mysql-connector-net-8.0.16.msi
    - This is a link where you can select the version for yourself and can see the MD5 checksums and GnuPG signatures: https://downloads.mysql.com/archives/c-net/
3. Run the [python](#how-to-run) script

- If destination == 'json' Open templates/games_v1-2_json.pbit to see your data
    - You will see an error. This is normal. Go to transform -> Data Source Settings
    - From here you can change the data sources to point to paths of the .json files in data/
    - Once you're done, hit apply and your data will load
    - You will see another file called: steam_bi_steamid_guid.json in data/
        - In order to anonymize the data, all steamids are replaced with a guid
        - This file contains the actual steamids and the guids so you can de-anonymize the data after generating
        - Each guid will be unique per steamid and are re-generated every time new data is fetched 
- If destination == 'mysql' Open templates/games_v2_mysql.pbit to see your data
    - You will see an error. This is normal. Go to transform -> Data Source Settings
    - From here you can change the data source to point to your MySQL DB
    - Once you're done, hit apply and your data will load
- If you use a custom steam url and you don't know your steamid, you can look it up with the following command:
    - Powershell: ```curl.exe YOUR_STEAM_PROFILE_URL | Select-String -Pattern "g_rgProfileData"``

## How to Run
Change to python/ then:
```
python starter.py
```

To see your data, check [Superset](#superset) or [PowerBI](#powerbi) for more information.

## Resources
- [Steam API Key](https://partner.steamgames.com/doc/webapi_overview/auth)
- [Docker](https://docs.docker.com/engine/install/)
- [Apache Superset](https://superset.apache.org/docs/intro)
- [MySQL Docker](https://hub.docker.com/_/mysql)
- [MySQL Workbench](https://www.mysql.com/products/workbench/)
- [PowerBI Desktop](https://powerbi.microsoft.com/en-us/desktop/)

## Sample Output
- [Screenshots](media/screenshots/)
- [PDF - PowerBI Export](https://raw.githubusercontent.com/m-e-w/steam_bi/main/media/pdf/PowerBI_Export.pdf)

Template_V1
![Template_V1](https://raw.githubusercontent.com/m-e-w/steam_bi/main/media/screenshots/Capture_05.PNG)
Template_V2
![Template_V2](https://raw.githubusercontent.com/m-e-w/steam_bi/main/media/screenshots/Capture_04.PNG)




