# Project Description
Loews aims to develop a locust early warning system leveraging Geospatial Data to map locust breeding grounds for early intervention. It provides up-to-date information and analysis on locust outbreaks and mitigation measures in Kenya to stakeholders such as farmers, the government, and other agencies. 

To identify breeding grounds, Loews utilizes a Random Forest Model trained on 5000 Geospatial Data Points with main features including Rainfall, Temperature, and Soil Type. The mapping of breeding grounds is visualized using the Folium Library, with markers indicating possible breeding grounds and land sizes. 

Additionally, visualizations on the Analytics Page utilize Synthetic Data generated using the Faker Library, simulating data that will be collected from farmers on locust sightings in Kenya. 

The Chatbot Functionality is implemented using Retrieval Augmented Generation (R.A.G) Technique, utilizing tools such as FAISS for vector store simulation, OpenAI Embeddings, and Langchain Library. This chatbot provides updated information on Highly Hazardous Pesticides (HHP) currently in use in Kenya.Future plan is to have this not provide updated information on Locust Outbreaks, Strategies/Measures from Credible Sources such as Ministry of Agriculture e.t.c to counter `gpt3.5-turbo` Hallucinations & lack of updated information.

## Local Project Set Up
To set up Loews locally:

1. Create a virtual environment locally and clone the project - either use conda or venv.
2. Configure Project API Key on OpenAI Platform.
3. Set Up an env file with the following secret keys - `SECRET_KEY`, `OPENAI_API_KEY`, and `DEBUG`.
4. Install the required libraries from `requirements.txt`.
5. Carry out Database Migrations - `python manage.py makemigrations`, then `migrate`.
6. Set Up a Superuser - `python manage.py createsuperuser`.
7. Run the Project - `python manage.py runserver 3000`.
8. Project APP URL - [http://127.0.0.1:3000/coreapp/](http://127.0.0.1:3000/coreapp/)

### Sample Pages
- ![Home Page](https://github.com/john-thuo1/loews/assets/108690517/34ab9c61-c028-4731-a192-e293669b767e)
- ![Analytics Page](https://github.com/john-thuo1/loews/assets/108690517/e7c4a91f-ae5d-4165-a6c9-3eeb3ea5a255)

## Future Steps
1. Automating Data Processing Steps using tools such as Airflow.
2. Implementing Realtime Predictions on the App. Predictions have been made in the [Collab File](https://colab.research.google.com/drive/1ZmHPuyaNubCCN9yNE9ofV-_Z3FJKc0WQ?usp=sharing) and only mapped out in the Application for Visualization Purposes. 
3. Incorporate Multilanguage Support.
