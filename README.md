# keyword-generator
This project uses the **Google Ads API to generate keyword ideas through the keyword adplanner feature**. By **defining a seed keywords** you will retrieve related keywords. Every **associated (related) keyword will come with monthly search volume**, average search volume, high- and low bid cpc, concept_group, brand bool and competition index. Generated data will be stored in the data folder in the corresponding **csv file called keyword_ideas.csv**. With a further selection you can upload the data automatically into a new table of your hosted Postgres (Se how to define the .env file further below)

For using this repository **you need first having an active Google Ads account** and at least a **test api token in Google Ads**. Authentication can be troublesome due the fact you need to **register an App on GCP** and **apply for an Google Ads API key**, therefore I am creating currently a blog article that takes you **step by step through the process** (https://medium.com/kuwala-io/navigating-the-google-ads-api-authorization-maze-step-by-step-guide-for-authentication-402313d1bd0d). Once you have your credentials, you can **add credentials into the google-ads.yaml** and the customer_id in the generate_keywords.py, and run the project. 

## Prerequisites

- Python 3.6 or higher
- Git

## Setup

1. **Clone the Repository**

```sh
git clone https://github.com/floriankuwala/keyword-generator.git
cd keyword-generator
```
   
2. **Setup your virtual environment variable**

```sh

   python -m venv my_project_env
   
```

3. **Activate your virtual environment**

- For MacOS

```sh

source my_project_env/bin/activate

```

- For Windows
```sh

.\my_project_env\Scripts\activate

```


4. **Install Requirements**
```sh

pip install -r requirements.txt

```

5. **Set Up Environment Variables (Optional / Coming Soon...)**

Add your credentials for a hosted PostGres in your .env file as following: 

```sh
DB_TYPE=postgresql
DB_USER=your username
DB_PASSWORD=your password
DB_HOST=your hostadress
DB_PORT=5432
```

**AND**

Configure your google-ads.yaml with the following information:
```yaml
developer_token: "your developer token"
client_id: "your client id"
client_secret: "your client secret"
refresh_token: "your refresh token"
use_proto_plus: True
```

**AND**
Adjust your customer_id in the generate_keyword_ideas.py

## Running the Project
```sh

python main.py

```

The terminal will give you multiple options which you can start seperately.
a) generating keyword ideas through google ads api (ads api credentials need to be acquired)
b) creating a table and upload the generated data to a hosted postgres
c) retrieving keywords from database and utilize google trends (output in the corresponding csv as well)


## Folder Structure

```sh
keyword-generator/
│
├── my_project_env/ # Virtual environment folder, e.g. setting env variables for database connection
│
├── src/ # Source code folder
│ └── generate_keyword_ideas.py
│ └── config.py
│ └── db_operations.py
│ └── models.py
│
├── resources/ # Resources like configuration files
│ └── google-ads.yaml # google ads token and api configuration, Please put in here your credentials
│ └── geotargets.csv # list of geotargets and theire corresponding number
│ └── languagecodes.csv # language codes to be set
│
├── data/ # Folder to store input/output data, if needed
│ └── seed_keywords.txt # seed keywords for google ads api (one per line) example: 'Apache 207'
│ └── keyword_ideas.csv # Output when you run the main.py successfully
│
├── logs/ # Log files for errors and other information
│ └── app.log (coming soon)
│
├── tests/ # Test cases
│ └── test_data.py (coming soon)
│
├── .gitignore # Git ignore file to exclude unnecessary files/folders from version control
├── requirements.txt # List of dependencies
├── README.md # Project description and setup instructions
└── main.py # Main script to run
```

