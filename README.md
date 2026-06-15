# 🏅 Olympics Analysis Dashboard

An interactive Streamlit web application for exploring and analyzing over 120 years of Olympic Games data. Dive into medal tallies, country performance trends, athlete demographics, and much more through rich visualizations and intuitive filtering.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### 📊 Medal Tally
- Filter medals by **year** and **country**
- View summary metrics (Gold, Silver, Bronze, Total)
- Styled data table with color gradients for quick insights

### 📈 Overall Analysis
- **Key Statistics**: Total editions, host cities, sports, events, athletes, and participating nations
- **Trend Visualizations**:
  - Participating nations over time (line chart)
  - Events held over time (bar chart)
  - Athlete participation over time (area chart)
  - Events per sport heatmap
- **Top 15 Most Successful Athletes** — filterable by sport

### 🌍 Country Wise Analysis
- **Medal tally per year** — line plot showing a country's total medals across Olympic editions
- **Top sports by medal count** — horizontal bar chart highlighting where a country excels
- **Top 10 most successful athletes** from any selected country

### 🏃 Athlete Wise Analysis
- **Age distribution comparison** (KDE plots) — compare age distributions of all athletes vs. Gold, Silver, or Bronze medalists
- **Age distribution by sport** — overlay density curves for multiple sports

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io/) | Web application framework |
| [Pandas](https://pandas.pydata.org/) | Data manipulation and analysis |
| [NumPy](https://numpy.org/) | Numerical computing |
| [Plotly](https://plotly.com/python/) | Interactive visualizations |
| [Matplotlib](https://matplotlib.org/) | Static visualizations (heatmaps) |
| [Seaborn](https://seaborn.pydata.org/) | Statistical data visualization |
| [SciPy](https://scipy.org/) | Statistical computations (KDE) |

---

## 📁 Project Structure

```
olympics-analysis/
├── app/
│   ├── app.py              # Main Streamlit application (UI + logic)
│   ├── helper.py           # Analytics & visualization functions
│   └── preprocessor.py     # Data preprocessing pipeline
├── data/
│   ├── athlete_events.csv  # 120+ years of Olympic athlete data
│   └── noc_regions.csv     # NOC code to country/region mapping
├── docs/
│   └── frontend-migration-plan.md  # Plan for migrating to React + FastAPI
├── notebooks/
│   ├── analysis.ipynb      # Exploratory data analysis
│   └── test.ipynb          # Testing & experimentation
├── DEPLOYMENT.md           # Deployment guide for Render
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/olympics-analysis.git
   cd olympics-analysis
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   streamlit run app/app.py
   ```

5. **Open in browser**

   The app will launch at `http://localhost:8501` by default.

---

## 📊 Dataset

The project uses two CSV datasets:

### athlete_events.csv
Contains information on every athlete who has participated in the Olympic Games from 1896 to 2016.

| Column | Description |
|---|---|
| ID | Unique athlete identifier |
| Name | Athlete's full name |
| Sex | Gender (M/F) |
| Age | Age at time of the Games |
| Height | Height in cm |
| Weight | Weight in kg |
| Team | Team name |
| NOC | National Olympic Committee code |
| Games | Year and season (e.g., \"2016 Summer\") |
| Year | Year of the Games |
| Season | Season (Summer/Winter) |
| City | Host city |
| Sport | Sport discipline |
| Event | Specific event within the sport |
| Medal | Medal won (Gold/Silver/Bronze) |

### noc_regions.csv
Maps NOC codes to country/region names.

| Column | Description |
|---|---|
| NOC | National Olympic Committee code |
| region | Country or region name |
| notes | Additional notes (historical names, etc.) |

> **Note**: The app filters to **Summer Olympics only** for consistent analysis.

---

## 🌐 Deployment

The app is ready for deployment on [Render](https://render.com/). See [DEPLOYMENT.md](./DEPLOYMENT.md) for step-by-step instructions.

Quick start for deployment:
1. Push to GitHub
2. Connect repo to Render
3. Configure Web Service with start command: `streamlit run app/app.py`

> **⚠️ Free Tier**: Services spin down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.

---

## 🔮 Future Plans

The project has a documented plan to migrate from Streamlit to a more modern architecture:
- **Backend**: FastAPI with pandas-based analytics
- **Frontend**: React with interactive charts
- **API-first design** that decouples data processing from UI

See [docs/frontend-migration-plan.md](./docs/frontend-migration-plan.md) for the full migration plan.

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- [120 years of Olympic history: athletes and results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) dataset on Kaggle
- Streamlit for making data dashboarding accessible
- All Olympic athletes who have inspired generations
