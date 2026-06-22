# Airline-Loyalty-Program
#  SkyReward — Airline Loyalty Retention Intelligence

A behavioral analytics project built for the **Consulting & Analytics Club, IIT Guwahati — Summer Projects 2026**.

---

##  Problem Statement

Airlines lose high-value customers silently — members stop flying months before they formally cancel. This project builds a data-driven system to predict who is at risk of disengaging, segment customers by value, and recommend specific retention actions before it's too late.

---

##  What This Project Does

- **Churn Prediction** — Gradient Boosting model (AUC = 0.85) trained on 2017 behavioral data to predict 2018 disengagement. Churn is defined as formal cancellation OR zero flights in 2018 — catching 661 silent churners a cancellation-only model would miss.

- **Customer Segmentation** — KMeans clustering (k=4) producing four actionable segments: Loyalists, Champions, Dormant, and At-Risk, each with a distinct retention strategy.

- **Retention Playbook** — Three specific recommendations with named segments, triggers, channels, cost estimates, and success metrics — ready to hand to a marketing operations team.

- **Interactive Dashboard** — A Streamlit app a non-technical marketing manager can use without guidance.

---

##  Dataset

- `Customer_Loyalty_History.csv` — 16,737 members, demographics, CLV, card tier, cancellation records
- `Customer_Flight_Activity.csv` — 392,936 monthly flight activity records (2017–2018)
- `Calendar.csv` — Date dimension
- `Airline_Loyalty_Data_Dictionary.csv` — Column definitions

---

##  Key Findings

- **16.3% churn rate** — 2,067 formal cancellations + 661 behavioral churners
- **Tenure (49.8%)** and **Flight Consistency (40.5%)** drive 90%+ of churn — it's an onboarding problem, not a demographic one
- **Salary and demographics contribute <1%** — retention is behavioral
- **Loyalists (59.7% of members)** churn at only 4.6% — the highest ROI retention target
- **Champions (37.7% of members)** churn at 34.8% — biggest conversion opportunity

---

##  Tech Stack

- **Python** — Pandas, Scikit-learn, Matplotlib
- **ML Models** — Logistic Regression, Random Forest, Gradient Boosting
- **Clustering** — KMeans (k=4)
- **Dashboard** — Streamlit + Plotly

---

##  Live App

https://airline-loyalty-program-jkapxtutow3keevwljcfu4.streamlit.app/

---

##  Run Locally

```bash
git clone https://github.com/abhitmukhija/Airline-Loyalty-Program.git
cd Airline-Loyalty-Program
pip install -r requirements.txt
streamlit run app.py
```

---

##  Project Structure
```
├──Customer_Loyalty_History.csv
├── Customer_Flight_Activity.csv
├── Calendar.csv
├── Airline_Loyalty_Data_Dictionary.csv
├── final_results.csv          # Scored dataset with churn probability + segments
├── pipeline.ipynb             # Full ML pipeline — cleaning, features, model, segmentation
├── app.py                     # Streamlit dashboard
├── requirements.txt
└── README.md
```
---

##  Done By

**Abhit and Ashish** —  IIT Guwahati
Consulting & Analytics Club | Summer Projects 2026
