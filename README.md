<h1 align="center">IBM Full Stack Software Developer Certificate <br> Capstone </h1>

> The final project for this course has several steps that you must complete.
> To give you an overview of the whole project, all the high-level steps are listed below.
> The project is then divided into several smaller labs that give the detailed instructions for each step.
> You must complete all the labs to successfully complete the project.

## Setup

1. Clone this repository

```bash
git clone https://github.com/vikiru/ibm-fullstack-capstone.git
cd ibm-fullstack-capstone
```

2. Install the required dependencies
   1. Install all Python dependencies
      ```bash
      pip install -U -r requirements.txt
      ```
   2. Install all Node dependencies
      ```bash
      npm install
      ```
3. Setup the `.env` file with the required values (located within `ibm-fullstack-capstone/server/.env.sample`)

   ```text
   # Cloudant Service on IBM Cloud
   IAM_API_KEY = "YOUR-KEY-HERE"
   CLOUDANT_URL = "YOUR-URL-HERE"
   CLOUDANT_USERNAME = "YOUR-USERNAME-HERE"

   # Serverless Function on IBM Cloud
   # Can also use reviews.py and get-dealership.js within functions folder to test locally
   GET_DEALER_URL = "YOUR-URL-HERE"
   GET_REVIEW_URL = "YOUR-URL-HERE"
   POST_REVIEW_URL = "YOUR-URL-HERE"

   # NLU Service on IBM Cloud
   NLU_API_KEY = "YOUR-KEY-HERE"
   NLU_URL = "YOUR-URL-HERE"
   ```

## Usage

1. Start the main Django App

```bash
cd server
python manage.py runserver
```

### Local Development

1. Start the function files located within `ibm-fullstack-capstone/functions`
   1. Start `get-dealership.js`
      ```bash
      npm start
      ```
   2. Start `reviews.py`
      ```bash
      python reviews.py
      ```

## Project Breakdown

**Prework: Sign up for IBM Cloud account and create a Watson Natural language Understanding service**

1. Create an IBM cloud account if you don't have one already.
2. Create an instance of the Natural Language Understanding (NLU) service.

**Fork the project Github repository with a project then build and deploy the template project**

1. Fork the repository in your account
2. Clone the repository in the theia lab environment
3. Create static pages to finish the user stories
4. Deploy the application on IBM Cloud

**Add user management to the application**

1. Implement user management using the Django user authentication system.
2. Set up continuous integration and delivery

**Implement backend services**

1. Create cloud functions to manage dealers and reviews
2. Create Django models and views to manage car model and car make
3. Create Django proxy services and views to integrate dealers, reviews, and cars together

**Add dynamic pages with Django templates**

1. Create a page that shows all the dealers
2. Create a page that show reviews for a selected dealer
3. Create a page that let's the end user add a review for a selected dealer

**Containerize your application**

1. Add deployment artifacts to your application
2. Deploy your application
