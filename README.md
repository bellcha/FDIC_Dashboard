# FDIC Call Report Dashboard

**Description**

The FDIC Call Report Dashboard allows you to visualize a Bank’s financial performance on a per quarter basis.  The financial data and ratios for this dashboard are from the FDIC’s BankFind Suite API (https://banks.data.fdic.gov/docs/).  The historical stock price data is derived from Yahoo Finance.

**Installation**

I have included a Docker file for easy installation and running the application.  
  -	If you don’t have Docker installed, please see Docker’s official documentation for installation instructions (https://docs.docker.com/get-docker/)
  -	Simply Git clone the project to your local machine or server.  Once downloaded, navigate to the project’s directory.  
  -	Inside the project’s directory, build the docker imager by entering the following command as sudo or administrator: sudo docker build –t fdicdashboard:latest .
  -	Once the docker image is built, start the Docker container with the following command: sudo docker run -d -p 8501:8501 fdicdashboard:latest
  -	Confirm the Docker image is running by entering the following command: sudo docker ps -a
  -	You can navigate to the dashboard by opening your browers and entering the following url: Localhost: http://localhost:8501 or on a server http://serverip:8501 

Example: You can navigate to my instance of the app to see how it looks and feels:  http://dashboard.bellcha.com

**Using the App**

When navigating to the app, the default setting is to display the last five quarters.  In the bar at the top of the screen, you can enter a number between 1 and 30 to display additional historical data.

**Addtional Notes**

Currently, I am on pulling in data for Merchants and Marine Bank.  In the future, I plan to add the ability to search for any Bank that supplies call report data to the FDIC.
