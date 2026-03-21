# Frontend Migration Plan: Streamlit to React

## Objective

Shift the current UI from Streamlit to React while keeping the existing pandas-based analytics logic.  
The target architecture is:

- Frontend: React
- Backend API: FastAPI
- Data processing: pandas
- Data source: CSV files in `data/`

This approach is valid and fits the current project structure.

## Current State

Today the project works like this:

- `app/app.py` loads CSV files directly using pandas
- `app/preprocessor.py` preprocesses the Olympics dataset
- `app/helper.py` contains analytics functions such as medal tally and trend calculations
- Streamlit handles both UI and server-side execution in one app

This is simple for prototyping, but it tightly couples UI, data loading, and business logic.

## Proposed Target Architecture

### 1. React Frontend

React will be responsible for:

- page routing
- filters
- tables
- charts
- calling backend APIs
- rendering loading and error states

React should not do pandas work directly. It should only request data from FastAPI and render the response.

### 2. FastAPI Backend

FastAPI will be responsible for:

- exposing REST endpoints
- loading CSV data
- running preprocessing and analytics logic
- returning JSON responses to the frontend

FastAPI will act as the bridge between React and pandas code.

### 3. CSV-Based Data Layer

CSV files can continue to be used:

- `data/athlete_events.csv`
- `data/noc_regions.csv`

FastAPI can read these files with pandas and keep the processed data in memory for API requests.

## Recommended Data Flow

The data flow should be:

1. React sends a request to FastAPI, for example `/api/medal-tally?year=2012&country=India`
2. FastAPI receives the request
3. FastAPI uses pandas and existing helper/preprocessor logic
4. FastAPI converts the result DataFrame into JSON
5. React receives the JSON and updates the UI

In simple terms:

`React -> FastAPI -> pandas/CSV -> FastAPI JSON response -> React UI`

## Important Implementation Note

Do not read large CSV files again on every request if you can avoid it.

Better approach:

- load CSV files when FastAPI starts
- preprocess once at startup
- reuse the in-memory DataFrame for API calls

This will be much faster than calling `pd.read_csv()` for every frontend request.

## Suggested Backend Refactor

Split the current Streamlit-oriented code into backend-friendly modules.

Suggested structure:

```text
backend/
  main.py
  services/
    data_loader.py
    analytics.py
  schemas/
    response_models.py
frontend/
  src/
    pages/
    components/
    services/
```

### Backend responsibilities

- `data_loader.py`
  - read CSV files
  - preprocess data once
  - store shared DataFrames

- `analytics.py`
  - move reusable logic from `helper.py`
  - keep functions pure and independent from Streamlit

- `main.py`
  - define FastAPI app
  - define API routes
  - return JSON responses

## Suggested API Endpoints

Examples based on the current app:

- `GET /api/filters`
  - returns available years and countries

- `GET /api/medal-tally?year=overall&country=overall`
  - returns medal tally table

- `GET /api/overall-stats`
  - returns editions, cities, sports, events, athletes, nations

- `GET /api/participating-nations`
  - returns year-wise trend data

Later you can add:

- `GET /api/country-analysis?country=India`
- `GET /api/athlete-analysis?name=...`

## Response Format

FastAPI should return dictionary/JSON responses.  
That matches your understanding.

Example:

```json
{
  "year": 2012,
  "country": "India",
  "rows": [
    {
      "region": "India",
      "Gold": 0,
      "Silver": 2,
      "Bronze": 4,
      "total": 6
    }
  ]
}
```

If pandas returns a DataFrame, convert it like this conceptually:

- table data: `df.to_dict(orient="records")`
- summary stats: normal Python dict

## Frontend Fetching Approach

React can call FastAPI using `fetch` or `axios`.

Typical frontend flow:

1. user selects filters in React
2. React calls FastAPI endpoint
3. React stores response in component state
4. charts/tables rerender with returned data

Recommended frontend separation:

- `services/api.js` or `services/api.ts` for HTTP calls
- page components for screens
- reusable chart/table components

## Migration Phases

### Phase 1: Separate logic from Streamlit

- remove Streamlit dependency from analytics functions
- keep only pandas-based reusable functions
- isolate data loading and preprocessing

### Phase 2: Build FastAPI backend

- create FastAPI app
- load CSVs on startup
- expose endpoints for current Streamlit screens
- test API responses with browser or Postman

### Phase 3: Build React frontend

- create pages matching current dashboard sections
- build filter components
- fetch backend data
- render tables and charts

### Phase 4: Replace Streamlit UI

- verify React pages match existing outputs
- stop using Streamlit as primary frontend
- keep Streamlit only as fallback if needed

## Mapping from Current App to New Design

Current Streamlit menu items can become React pages:

- `Medal Tally` -> `/medal-tally`
- `Overall Analysis` -> `/overall-analysis`
- `Country Wise Analysis` -> `/country-analysis`
- `Athlete Wise Analysis` -> `/athlete-analysis`

Current Python code mapping:

- `app/preprocessor.py` -> backend preprocessing module
- `app/helper.py` -> backend analytics/service module
- `app/app.py` -> split into React UI + FastAPI routes

## Benefits of This Shift

- better separation of frontend and backend
- easier UI customization than Streamlit
- API can be reused by other clients later
- React gives more control over layout and interactions
- backend analytics logic stays in Python where pandas is strong

## Risks and Considerations

- CSV files are fine for now, but not ideal for high concurrency or frequent updates
- large CSV reads can slow startup
- some current functions are tied to Streamlit assumptions and should be cleaned up
- chart data should be returned as raw series/data points, not Plotly figure objects

For example, `participating_nations_over_time()` should return structured data, and React should build the chart on the frontend.

## Recommendation

Yes, this can be done using:

- React for frontend
- FastAPI for backend
- pandas for analytics
- CSV files for reading data

This is the right next step for moving from a prototype dashboard to a cleaner web application structure.

The main design improvement I recommend is:

- keep CSV reading and preprocessing in FastAPI startup
- reuse existing pandas logic
- return JSON/dict responses
- let React handle all rendering

## Next Implementation Step

Start with backend extraction first:

1. refactor `helper.py` and `preprocessor.py` so they do not depend on Streamlit
2. create FastAPI endpoints for `filters`, `medal-tally`, and `overall-stats`
3. then create React pages that consume those endpoints

That order will reduce risk and let the frontend progress against a stable API.
