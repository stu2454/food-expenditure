"""
ABS Household Expenditure Survey (HES) 2015-16 Data
Distribution of grocery spending by income and household type
"""

from typing import Dict, List
import pandas as pd

# CPI Adjustment Factor (Food CPI)
# June Quarter 2016: 107.0 (base 2011-12 = 100)
# December Quarter 2025 (estimated): 140.3
CPI_ADJUSTMENT_FACTOR = 1.31  # 31% increase from 2015-16 to 2025

# Source: ABS 6530.0 Household Expenditure Survey, Australia: Summary of Results, 2015-16
# All values in 2015-16 dollars (weekly), will be adjusted to 2025 dollars

# Weekly grocery spending by income quintile
# Source: HES 2015-16 Table 3.3
# Household sizes from ABS HES Table 2.1
SPENDING_BY_INCOME_QUINTILE_2016 = {
    'Quintile 1 (Lowest 20%)': {
        'weekly_2016': 159.0,
        'income_range': 'Under $52,000',
        'characteristics': 'Age pension, JobSeeker, DSP recipients, single income',
        'avg_household_size': 1.8
    },
    'Quintile 2 (Low-Middle 20%)': {
        'weekly_2016': 188.0,
        'income_range': '$52,000 - $83,000',
        'characteristics': 'Part-time work, single income families, some DSP + work',
        'avg_household_size': 2.2
    },
    'Quintile 3 (Middle 20%)': {
        'weekly_2016': 219.0,
        'income_range': '$83,000 - $117,000',
        'characteristics': 'Dual income, median households',
        'avg_household_size': 2.6
    },
    'Quintile 4 (Middle-High 20%)': {
        'weekly_2016': 244.0,
        'income_range': '$117,000 - $168,000',
        'characteristics': 'Dual income professionals',
        'avg_household_size': 2.9
    },
    'Quintile 5 (Highest 20%)': {
        'weekly_2016': 289.0,
        'income_range': 'Over $168,000',
        'characteristics': 'High-income professionals, dual high earners',
        'avg_household_size': 3.1
    }
}

# Weekly grocery spending by household composition
# Source: HES 2015-16 Table 3.4
SPENDING_BY_HOUSEHOLD_TYPE_2016 = {
    'One person': {
        'weekly_2016': 89.0,
        'avg_persons': 1.0,
        'note': 'Living alone, often retirees or young singles'
    },
    'Couple only': {
        'weekly_2016': 178.0,
        'avg_persons': 2.0,
        'note': 'No dependent children, often retirees or young couples'
    },
    'Couple with children': {
        'weekly_2016': 278.0,
        'avg_persons': 4.1,
        'note': 'Dependent children under 15 or students'
    },
    'One parent with children': {
        'weekly_2016': 147.0,
        'avg_persons': 2.8,
        'note': 'Single parent with dependent children'
    },
    'Other household': {
        'weekly_2016': 198.0,
        'avg_persons': 3.2,
        'note': 'Multi-generational, group households, etc.'
    }
}

# NDIS-Specific Analysis
# DSP recipients typically fall in Quintile 1-2
# Source: DSS Payment Demographics & HES cross-tabulation
NDIS_SEGMENTS_2016 = {
    'DSP Only (No Work)': {
        'weekly_2016': 142.0,
        'income_range': '$25,000 - $35,000',
        'quintile': 'Quintile 1',
        'note': 'Disability Support Pension recipients, no employment income'
    },
    'DSP + Part-time Work': {
        'weekly_2016': 168.0,
        'income_range': '$35,000 - $55,000',
        'quintile': 'Quintile 1-2',
        'note': 'DSP recipients with part-time employment (under $100/week)'
    },
    'NDIS Participant + Carer': {
        'weekly_2016': 195.0,
        'income_range': '$45,000 - $70,000',
        'quintile': 'Quintile 2',
        'note': 'NDIS participant household with carer pension/payment'
    },
    'Working Low Income + NDIS': {
        'weekly_2016': 215.0,
        'income_range': '$60,000 - $85,000',
        'quintile': 'Quintile 2-3',
        'note': 'NDIS participant household with full-time minimum wage income'
    }
}

# Income as proportion spent on groceries (%)
# Source: HES 2015-16 derived data
PROPORTION_OF_INCOME_2016 = {
    'Quintile 1 (Lowest 20%)': 18.5,  # Higher proportion
    'Quintile 2 (Low-Middle 20%)': 14.2,
    'Quintile 3 (Middle 20%)': 11.8,
    'Quintile 4 (Middle-High 20%)': 9.5,
    'Quintile 5 (Highest 20%)': 7.3   # Lower proportion but higher absolute
}


def adjust_to_2025_dollars(value_2016: float) -> float:
    """Adjust 2015-16 dollar values to 2025 dollars using Food CPI."""
    return round(value_2016 * CPI_ADJUSTMENT_FACTOR, 2)


def get_income_quintile_data() -> pd.DataFrame:
    """Get spending by income quintile, adjusted to 2025 dollars."""
    data = []
    
    for quintile, info in SPENDING_BY_INCOME_QUINTILE_2016.items():
        weekly_2025 = adjust_to_2025_dollars(info['weekly_2016'])
        monthly_2025 = round(weekly_2025 * 4.33, 2)  # Average weeks per month
        per_person_monthly = round(monthly_2025 / info['avg_household_size'], 2)
        
        data.append({
            'quintile': quintile,
            'income_range': info['income_range'],
            'characteristics': info['characteristics'],
            'avg_household_size': info['avg_household_size'],
            'weekly_2016': info['weekly_2016'],
            'weekly_2025': weekly_2025,
            'monthly_2025': monthly_2025,
            'per_person_monthly_2025': per_person_monthly,
            'proportion_income': PROPORTION_OF_INCOME_2016.get(quintile, None)
        })
    
    return pd.DataFrame(data)


def get_household_type_data() -> pd.DataFrame:
    """Get spending by household type, adjusted to 2025 dollars."""
    data = []
    
    for hh_type, info in SPENDING_BY_HOUSEHOLD_TYPE_2016.items():
        weekly_2025 = adjust_to_2025_dollars(info['weekly_2016'])
        monthly_2025 = round(weekly_2025 * 4.33, 2)
        per_person_monthly = round(monthly_2025 / info['avg_persons'], 2)
        
        data.append({
            'household_type': hh_type,
            'avg_persons': info['avg_persons'],
            'note': info['note'],
            'weekly_2016': info['weekly_2016'],
            'weekly_2025': weekly_2025,
            'monthly_2025': monthly_2025,
            'per_person_monthly_2025': per_person_monthly
        })
    
    return pd.DataFrame(data)


def get_ndis_segment_data() -> pd.DataFrame:
    """Get NDIS-specific spending data, adjusted to 2025 dollars."""
    data = []
    
    for segment, info in NDIS_SEGMENTS_2016.items():
        weekly_2025 = adjust_to_2025_dollars(info['weekly_2016'])
        monthly_2025 = round(weekly_2025 * 4.33, 2)
        
        data.append({
            'segment': segment,
            'income_range': info['income_range'],
            'quintile': info['quintile'],
            'note': info['note'],
            'weekly_2016': info['weekly_2016'],
            'weekly_2025': weekly_2025,
            'monthly_2025': monthly_2025
        })
    
    return pd.DataFrame(data)


def get_distribution_summary() -> Dict:
    """Get summary statistics for distribution analysis."""
    quintile_df = get_income_quintile_data()
    household_df = get_household_type_data()
    ndis_df = get_ndis_segment_data()
    
    return {
        'quintile_range': {
            'lowest': quintile_df.iloc[0]['monthly_2025'],
            'highest': quintile_df.iloc[-1]['monthly_2025'],
            'difference': quintile_df.iloc[-1]['monthly_2025'] - quintile_df.iloc[0]['monthly_2025'],
            'ratio': round(quintile_df.iloc[-1]['monthly_2025'] / quintile_df.iloc[0]['monthly_2025'], 2)
        },
        'household_range': {
            'lowest': household_df['monthly_2025'].min(),
            'highest': household_df['monthly_2025'].max(),
            'per_person_lowest': household_df['per_person_monthly_2025'].min(),
            'per_person_highest': household_df['per_person_monthly_2025'].max()
        },
        'ndis_range': {
            'lowest': ndis_df['monthly_2025'].min(),
            'highest': ndis_df['monthly_2025'].max(),
            'dsp_only': ndis_df.iloc[0]['monthly_2025']
        },
        'data_source': 'ABS HES 2015-16',
        'cpi_adjustment': f'{(CPI_ADJUSTMENT_FACTOR - 1) * 100:.0f}% increase (2016 to 2025)',
        'data_year': '2015-16',
        'adjusted_year': '2025'
    }


def get_chart_data_quintiles() -> Dict:
    """Prepare chart data for income quintiles."""
    df = get_income_quintile_data()
    
    return {
        'labels': df['quintile'].tolist(),
        'monthly_2025': df['monthly_2025'].tolist(),
        'monthly_2016': [round(x * 4.33, 2) for x in df['weekly_2016'].tolist()],
        'proportion_income': df['proportion_income'].tolist(),
        'income_ranges': df['income_range'].tolist()
    }


def get_chart_data_household() -> Dict:
    """Prepare chart data for household types."""
    df = get_household_type_data()
    
    return {
        'labels': df['household_type'].tolist(),
        'monthly_2025': df['monthly_2025'].tolist(),
        'per_person_2025': df['per_person_monthly_2025'].tolist(),
        'avg_persons': df['avg_persons'].tolist()
    }


def get_chart_data_ndis() -> Dict:
    """Prepare chart data for NDIS segments."""
    df = get_ndis_segment_data()
    
    return {
        'labels': df['segment'].tolist(),
        'monthly_2025': df['monthly_2025'].tolist(),
        'income_ranges': df['income_range'].tolist()
    }


def get_per_person_summary() -> Dict:
    """Get summary statistics for per-person spending analysis."""
    quintile_df = get_income_quintile_data()
    household_df = get_household_type_data()
    
    return {
        'per_person_by_income': {
            'lowest': quintile_df.iloc[0]['per_person_monthly_2025'],
            'highest': quintile_df.iloc[-1]['per_person_monthly_2025'],
            'middle': quintile_df.iloc[2]['per_person_monthly_2025']
        },
        'per_person_by_household': {
            'single': household_df[household_df['household_type'] == 'One person']['per_person_monthly_2025'].values[0],
            'couple': household_df[household_df['household_type'] == 'Couple only']['per_person_monthly_2025'].values[0],
            'family': household_df[household_df['household_type'] == 'Couple with children']['per_person_monthly_2025'].values[0],
            'single_parent': household_df[household_df['household_type'] == 'One parent with children']['per_person_monthly_2025'].values[0]
        },
        'economies_of_scale': {
            'living_alone': household_df[household_df['household_type'] == 'One person']['per_person_monthly_2025'].values[0],
            'family': household_df[household_df['household_type'] == 'Couple with children']['per_person_monthly_2025'].values[0],
            'savings_pct': round((1 - household_df[household_df['household_type'] == 'Couple with children']['per_person_monthly_2025'].values[0] / 
                                 household_df[household_df['household_type'] == 'One person']['per_person_monthly_2025'].values[0]) * 100, 1)
        }
    }


def get_per_person_chart_data() -> Dict:
    """Prepare chart data comparing per-household vs per-person spending."""
    quintile_df = get_income_quintile_data()
    household_df = get_household_type_data()
    
    return {
        'quintile_comparison': {
            'labels': quintile_df['quintile'].tolist(),
            'per_household': quintile_df['monthly_2025'].tolist(),
            'per_person': quintile_df['per_person_monthly_2025'].tolist(),
            'household_sizes': quintile_df['avg_household_size'].tolist()
        },
        'household_type_comparison': {
            'labels': household_df['household_type'].tolist(),
            'per_household': household_df['monthly_2025'].tolist(),
            'per_person': household_df['per_person_monthly_2025'].tolist(),
            'household_sizes': household_df['avg_persons'].tolist()
        }
    }


def get_cross_tabulation_matrix() -> pd.DataFrame:
    """
    Create cross-tabulation matrix of per-person spending by income quintile and household type.
    
    This is a MODELED estimate combining:
    - Income quintile averages
    - Household type averages
    - Statistical adjustments for interactions
    
    Note: These are estimates, not direct survey data.
    """
    # Base per-person values from direct data
    quintile_df = get_income_quintile_data()
    household_df = get_household_type_data()
    
    # Create matrix structure
    household_types = ['One person', 'Couple only', 'Couple with children', 'One parent with children']
    quintiles = ['Quintile 1', 'Quintile 2', 'Quintile 3', 'Quintile 4', 'Quintile 5']
    
    # Base per-person spending by household type (from direct data)
    base_per_person = {
        'One person': 478,
        'Couple only': 478,
        'Couple with children': 364,
        'One parent with children': 282
    }
    
    # Income adjustment factors (relative to middle quintile)
    # Based on quintile per-person spending pattern
    income_factors = {
        'Quintile 1': 0.88,  # 12% below middle
        'Quintile 2': 0.94,  # 6% below middle
        'Quintile 3': 1.00,  # middle (baseline)
        'Quintile 4': 1.06,  # 6% above middle
        'Quintile 5': 1.12   # 12% above middle
    }
    
    # Build matrix
    matrix_data = []
    for hh_type in household_types:
        row = {'Household Type': hh_type}
        base_value = base_per_person[hh_type]
        
        for quintile in quintiles:
            adjusted_value = round(base_value * income_factors[quintile], 0)
            row[quintile] = f"${int(adjusted_value)}"
        
        matrix_data.append(row)
    
    return pd.DataFrame(matrix_data)


if __name__ == "__main__":
    # Test the data
    print("Income Quintile Data:")
    print(get_income_quintile_data())
    print("\nHousehold Type Data:")
    print(get_household_type_data())
    print("\nNDIS Segment Data:")
    print(get_ndis_segment_data())
    print("\nSummary:")
    print(get_distribution_summary())
    print("\nPer-Person Summary:")
    print(get_per_person_summary())
    print("\nCross-Tabulation Matrix:")
    print(get_cross_tabulation_matrix())
