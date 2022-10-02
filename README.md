# Project Title

Converting XML to JSON using boto3 and Localstack

## Description

In this project we convert xml files to json. Files are stored on S3 bucket and the solution continuously monitors the S3 bucket.
Once a new files arrives in sqs queue notification triggers and it downloads the file to local system. Conversion starts
and new file in json format gets uploaded in different S3 bucket.

## Getting Started

Below are the steps needed to run the application

### Dependencies

* Python >= 3.8
* Docker
* Localstack

### Executing program

* Download or clone the repository in your system.
* Create virtual environment and activate it.
* Run requirements.txt file to install required modules.
```
pip install -r requirements.txt
```
* Update the environment variables in .env file
* Build the image of the project by running the below command
```
docker build -t myimage .
```
* Change the parameters in docker-compose.yml file according to your environment like image name, container etc
* Run docker compose command command
```
docker-compose up
```
* To test it locally using localstack run the run.py file in pycharm or any IDE.

## Authors

Lalit

## Version History

* 0.1
    * Initial Release