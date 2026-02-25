"""
Household Spending Estimates - Flask Application
Australian household grocery spending estimates from ABS MHSI data
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import pandas as pd
from data_fetcher import get_spending_data, get_summary_stats, get_chart_data
from hes_data import (
    get_income_quintile_data, 
    get_household_type_data, 
    get_ndis_segment_data,
    get_distribution_summary,
    get_chart_data_quintiles,
    get_chart_data_household,
    get_chart_data_ndis,
    get_per_person_summary,
    get_per_person_chart_data,
    get_cross_tabulation_matrix
)

app = Flask(__name__)

# Cache for data (refresh on app restart)
_data_cache = None
_cache_time = None


def get_data(force_refresh=False):
    """Get spending data with simple caching."""
    global _data_cache, _cache_time
    
    if _data_cache is None or force_refresh:
        _data_cache = get_spending_data(use_api=True)
        _cache_time = datetime.now()
    
    return _data_cache


@app.route('/')
def index():
    """Dashboard homepage."""
    df = get_data()
    stats = get_summary_stats(df)
    
    return render_template('index.html', 
                         stats=stats,
                         last_updated=_cache_time.strftime('%Y-%m-%d %H:%M:%S') if _cache_time else 'Unknown')


@app.route('/methodology')
def methodology():
    """Methodology explanation page."""
    return render_template('methodology.html')


@app.route('/data')
def data_table():
    """Full data table page."""
    df = get_data()
    
    # Prepare table data
    table_data = df[[
        'month', 
        'food_aud_m_sa', 
        'households', 
        'food_per_household_month',
        'food_per_hh_12m_avg'
    ]].to_dict('records')
    
    return render_template('data.html', 
                         table_data=table_data,
                         total_rows=len(table_data))


@app.route('/distribution')
def distribution():
    """Distribution analysis page - spending by income and household type."""
    summary = get_distribution_summary()
    quintile_data = get_income_quintile_data().to_dict('records')
    household_data = get_household_type_data().to_dict('records')
    ndis_data = get_ndis_segment_data().to_dict('records')
    per_person_summary = get_per_person_summary()
    cross_tab_matrix = get_cross_tabulation_matrix().to_dict('records')
    
    return render_template('distribution.html',
                         summary=summary,
                         quintile_data=quintile_data,
                         household_data=household_data,
                         ndis_data=ndis_data,
                         per_person_summary=per_person_summary,
                         cross_tab_matrix=cross_tab_matrix)


@app.route('/api/chart-data')
def api_chart_data():
    """API endpoint for chart data."""
    df = get_data()
    months = int(request.args.get('months', 24))
    chart_data = get_chart_data(df, months)
    return jsonify(chart_data)


@app.route('/api/summary')
def api_summary():
    """API endpoint for summary statistics."""
    df = get_data()
    stats = get_summary_stats(df)
    return jsonify(stats)


@app.route('/api/refresh')
def api_refresh():
    """API endpoint to force data refresh."""
    df = get_data(force_refresh=True)
    stats = get_summary_stats(df)
    return jsonify({
        'success': True,
        'refreshed_at': _cache_time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_months': len(df),
        'latest_month': stats['latest_month']
    })


@app.route('/api/distribution/quintiles')
def api_distribution_quintiles():
    """API endpoint for income quintile chart data."""
    return jsonify(get_chart_data_quintiles())


@app.route('/api/distribution/household')
def api_distribution_household():
    """API endpoint for household type chart data."""
    return jsonify(get_chart_data_household())


@app.route('/api/distribution/ndis')
def api_distribution_ndis():
    """API endpoint for NDIS segment chart data."""
    return jsonify(get_chart_data_ndis())


@app.route('/api/distribution/per-person')
def api_distribution_per_person():
    """API endpoint for per-person comparison chart data."""
    return jsonify(get_per_person_chart_data())


@app.route('/api/distribution/per-person-summary')
def api_per_person_summary():
    """API endpoint for per-person summary statistics."""
    return jsonify(get_per_person_summary())


@app.template_filter('format_currency')
def format_currency(value):
    """Format value as currency."""
    if value is None:
        return 'N/A'
    return f"${value:,.2f}"


@app.template_filter('format_number')
def format_number(value):
    """Format value as number with commas."""
    if value is None:
        return 'N/A'
    return f"{int(value):,}"


@app.template_filter('format_percent')
def format_percent(value):
    """Format value as percentage."""
    if value is None:
        return 'N/A'
    return f"{value:+.1f}%"


if __name__ == '__main__':
    # For local development
    app.run(debug=True, host='0.0.0.0', port=5002)
