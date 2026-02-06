"""
ABS MHSI Data Fetcher and Processor
Fetches Monthly Household Spending Indicator data and calculates per-household estimates.
"""

import pandas as pd
import requests
import json
from datetime import datetime
from typing import Optional, Dict, List

# Configuration
API_URL = "https://data.api.abs.gov.au/rest/data/ABS,HSI_M,1.6.0/7+8+9.2.10.AUS.M?startPeriod=2024-01&dimensionAtObservation=AllDimensions"

HOUSEHOLDS = {
    2023: 10_600_000,
    2024: 10_800_000,
    2025: 11_000_000,
}

# Manual data fallback
MANUAL_DATA = {
    'month': [
        '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
        '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
        '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
        '2025-07', '2025-08', '2025-09', '2025-10', '2025-11'
    ],
    'food_aud_m_sa': [
        11127.9, 11134.6, 11109.6, 11105.4, 11181.1, 11167.1,
        11225.8, 11293.2, 11333.0, 11375.7, 11471.5, 11444.5,
        11527.0, 11641.4, 11842.0, 11820.3, 11839.4, 11993.4,
        11981.1, 12003.9, 12075.6, 12205.9, 12292.4
    ]
}


def fetch_abs_data(url: str = API_URL) -> Optional[Dict]:
    """Fetch SDMX-JSON data from ABS API."""
    headers = {
        'Accept': 'application/vnd.sdmx.data+json;version=2.0.0',
        'Accept-Encoding': 'gzip, deflate',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching ABS data: {e}")
        return None


def parse_sdmx_data(sdmx_json: Dict) -> Optional[pd.DataFrame]:
    """Parse SDMX-JSON 2.0 format and extract observations."""
    if not sdmx_json or 'data' not in sdmx_json:
        return None
    
    try:
        structure = sdmx_json['data'].get('structure', {})
        dimensions = structure.get('dimensions', {}).get('observation', [])
        
        # Find TIME_PERIOD dimension
        time_idx = None
        for i, dim in enumerate(dimensions):
            if 'TIME' in dim.get('id', '').upper():
                time_idx = i
                break
        
        if time_idx is None:
            return None
        
        # Extract observations
        datasets = sdmx_json['data'].get('dataSets', [])
        if not datasets:
            return None
        
        observations = datasets[0].get('observations', {})
        if not observations:
            return None
        
        # Parse observations
        records = []
        for obs_key, obs_value in observations.items():
            key_parts = obs_key.split(':')
            
            # Get time period
            time_period = None
            if time_idx < len(key_parts):
                time_code = key_parts[time_idx]
                for dim in dimensions:
                    if 'TIME' in dim.get('id', '').upper():
                        values = dim.get('values', [])
                        if int(time_code) < len(values):
                            time_period = values[int(time_code)].get('id')
                        break
            
            # Get value
            value = obs_value[0] if isinstance(obs_value, list) else obs_value
            
            if time_period and value is not None:
                records.append({
                    'month': time_period,
                    'food_aud_m_sa': float(value)
                })
        
        if not records:
            return None
        
        df = pd.DataFrame(records)
        return df.sort_values('month').reset_index(drop=True)
        
    except Exception as e:
        print(f"Error parsing SDMX data: {e}")
        return None


def load_manual_data() -> pd.DataFrame:
    """Load manual data as fallback."""
    return pd.DataFrame(MANUAL_DATA)


def get_household_count(month_str: str) -> int:
    """Get household count for a given month using annual step function."""
    year = int(month_str[:4])
    return HOUSEHOLDS.get(year, 11_000_000)  # Default to 2025 if unknown


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process food spending data and calculate per-household values."""
    df = df.copy()
    
    # Add household counts
    df['households'] = df['month'].apply(get_household_count)
    
    # Convert to AUD$ and calculate per-household
    df['food_aud_sa'] = df['food_aud_m_sa'] * 1_000_000
    df['food_per_household_month'] = (
        df['food_aud_sa'] / df['households']
    ).round(2)
    
    # 12-month rolling average
    df = df.sort_values('month').reset_index(drop=True)
    df['food_per_hh_12m_avg'] = (
        df['food_per_household_month']
        .rolling(window=12, min_periods=1)
        .mean()
        .round(2)
    )
    
    return df


def get_spending_data(use_api: bool = True) -> pd.DataFrame:
    """
    Main function to get processed spending data.
    Tries API first, falls back to manual data.
    """
    df = None
    data_source = "manual"
    
    if use_api:
        sdmx_data = fetch_abs_data()
        if sdmx_data:
            df = parse_sdmx_data(sdmx_data)
            if df is not None:
                data_source = "api"
    
    if df is None:
        df = load_manual_data()
    
    df = process_data(df)
    df['data_source'] = data_source
    
    return df


def get_summary_stats(df: pd.DataFrame) -> Dict:
    """Calculate summary statistics for the dashboard."""
    latest = df.iloc[-1]
    
    # Year-to-date 2025
    df_2025 = df[df['month'].str.startswith('2025')]
    avg_2025 = df_2025['food_per_household_month'].mean() if not df_2025.empty else None
    
    # Last 12 months
    avg_12m = df.tail(12)['food_per_household_month'].mean() if len(df) >= 12 else None
    
    # Year-over-year growth
    yoy_growth = None
    if len(df) >= 12:
        current = latest['food_per_household_month']
        previous = df.iloc[-12]['food_per_household_month']
        yoy_growth = ((current / previous) - 1) * 100
    
    return {
        'latest_month': latest['month'],
        'latest_value': latest['food_per_household_month'],
        'latest_national': latest['food_aud_m_sa'],
        'households': int(latest['households']),
        'rolling_12m': avg_12m,
        'ytd_2025': avg_2025,
        'yoy_growth': yoy_growth,
        'data_source': latest.get('data_source', 'unknown'),
        'total_months': len(df)
    }


def get_chart_data(df: pd.DataFrame, months: int = 24) -> Dict:
    """Prepare data for Chart.js visualization."""
    df_recent = df.tail(months)
    
    return {
        'labels': df_recent['month'].tolist(),
        'values': df_recent['food_per_household_month'].tolist(),
        'rolling_avg': df_recent['food_per_hh_12m_avg'].tolist(),
        'national_spending': df_recent['food_aud_m_sa'].tolist()
    }


if __name__ == "__main__":
    # Test the data fetcher
    print("Testing data fetcher...")
    df = get_spending_data(use_api=True)
    print(f"\nLoaded {len(df)} months of data")
    print(f"Latest: {df.iloc[-1]['month']} - ${df.iloc[-1]['food_per_household_month']:.2f}")
    
    stats = get_summary_stats(df)
    print(f"\nSummary stats:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
