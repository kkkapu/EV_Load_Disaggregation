# EV_Load_Disaggregation
# Overview
The problem of disaggregating BTM EV load traces from smart meter data traces is studied. Based on the characteristics of typical EV charging traces, three interdependent sub-problems are formulated: a) Detecting the presence of BTM EVs, b) Estimating the EV charging rate, and c) Detecting the EV charging periods. A unified iterative algorithmic framework is developed to solve all three sub-problems. Importantly, the proposed algorithms do not assume or utilize the knowledge of ground truth EV load traces but estimate BTM EV load traces in an ``unsupervised'' fashion. Numerical evaluation is conducted based on real-world 15-minute interval smart meter data collected from Austin, TX, and demonstrates great performance achieved by the proposed algorithms. 

# How to use
Before using the code, all the input data and variables should be prepared. 
For each customer, the time information (month/day/hour/minute) with the corresponding temperature at that time and the total consumption information are needed as input. To perform the EV load disaggregation, several steps needs to be done. 
1. Use EV_Presence_Detection.ipynb to classify customers into two groups (customers with EV/customers without EV).
2. Use Charging_Rate_Estimation.ipynb to estimate the charging rate for EV customers. 
3. Use Disaggregation.ipynb and the estimated charging rates from step2 to do EV load disaggregation.

# EV Presence Detection
This part tries to identify whether a customer owns an EV or not. 
- Input: the information from individual customer (should be preprared as mentioned above).
- Output: estimatd charging rate, average charging hours, average temperature during charging hours.
The three outputs will used to classify customers into with group/without EV group according to the strandards proposed in the paper.




