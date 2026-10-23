# OLA Ride Insights

## Project Overview

OLA Ride Insights is a data analytics project focused on analyzing ride-booking data to understand booking trends, vehicle performance, revenue, cancellations, and customer and driver ratings. The project uses interactive dashboards to present insights and support data-driven business decisions.

## Live Dashboards

- Streamlit Application: [https://ridespheres-tnazbhfgsb4bxeq3e63c9.streamlit.app/](https://ridespheres-tnazbhfgsb4bxeq3e63c9.streamlit.app/?utm_source=chatgpt.com)
- Power BI Dashboard: [https://app.powerbi.com/reportEmbed?reportId=4172a321-48ac-4c0e-be74-8593ebe98feb&autoAuth=true&ctid=4580cbc0-d2d6-45ab-a7e4-3f99149acd27](https://app.powerbi.com/reportEmbed?reportId=4172a321-48ac-4c0e-be74-8593ebe98feb\&autoAuth=true\&ctid=4580cbc0-d2d6-45ab-a7e4-3f99149acd27\&utm_source=chatgpt.com)

## Objectives

- Analyze total bookings and booking-status distribution.
- Compare bookings across different vehicle types.
- Analyze booking value and payment methods.
- Identify customer and driver cancellation patterns.
- Evaluate customer and driver ratings.
- Present insights through interactive dashboards.

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly
- Power BI
- SQL
- Hadoop MapReduce
- AWS EC2
- Amazon S3
- Git and GitHub

## Project Structure

```
OLA-Ride-Analytics-Big-Data-Cloud/
│
├── README.md
├── dataset/
│   └── Bookings_Cleaned.csv
│
├── hadoop-mapreduce/
│   ├── src/
│   │   └── BookingsAnalysis.java
│   ├── output/
│   │   └── part-r-00000
│   └── README.md
│
├── aws-cloud-infrastructure/
│   ├── ec2/
│   └── s3/
│
├── power-bi-dashboard/
│   └── OLA_Ride_Analytics.pbix
│
├── streamlit-dashboard/
│   ├── app.py
│   └── requirements.txt
│
├── analytical-outputs/
├── project-documentation/
└── project-screenshots/
```

## Streamlit Dashboard Features

The Streamlit application contains five sections:

1. Overall: Booking KPIs, vehicle-type distribution, booking-status distribution, and daily successful-booking trends.
2. Vehicle Type: Booking counts, booking value, ride distance, and ratings by vehicle type.
3. Revenue: Booking value trends, successful booking value, and payment-method analysis.
4. Cancellation: Customer cancellations, driver cancellations, cancellation rates, and cancellation reasons.
5. Ratings: Customer and driver rating analysis by vehicle type.

The application also includes a date-range filter and interactive charts.

## Power BI Dashboard

The Power BI dashboard provides visual analysis of ride volume, booking status, vehicle types, cancellation reasons, payment methods, ride distance, and customer and driver ratings.

## Installation and Execution

### 1. Clone the repository

```
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd <YOUR-REPOSITORY-FOLDER>
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the Streamlit application

```
streamlit run app.py
```

Ensure that the dataset and logo are available at the paths configured in the application.

## Deployment

The Streamlit application can be deployed using Streamlit Community Cloud.

1. Upload the project code to GitHub.
2. Ensure that `app.py`, `requirements.txt`, and required assets are committed.
3. Connect the GitHub repository to Streamlit Community Cloud.
4. Select the correct branch and application file.
5. Deploy and verify the application.

## Expected Outcomes

- Interactive visualization of ride-booking trends.
- Analysis of revenue, cancellations, and ratings.
- Comparison of vehicle performance.
- Accessible dashboards for exploring business insights.
- Organized source code and project documentation.

## Security Considerations

- Do not upload AWS access keys, secret keys, passwords, or tokens.
- Do not publish sensitive customer information.
- Include actual source code and generated outputs in the repository.
- Verify that the required dataset and assets are available to the deployed application.

## Conclusion

OLA Ride Insights combines data analysis, business intelligence, and interactive dashboard development to explore ride-sharing operations. The project uses Streamlit and Power BI to present booking patterns and operational insights in an accessible format.
