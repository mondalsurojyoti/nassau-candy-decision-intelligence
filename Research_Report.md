# Optimizing Supply Chain Logistics: A Decision Intelligence Framework for Nassau Candy

## 1. Abstract
This paper details the development and implementation of a Decision Intelligence application designed to optimize factory reallocation and shipping logistics for Nassau Candy. By leveraging machine learning for lead time prediction and a deterministic optimization engine, the platform provides actionable recommendations to minimize geographic drag, reduce shipping delays, and maintain financial stability (margins). The solution is deployed as an interactive Streamlit web application.

## 2. Introduction
In modern supply chain management, balancing the speed of delivery against the cost of freight is a critical challenge. Distributors often rely on static, historical factory assignments that do not account for dynamic variables such as changing shipping modes, regional demand shifts, and factory capacities. This project introduces a predictive analytics framework that evaluates current supply chain routes and recommends optimal factory reallocations using data-driven insights.

## 3. Methodology

### 3.1 Data Preparation
The dataset (`Nassau Candy Distributor.csv`) comprises historical logistics data including product categories, regional destinations, shipping modes, margins, and historical lead times. Data preprocessing involves handling missing values, encoding categorical variables (e.g., Region, Ship Mode), and generating spatial features such as estimated distance (km) using Haversine formulas based on factory locations.

### 3.2 Predictive Modeling
A machine learning regression model (via Scikit-Learn) is trained to predict the **Lead Time (in Days)** for any given combination of Product, Factory, Region, and Ship Mode. 
- **Features Used:** Distance, Ship Mode Weight, Product Category, and Region Encodings.
- **Target Variable:** Actual Historical Lead Time.
- **Evaluation Metrics:** The model's performance is monitored using R² (variance explained), Mean Absolute Error (MAE), and Root Mean Square Error (RMSE).

### 3.3 Optimization Engine
The core of the decision intelligence system is the optimization simulation. For a user-defined scenario (Product, Region, Ship Mode), the system simulates the predicted lead time and margin impact across all available factories. 
A **Composite Score** is calculated based on a weighted priority slider (Speed vs. Profit):
`Composite Score = (Normalized Speed * Speed Weight) + (Normalized Margin * Profit Weight)`

## 4. System Architecture
The application is structured into modular Python components:
- `app.py`: The frontend UI built with Streamlit, handling user inputs, dynamic KPI rendering, and visual charts.
- `model.py`: Encapsulates the training and inference pipeline for the predictive model.
- `optimizer.py`: Houses the simulation logic, comparing current factory assignments against all permutations to rank the best alternatives.
- `data_prep.py`: Data cleaning and feature engineering pipelines.

## 5. Results and Business Impact
The interactive dashboard successfully identifies inefficiencies in current logistics routes. For example, by simulating what-if scenarios, the application can detect when switching a product's originating factory reduces lead time by several days with minimal or positive impact on profit margins. 

The Risk & Impact panel further ensures that automated recommendations do not erode profitability, flagging high-risk routes that require executive oversight.

## 6. Conclusion
The Nassau Candy Decision Intelligence application demonstrates how predictive machine learning can be combined with user-driven optimization to solve complex logistics problems. The system provides a scalable, professional-grade tool for supply chain managers to make informed, mathematically backed decisions.
