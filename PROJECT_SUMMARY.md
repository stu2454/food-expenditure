# Household Spending Estimates Web App - Project Summary

## 🎯 Project Overview

A professional Flask web application that calculates and displays monthly household grocery spending estimates in Australia using ABS Monthly Household Spending Indicator (MHSI) data. Built for deployment to Render.com with Docker containerization.

## ✨ Key Features

### Dashboard Page
- Interactive Chart.js visualizations
- Key metrics cards (latest month, 12-month average, YoY growth, household count)
- Time period selection (12 months, 24 months, all data)
- Data source status indicator
- Responsive Bootstrap 5 design

### Methodology Page
- Complete step-by-step calculation explanation
- Data source documentation
- Interpretation guidelines and limitations
- Validation and sanity checks
- Alternative approaches discussion
- Professional formatting for policy communication

### Data Page
- Full dataset table with all calculated values
- Search/filter functionality
- Export to CSV
- Copy to clipboard
- Column definitions

## 📁 Project Structure

```
household-spending-app/
├── app.py                   # Flask application with routes
├── data_fetcher.py          # ABS API integration & calculations
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── render.yaml             # Render deployment config
├── README.md               # Main documentation
├── DEPLOYMENT.md           # Step-by-step deployment guide
├── start.sh                # Quick start script (Mac/Linux)
├── start.bat               # Quick start script (Windows)
├── .gitignore              # Git ignore rules
├── .dockerignore           # Docker ignore rules
│
├── templates/
│   ├── base.html           # Base template with navigation
│   ├── index.html          # Dashboard page
│   ├── methodology.html    # Methodology explanation
│   └── data.html           # Data table page
│
└── static/
    └── css/
        └── style.css       # Custom styling
```

## 🛠 Technology Stack

- **Backend**: Flask 3.0 (Python web framework)
- **Data Processing**: Pandas 2.1.4
- **HTTP Client**: Requests 2.31.0
- **Production Server**: Gunicorn 21.2.0
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Charts**: Chart.js 4.4
- **Containerization**: Docker
- **Deployment**: Render.com

## 📊 Data Sources

1. **ABS Monthly Household Spending Indicator (MHSI)**
   - Catalogue: 5682.0
   - Category: Food (COICOP 01)
   - Series: Seasonally Adjusted, Level, Current prices
   - Units: AUD$ millions
   - Geography: Australia (national)

2. **ABS Household and Family Projections**
   - Catalogue: 3236.0
   - Series: Series B (middle assumption)
   - Annual counts as at June 30
   - Applied as annual step function

## 🧮 Calculation Methodology

1. Obtain national food spending from ABS MHSI (AUD$ millions)
2. Obtain Australian household count from ABS projections
3. Calculate: Per-household = (National spending × 1,000,000) ÷ Households
4. Calculate 12-month rolling average for trend analysis

**Example (November 2025):**
- National: $12,292.4 million
- Households: 11,000,000
- Per-household: $1,117.49/month

## 🚀 Quick Start

### Local Development
```bash
# Mac/Linux
./start.sh

# Windows
start.bat

# Or manually:
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

### Docker
```bash
docker build -t household-spending-app .
docker run -p 10000:10000 household-spending-app
```

Visit `http://localhost:10000`

## ☁️ Deployment to Render

### Quick Deploy (3 steps)
1. Push code to GitHub
2. Connect repository to Render
3. Render auto-deploys using `render.yaml`

See **DEPLOYMENT.md** for detailed step-by-step instructions.

## 🔄 Monthly Updates

When new ABS data is released:

1. Edit `data_fetcher.py` → `MANUAL_DATA` section
2. Add new month and spending value
3. Commit and push to GitHub
4. Render automatically redeploys

```python
MANUAL_DATA = {
    'month': [..., '2025-12'],
    'food_aud_m_sa': [..., 12345.6]  # Add new value
}
```

## 📋 File Descriptions

### Core Application
- **app.py**: Flask routes, template rendering, API endpoints
- **data_fetcher.py**: ABS API integration, SDMX parsing, calculations

### Templates (Jinja2)
- **base.html**: Navigation, footer, common layout
- **index.html**: Dashboard with metrics and charts
- **methodology.html**: Comprehensive methodology explanation
- **data.html**: Sortable data table with export

### Configuration
- **requirements.txt**: Python package dependencies
- **Dockerfile**: Multi-stage Docker build configuration
- **render.yaml**: Render.com deployment configuration
- **.gitignore**: Git version control exclusions
- **.dockerignore**: Docker build exclusions

### Documentation
- **README.md**: Project overview and setup instructions
- **DEPLOYMENT.md**: Detailed GitHub → Render deployment guide

### Scripts
- **start.sh**: Quick start for Mac/Linux
- **start.bat**: Quick start for Windows

## 🎨 Design Features

### Responsive Layout
- Mobile-first Bootstrap 5 design
- Collapsible navigation on mobile
- Responsive tables and charts
- Touch-friendly controls

### Visual Design
- Primary color: #0d6efd (Bootstrap blue)
- Card-based layout with shadows
- Bootstrap Icons for visual clarity
- Smooth animations and transitions
- Print-friendly styles

### User Experience
- Intuitive navigation
- Loading states
- Error handling with fallback data
- Export capabilities (CSV, clipboard)
- Search/filter functionality

## 🔐 Security & Best Practices

- Non-root Docker user
- No hardcoded secrets
- Environment variable configuration
- Input validation
- CORS headers properly configured
- Production-ready Gunicorn server

## 📈 API Endpoints

- `GET /` - Dashboard
- `GET /methodology` - Methodology page
- `GET /data` - Data table page
- `GET /api/chart-data?months=24` - Chart data JSON
- `GET /api/summary` - Summary statistics JSON
- `GET /api/refresh` - Force data refresh

## 🧪 Testing

The application includes:
- Python syntax validation
- Docker build verification
- Manual testing checklist
- Sanity check validations

## 📝 Interpretation Notes

**What the estimate IS:**
- Aggregate average (national total ÷ household count)
- National accounts methodology
- Seasonally adjusted
- Transparent and automatable

**What the estimate IS NOT:**
- Household survey median
- Representative of individual households
- Measure of spending distribution
- Real-time indicator

## 🎓 Use Cases

- Policy analysis and communication
- Trend monitoring
- Budget planning discussions
- Internal NDIA reporting
- Team briefings

## 💡 Future Enhancements

Potential additions:
- State/territory breakdowns (if data available)
- CPI-adjusted real values
- Comparison with other categories
- Historical data visualization
- Email alerts for new data

## 🤝 Team Collaboration

- GitHub repository for version control
- Render dashboard for deployment monitoring
- VS Code for development
- Team can access via shared Render URL

## 📞 Support

For questions or issues:
1. Check DEPLOYMENT.md troubleshooting section
2. Review Render logs
3. Contact NDIA AT Markets team

## ✅ Deployment Checklist

Before going live:
- [ ] Test locally on your machine
- [ ] Test Docker build
- [ ] Push to GitHub successfully
- [ ] Deploy to Render
- [ ] Verify all pages load correctly
- [ ] Test on mobile device
- [ ] Share URL with team
- [ ] Document monthly update process
- [ ] Set calendar reminder for monthly updates

## 🎉 Success Metrics

After deployment, you'll have:
- ✅ Professional web application
- ✅ Accessible to entire team (URL)
- ✅ Automatic HTTPS security
- ✅ Mobile-friendly interface
- ✅ Clear methodology documentation
- ✅ Easy monthly updates
- ✅ Export capabilities
- ✅ No server maintenance required

## 📚 Additional Resources

- Flask documentation: https://flask.palletsprojects.com/
- Bootstrap 5: https://getbootstrap.com/
- Chart.js: https://www.chartjs.org/
- Render docs: https://render.com/docs
- ABS Data Explorer: https://dataexplorer.abs.gov.au/

---

**Built for NDIA Assistive Technology Markets Team**
**Ready for immediate deployment to Render.com**
