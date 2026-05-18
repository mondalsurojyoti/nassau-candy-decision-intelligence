# Nassau Candy — Decision Intelligence

Nassau Candy Decision Intelligence is a robust, data-driven web application built with Streamlit designed to optimize factory reallocation and shipping logistics. It provides real-time, predictive insights to streamline operations, reduce lead times, and maintain financial stability for distribution networks.

## Features

- **Factory Optimization Simulator:** Simulates reallocation of products across different factories based on dynamic parameters such as speed priority, product, region, and shipping mode.
- **What-If Analysis:** Compares current factory assignments against machine-learning-recommended optimal factories, highlighting time saved, percentage reduction, and margin impacts.
- **Risk & Impact Assessment:** Evaluates potential operational risks and profitability impacts of suggested reallocations, ensuring that speed is balanced with cost-efficiency.
- **Recommendation Dashboard:** Delivers actionable insights, ranking alternative factory assignments and calculating composite scores based on geographic drag and predictive lead times.
- **Professional Analytics Interface:** Features a modern, polished dark-themed UI with dynamic KPI cards, comprehensive metrics tracking (R², MAE, RMSE), and interactive tables.

## Project Structure

- `app.py`: The main Streamlit dashboard application.
- `config.py`: Contains configurations, mappings (Product, Division), and KPI definitions.
- `data_prep.py`: Handles data loading and preprocessing logic.
- `model.py`: Implements the predictive model for lead time estimation.
- `optimizer.py`: Contains simulation logic and KPI computation functions.
- `requirements.txt`: Project dependencies.
- `Nassau Candy Distributor.csv`: The core dataset utilized for simulation and modeling.

## Installation

1. **Clone the repository** (if applicable) or download the project files.
2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Start the Streamlit application by running the following command in your terminal:

```bash
streamlit run app.py
```

The application will launch in your default web browser (typically at `http://localhost:8501`). Use the sidebar to select your desired parameters (Product, Region, Ship Mode, and Priority) to interact with the simulations.

## Built With

- [Streamlit](https://streamlit.io/) - Web framework for data applications
- [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) - Data manipulation
- [Scikit-Learn](https://scikit-learn.org/) - Machine learning and modeling
- [Haversine](https://pypi.org/project/haversine/) - Geographic calculations

## License

© 2024 Nassau Candy Decision Intelligence. All rights reserved.
