# EV_Load_Disaggregation
# Overview
The problem of disaggregating BTM EV load traces from smart meter data traces is studied. Based on the characteristics of typical EV charging traces, three interdependent sub-problems are formulated: a) Detecting the presence of BTM EVs, b) Estimating the EV charging rate, and c) Detecting the EV charging periods. A unified iterative algorithmic framework is developed to solve all three sub-problems. Importantly, the proposed algorithms do not assume or utilize the knowledge of ground truth EV load traces but estimate BTM EV load traces in an ``unsupervised'' fashion. Numerical evaluation is conducted based on real-world 15-minute interval smart meter data collected from Austin, TX, and demonstrates great performance achieved by the proposed algorithms. 

# How to use
Before using the code, all the input data and variables should be prepared. 
For each customer, the time information (month/day/hour/minute) with the corresponding temperature at that time and the total consumption information are needed as input. The sample data file can be found in the "sample data" folder and it contains the following variables.
- dataid: the id of the customer
- local_15min: the time index
- grid: the netload data
- solar: ground truth of the solar generation
- car: the EV charging load
- Month: month of the year (between 1 and 12)
- Day: day of the month (between 1 and 31)
- Hour: hour of the day (between 0 and 23)
- Minute: minute of the hour (between 0 and 59)
- temperature: temperature at the given time index
- air1: the air conditioning load
- weekday: day of the week (between 0 and 6)
- consumption: the ground truth total load (= the netload + the ground truth solar generation) 

To perform the EV load disaggregation, several steps needs to be done. 
1. Use EV_Presence_Detection.ipynb to classify customers into two groups (customers with EV/customers without EV).
2. Use Charging_Rate_Estimation.ipynb to estimate the charging rate for EV customers. 
3. Use EV_Load_Disaggregation.ipynb and the estimated charging rates from step2 to do EV load disaggregation.

# EV Presence Detection (EV_Presence_Detection.ipynb)
This part tries to identify whether a customer owns an EV or not. 
- Input: information from individual customer (should be preprared as mentioned above).
- Output: estimatd charging rate, average charging hours, average temperature during charging hours.
The three outputs will used to classify customers into with group/without EV group according to the standards proposed in the paper.

# Charging Rate Estimation (Charging_Rate_Estimation.ipynb)
This part tries to estimate the charging rate of EV owners.
- Input: information from customers who are identified as owning EVs.
- Output: estimated charging rate for each customer

# EV Load Disaggregation (EV_Load_Disaggregation.ipynb)
This part tries to disaggregation the EV load from the total load of individual customers.
- Input: information from customers who own EVs as well as the estimated charging rate from step2
- Output: EV charging load profile for each customer (including start, end, and charging rate for each charging period)



