# Household Spending Estimates

A Flask web application that calculates and displays monthly household grocery spending estimates in Australia using ABS Monthly Household Spending Indicator (MHSI) data.

## Overview

This application provides:
- **Dashboard**: Key metrics and interactive charts showing spending trends
- **Methodology**: Detailed explanation of calculation steps and data sources
- **Data**: Full dataset table with export capabilities

## Features

- 📊 Interactive charts with Chart.js
- 📱 Responsive Bootstrap 5 design
- 🔄 Automatic data fetching from ABS API with manual fallback
- 📈 12-month rolling averages for trend analysis
- 💾 CSV export and clipboard copy functionality
- 🐳 Docker containerization
- ☁️ Ready for Render deployment

## Technology Stack

- **Backend**: Flask 3.0
- **Data Processing**: Pandas
- **Frontend**: Bootstrap 5, Chart.js
- **Deployment**: Docker, Gunicorn
- **Hosting**: Render (or any Docker-compatible platform)

## Local Development Setup

### Prerequisites

- Python 3.11+
- pip
- (Optional) Docker Desktop for containerized development

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/household-spending-app.git
   cd household-spending-app
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open in browser**:
   Navigate to `http://localhost:5000`

## Docker Development

### Build and run with Docker:

```bash
# Build the image
docker build -t household-spending-app .

# Run the container
docker run -p 10000:10000 household-spending-app
```

Navigate to `http://localhost:10000`

## Deployment to Render

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/household-spending-app.git
   git push -u origin main
   ```

2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml` and configure the service

3. **Deploy**:
   - Click "Apply" to deploy
   - Render will build and deploy your Docker container
   - Your app will be live at: `https://household-spending-estimates.onrender.com`

### Method 2: Manual Render Configuration

1. **Create a new Web Service** on Render:
   - Environment: Docker
   - Branch: main
   - Region: Choose your preferred region

2. **Configure**:
   - Build Command: (leave empty, Docker handles this)
   - Start Command: (leave empty, Docker handles this)
   - Health Check Path: `/`

3. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete

## Project Structure

```
household-spending-app/
│
├── app.py                  # Flask application
├── data_fetcher.py         # ABS API integration and data processing
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker configuration
├── render.yaml            # Render deployment configuration
│
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Dashboard page
│   ├── methodology.html   # Methodology explanation
│   └── data.html          # Data table page
│
├── static/
│   └── css/
│       └── style.css      # Custom styles
│
└── data/                  # (Optional) Local data storage
```

## Configuration

### Updating Household Projections

Edit `data_fetcher.py` to update household counts:

```python
HOUSEHOLDS = {
    2023: 10_600_000,
    2024: 10_800_000,
    2025: 11_000_000,
    2026: 11_200_000,  # Add new years as needed
}
```

### Updating Manual Data Fallback

If the ABS API is unavailable, the app uses manual data. Update this in `data_fetcher.py`:

```python
MANUAL_DATA = {
    'month': ['2024-01', '2024-02', ...],
    'food_aud_m_sa': [11127.9, 11134.6, ...]
}
```

## Data Sources

- **Primary**: ABS Monthly Household Spending Indicator (MHSI) - Catalogue 5682.0
- **Household Counts**: ABS Household and Family Projections - Catalogue 3236.0

## API Endpoints

The application includes REST API endpoints:

- `GET /api/chart-data?months=24` - Chart data for visualization
- `GET /api/summary` - Summary statistics
- `GET /api/refresh` - Force data refresh

## Maintenance

### Monthly Updates

To update with latest ABS data:

1. Check for new MHSI releases (typically 6-8 weeks after reference month)
2. Visit [ABS Data Explorer](https://dataexplorer.abs.gov.au)
3. Update `MANUAL_DATA` in `data_fetcher.py` with new values
4. Commit and push changes
5. Render will automatically redeploy

### Annual Updates

Update household projections when new ABS projections are released (typically annually).

## Troubleshooting

### API Connection Issues

If the ABS API is unavailable:
- App automatically falls back to manual data
- Check logs for API errors
- Verify network connectivity to `data.api.abs.gov.au`

### Docker Build Issues

```bash
# Clear Docker cache and rebuild
docker system prune -a
docker build --no-cache -t household-spending-app .
```

### Render Deployment Issues

- Check Render logs in the dashboard
- Verify all files are committed to Git
- Ensure `Dockerfile` and `requirements.txt` are present
- Check that PORT environment variable is set correctly

## Development Workflow

### Using VS Code

1. **Install recommended extensions**:
   - Python
   - Docker
   - GitHub Pull Requests

2. **Open terminal** in VS Code (`Ctrl+` ` or Cmd+` `)

3. **Run with hot reload**:
   ```bash
   export FLASK_DEBUG=1  # On Windows: set FLASK_DEBUG=1
   python app.py
   ```

4. **Test Docker build locally** before deploying:
   ```bash
   docker build -t test-app .
   docker run -p 10000:10000 test-app
   ```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is developed for internal use by the National Disability Insurance Agency (NDIA).

## Contact

For questions or issues, contact the NDIA Assistive Technology Markets team.

## Acknowledgments

- Australian Bureau of Statistics for providing MHSI data
- Bootstrap and Chart.js for UI components
