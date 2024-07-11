# Project Description
Loews is a locust early warning system leveraging Geospatial Data to map locust breeding grounds for early intervention. It provides up-to-date information and analysis on locust outbreaks and mitigation measures in Kenya to stakeholders such as farmers, the government, and other agencies. 

Loews utilizes a Random Forest Model trained on 5000 Geospatial Data Points to identify breeding grounds with main features including Rainfall, Temperature, and Soil Type. The mapping of breeding grounds is visualized using the Folium Library, with markers indicating possible breeding grounds and land sizes. 

Additionally, visualizations on the Analytics Page utilize Synthetic Data generated using the Faker Library, simulating data that will be collected from farmers on locust sightings in Kenya. 

The Chatbot Functionality is implemented using the Retrieval Augmented Generation (R.A.G) Technique, utilizing tools such as FAISS for vector store simulation, OpenAI Embeddings, and Langchain Library. This chatbot provides updated information on Highly Hazardous Pesticides (HHP) currently in use in Kenya.  The future plan is to have this provide updated information on Locust Outbreaks, Strategies/Measures from Credible Sources such as the Ministry of Agriculture, etc., to counter `gpt3.5-turbo` Hallucinations and lack of updated information.

## Local Project Set Up
#### To set up Loews locally without Docker:

1. Create a virtual environment locally, activate it and then clone the project - `python -m venv loews_project`.
2. Cd into the `loews` directory.
3. Configure your own Project API Key on OpenAI Platform.
4. Set Up an env file with the following secret keys - `SECRET_KEY`, `OPENAI_API_KEY`, and `DEBUG`.
5. Install the required libraries from `requirements.txt`.
6. For FAISS installation, install the binary package -  `pip install faiss-cpu` or with CUDA Support.
7. Carry out Database Migrations - `python manage.py makemigrations`, then `migrate`.
8. Set up a media directory on the Current Directory.
9. Set Up a Superuser  - `python manage.py createsuperuser`.
10. Run the Project - `python manage.py runserver 3000`. 
11. Project APP URL - `http://127.0.0.1:3000`
12. Log in on the backend with the details entered on Step 9 to view reports/chats - `http://127.0.0.1:3000/admin`  

#### To set up Loews locally using Docker Image ( if you have Docker Desktop already installed and running):

1. Navigate to the Project Directory after Step 1 above(^) and build the Docker Image - `docker-compose build`.
2. Once the image is built successfully, run the Docker container - `docker-compose up`.
3. After container is running, login to the app's Backend via `http://127.0.0.1:3000/admin` with username : `admin` password : `avatar1234!`.
4. Note, you can change the Backend Credentials by editing them on the `Dockerfile & docker-compose.yaml` files.
5. Frontend Application  Access url - `http://127.0.0.1:3000`.
6. To remove the Docker container and image - `docker-compose down`.
7. Check out `Dockerfile & docker-compose.yaml` to see how the Image file is set up.


### Sample Pages
- ![Home Page](https://github.com/john-thuo1/loews/assets/108690517/34ab9c61-c028-4731-a192-e293669b767e)
- ![Analytics Page](https://github.com/john-thuo1/loews/assets/108690517/e7c4a91f-ae5d-4165-a6c9-3eeb3ea5a255)
- ![Chatbot Page](https://github.com/john-thuo1/loews/assets/108690517/eaecb147-dee4-4efc-9563-4897a64c054b)

### Model Training & Optimization using mlflow
You can use the parameters registered to train your RandomForest Model to obtain a similar model.
![model tracking & registration](https://github.com/john-thuo1/ai_loews/assets/108690517/564ed5f1-697d-4ca2-9b0e-a41310de4c60)
![model registered](https://github.com/john-thuo1/ai_loews/assets/108690517/37c86f28-4218-4c34-a862-d2c8995d17ac)

## Future Steps
1. Set Up an Automated ETL Data Process, preferably using Airflow. 
2. Implement Real-time Predictions on the App with models running on AWS. Processing and predictions have been made in the [Collab File](https://colab.research.google.com/drive/1ieuJfoAEtqtNDgAZYtEwhOOobt2EbDLc?usp=sharing), and the Predicted Outputs are mapped out in the Application for Visualization Purposes. 
3. Incorporate Multilanguage Support.
4. Implement an efficient method of Referencing Chat Outputs for RAG. Currently, I have only included the PDF Source as my reference. However, the References should refer to the exact text chunks extracted and the associated citations.
