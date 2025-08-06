# STEDI Human Balance Analytics

## Contents
- [Overview](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#overview)
	1. [Project Details](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#project-details)
	2. [Project Summary](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#project-summary)
- [Methodology](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#methodology)
  1. [Landing Zone](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#landing-zone---landing)
  2. [Trusted Zone](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#trusted-zone---trusted)
  3. [Curated Zone](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#curated-zone---curated)
- [Acknowledgements](https://github.com/AnuragSinghal16/Udacity---STEDI-Human-Balance-Analytics/edit/main/README.md#acknowledgements)

## Overview
In this project, I will act as a data engineer for the STEDI team to build a data lakehouse solution for sensor data that trains a machine learning model.

### Project Details
The STEDI Team has been hard at work developing a hardware STEDI Step Trainer that:

  - trains the user to do a STEDI balance exercise;
  - and has sensors on the device that collect data to train a machine-learning algorithm to detect steps;
  - has a companion mobile app that collects customer data and interacts with the device sensors.
  - STEDI has heard from millions of early adopters who are willing to purchase the STEDI Step Trainers and use them.

Several customers have already received their Step Trainers, installed the mobile application, and begun using them together to test their balance. The Step Trainer is just a motion sensor that records the distance of the object detected. The app uses a mobile phone accelerometer to detect motion in the X, Y, and Z directions.

The STEDI team wants to use the motion sensor data to train a machine learning model to detect steps accurately in real-time. Privacy will be a primary consideration in deciding what data can be used.

Some of the early adopters have agreed to share their data for research purposes. Only these customers’ Step Trainer and accelerometer data should be used in the training data for the machine learning model.

### Project Summary
As a data engineer on the STEDI Step Trainer team, I will need to extract the data produced by the STEDI Step Trainer sensors and the mobile app, and curate them into a data lakehouse solution on AWS so that Data Scientists can train the learning model.

## Methodology
<img width="897" height="307" alt="image" src="https://github.com/user-attachments/assets/bdf6f19f-be2a-42e5-a37c-0d50bf257f8e" />

### Landing Zone - `./landing/`
To simulate the data coming from the various sources, we will need to create our own S3 directories for customer_landing, step_trainer_landing, and accelerometer_landing zones, and copy the data there as a starting point.

- We have decided we want to get a feel for the data we are dealing with in a semi-structured format, so we decide to create three Glue tables for the three landing zones.
  	1. `customer_landing.sql`
  	2. `accelerometer_landing.sql`
  	3. `step_trainer_landing.sql`
 
### Trusted Zone - `/.trusted/`
The Data Science team has done some preliminary data analysis and determined that the Accelerometer Records each match one of the Customer Records. We need to join customer data with accelerometer data and only include customers who've agreed to share their data for research purposes; to do this, we will only consider customers with `sharewithresearchasofdate` is not null. 

- We create two Glue jobs to send `customer_landing` table and `accelerometer_landing` table into a trusted zone. We will also create a landing table for step trainer data:
	1. `customer_landing_to_trusted.sql` - Sanitize the Customer data from the Website (Landing Zone) and only store the Customer Records who agreed to share their data for research purposes (Trusted Zone)
 	2. `accelerometer_landing_to_trusted.sql` - Sanitize the Accelerometer data from the Mobile App (Landing Zone) - and only store Accelerometer Readings from customers who agreed to share their data for research purposes (Trusted Zone)
	3. `step_trainer_landing_to_trusted.sql` - Read the Step Trainer IoT data stream (S3) and populate a Trusted Zone Glue Table called `step_trainer_trusted` that contains the Step Trainer Records data for customers who have accelerometer data and have agreed to share their data for research (customers_curated)

### Curated Zone - `./curated/`
Data Scientists have discovered a data quality issue with the Customer Data. The serial number should be a unique identifier for the STEDI Step Trainer they purchased. However, there was a defect in the fulfillment website, and it used the same 30 serial numbers over and over again for millions of customers! Most customers have not received their Step Trainers yet, but those who have, are submitting Step Trainer data over the IoT network (Landing Zone). The data from the Step Trainer Records has the correct serial numbers.

The problem is that because of this serial number bug in the fulfillment data (Landing Zone), we don’t know which customer the Step Trainer Records data belongs to.

The Data Science team would like us to write a Glue job that does the following: *Sanitize the Customer data (Trusted Zone) and create a Glue Table (Curated Zone) that only includes customers who have accelerometer data and have agreed to share their data for research called `customers_curated`.*

In this zone, we will create two tables:
1. `customer_curated.sql` - Sanitize the Customer data (Trusted Zone) and create a Glue Table (Curated Zone) that only includes customers who have accelerometer data and have agreed to share their data for research
2. `machine_learning_curated.sql` - Create an aggregated table that has each of the Step Trainer Readings, and the associated accelerometer reading data for the same timestamp, but only for customers who have agreed to share their data

## Acknowledgements
A big thanks to Udacity and NatWest Group for allowing me the opportunity to work on this project!


 
  

