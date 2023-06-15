# Django Nearby Shops Application

This Django application provides functionality to manage and display a list of nearby shops. It includes the following URL patterns:

[Click here to visit the deployment on railway.app](https://web-production-a819.up.railway.app/)

## Home

- URL: `/`
- Name: `home`
- Description: This is the landing page of the application. It provides an overview of the nearby shops feature.

## Shops List

- URL: `/shops`
- Name: `shops_list`
- Description: Displays a page that lists all the shops in the database as a table. Provides options to edit and delete shop entries.

## Edit Shop

- URL: `/edit_shop/`
- Name: `edit_shop`
- Description: Displays a page to add a new shop or edit an existing shop. If no `shop_id` is provided, it opens a blank form for adding a new shop. If `shop_id` is provided, it pre-fills the form with the existing shop details for editing.

## Delete Shop

- URL: `/delete_shop/<int:shop_id>/`
- Name: `delete_shop`
- Description: Deletes the shop with the specified `shop_id` from the database.

## Nearby Shops

- URL: `/nearby_shops/`
- Name: `nearby_shops`
- Description: Allows users to find and display a list of shops located within a specified radius from their current location. The user needs to provide latitude, longitude, city, and search radius in the request.

## Finding Nearby Shops

The Nearby Shops application utilizes the Haversine formula to calculate the distance between a user's current location and the shops in the database. The Haversine formula is commonly used to compute the great-circle distance between two points on a sphere, such as the Earth.

The Haversine formula takes into account the latitude and longitude coordinates of the user's current location and each shop's location. By calculating the distance between these points, the application determines which shops are within a specified radius of the user.

### Calculation Steps and additonal considerations
Note: Users are requested to enter latitude and longitude calues in decimal degrees which is the standard used by many gps applications. These need to be converted to radians before applying haversine formula cause python's math functions use radians for calculation.

1. The user submits their current latitude, longitude, city, and the desired search radius. (Here, instead of a form input from the user, we could also use Geolocation API provided by HTML to pull the coordinates of the user if they agree on sharing their location)

2. The application retrieves all shops in the specified city from the database. (This is an additional consideration that I have taken because it's in a real world scenario the city of the shop would be mentioned. This allows us to narrow our search down and compute the distance of less shops rather than computing the distance of all the shops in the database. This can be made more efficient by adding an additonal filter of category during the search)

3. For each shop, the Haversine formula is applied to calculate the distance between the user's location and the shop's location.

4. If the calculated distance is less than or equal to the search radius, the shop is considered within the user's vicinity.

5. The application creates a list of shops within the specified radius, including their distances from the user.

6. The list of nearby shops, along with the search radius, is then displayed to the user on the Nearby Shops page.


## Nearby Shops - Local Development Guide

This guide provides step-by-step instructions on how to set up and run the Nearby Shops project locally on your machine. Make sure you have Python and pip installed before proceeding.

### Prerequisites

- Python 3.9.16
- pip package manager

### Setup Instructions

1. Clone the repository:

```
$ git clone https://github.com/ProPegasus/nearby-shops.git
$ cd nearby-shops
```

2. Create a virtual environment and activate it:

```
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Install the project dependencies using pip:

```
$ pip install -r requirements.txt
```

### Running the Application

To run the Nearby Shops application locally, follow these steps:

1. Activate the virtual environment if it's not already activated:

```
$ source venv/bin/activate
```

2. Run the Django development server:

```
$ python manage.py runserver
```

3. Open your web browser and visit `http://localhost:8000` to access the application.

### Running Test Cases

The Nearby Shops project includes test cases to ensure the correctness of its functionality. To run the test cases, follow these steps:

1. Activate the virtual environment if it's not already activated:

```
$ source venv/bin/activate
```

2. Run the test command:

```
$ python manage.py test
```

The test runner will execute all the test cases and provide the test results in the terminal.

## Deploying Nearby Shops on Railway.app

This guide provides step-by-step instructions on how to deploy the Nearby Shops application on railway.app. Railway.app is a platform that simplifies the deployment of web applications directly from a GitHub repository.

### Prerequisites

- A GitHub account
- Nearby Shops project repository on GitHub

### Deployment Instructions

1. Create a `Procfile` in the root directory of your Nearby Shops project with the following content (Already provided in this repo):

```
web: gunicorn 'nearby_shops.wsgi'
```

This file specifies the command to start the web server (we are using gunicorn).

2. Create a `runtime.txt` file in the root directory of your Nearby Shops project with the following content((Already provided in this repo)):

```
python -3.9.16
```

This file specifies the Python runtime version to be used.

3. Open your web browser and visit [railway.app](https://railway.app). Log in with your GitHub account.

4. Click on the "New Project" button to create a new project on railway.app.

5. Select your Nearby Shops project repository from the list of repositories.

6. Review the project settings and make sure the deployment configuration is correct, including the correct branch to deploy.

7. Click on the "Deploy" button to start the deployment process.

8. Wait for railway.app to deploy your application. The deployment process may take a few moments.

9. Once the deployment is complete, railway.app will provide you with the URL where your Nearby Shops application is hosted. You can access the application using that URL.

### Additional Notes

- If you encounter any issues during the deployment process, refer to railway.app's documentation or support resources for troubleshooting steps.

- Make sure your GitHub repository is up to date with the latest changes before initiating the deployment to ensure the deployed application reflects the latest code.

## What could have been implemented
1. Having a logging mechanism to log info, warnings and errors
2. Using environment variables provided by Railway.app to store django secret key
3. A full-fledged SQL database instead of sqlite

