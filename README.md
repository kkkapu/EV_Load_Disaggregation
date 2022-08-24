# EV_Load_Disaggregation
# Overview
The problem of disaggregating BTM EV load traces from smart meter data traces is studied. Based on the characteristics of typical EV charging traces, three interdependent sub-problems are formulated: a) Detecting the presence of BTM EVs, b) Estimating the EV charging rate, and c) Detecting the EV charging periods. A unified iterative algorithmic framework is developed to solve all three sub-problems. Importantly, the proposed algorithms do not assume or utilize the knowledge of ground truth EV load traces but estimate BTM EV load traces in an ``unsupervised'' fashion. Numerical evaluation is conducted based on real-world 15-minute interval smart meter data collected from Austin, TX, and demonstrates great performance achieved by the proposed algorithms. 

# How to use
Before using the code, all the input data and variables should be prepared. 
For each customers, the time information (month/day/hour/minute) and the total consumption information are needed as input. To performe the EV load disaggregation, several steps needs to be done. 
1. classify customers into two groups (customers with EV/customers without EV) by using EV_customer.ipynb and NonEV_customer.ipynb (this part needs to be updated) as well as the standards proposed in the paper [link]. 
2. Use Charging_Rate_Estimation.ipynb to estimate the charging rate for EV customers. 
3) EV load disaggregation is performed though Disaggregation.ipynb and the estimated charging rates are needed as input (from step2). 
