# Tech Benchmark Hub

A comprehensive web application for comparing CPU and GPU performance data to help make informed hardware purchasing decisions. This project aggregates benchmark data from trusted sources like GamersNexus to provide easy-to-use comparison tools and interactive charts.

## Purpose

Tech Benchmark Hub aims to simplify hardware comparison for:

- PC builders researching components
- Tech enthusiasts comparing performance data
- Anyone looking to make data-driven hardware purchases

## Features

### Current Features

- **CPU Comparison**: Compare processor performance across multiple benchmarks
- **GPU Comparison**: Compare graphics card performance with detailed metrics
- **CPU + GPU Combo Analysis**: Analyze combined system performance
- **Interactive Charts**: Visual representation of benchmark data
- **Multi-Resolution Gaming Benchmarks**: Performance data at 1080p, 1440p, and 4K
- **Productivity Benchmarks**: Professional workload performance metrics

### Planned Features

- Cost-to-performance rankings
- Real-time hardware pricing integration
- Additional benchmark data sources
- Advanced filtering and sorting options

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas, NumPy
- **Charts**: Interactive visualization libraries

## Data Sources

Currently sourcing high-quality benchmark data from:

- **GamersNexus**: Professional hardware reviews and testing

_Note: This is an independent project. We're working toward potential collaboration with data sources to make this platform freely available to everyone._

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/stemcreations/techBenchmarkHub.git
   cd techBenchmarkHub
   ```

2. **Install dependencies**

   ```bash
   pip install -r req.txt
   ```

3. **Initialize the database**

   ```python
   python -c "from models import create_tables; create_tables()"
   ```

4. **Import benchmark data (optional)**

   ```python
   python import_data.py
   ```

5. **Run the application**

   ```bash
   python app.py
   ```

6. **Visit the application**
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
techBenchmarkHub/
├── app.py                 # Main Flask application
├── models.py             # Database models and configuration
├── csv_importer.py       # Data import utilities
├── import_data.py        # Data import scripts
├── req.txt              # Python dependencies
├── templates/           # HTML templates
│   ├── index.html       # Main dashboard
│   ├── cpu_comparison.html
│   ├── gpu_comparison.html
│   └── ...
├── static/             # CSS, JS, and static assets
├── instance/           # Database files
├── cpuBench/          # CPU benchmark data
└── gpuBench/          # GPU benchmark data
```

## Database Schema

### Products

- CPU and GPU information
- Core counts and specifications
- Unique product identification

### Benchmark Categories

- Test types (productivity, gaming)
- Resolution specifications
- Measurement units (fps, scores, time)

### Benchmark Results

- Performance scores
- 1% low fps data (for gaming)
- Test dates and metadata

## Contributing

We welcome contributions! This is our first open-source project, and we're learning as we go.

### Ways to Contribute

- Add new benchmark data sources
- Improve the user interface
- Enhance data visualization
- Fix bugs and improve performance
- Suggest new features

### Getting Started with Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Guidelines

- Write clean, commented code
- Test your changes before submitting
- Follow Python PEP 8 style guidelines
- Update documentation as needed

## Deployment

This application is designed to be deployed on cloud platforms like:

- Digital Ocean
- Heroku
- Railway
- AWS/Azure/GCP

For production deployment:

1. Ensure SQLite database is included
2. Configure environment variables as needed
3. Deploy using your preferred platform

## API Endpoints

- `GET /` - Main dashboard
- `GET /cpu-comparison` - CPU comparison page
- `GET /gpu-comparison` - GPU comparison page
- `GET /cpu-gpu-combo` - Combined analysis page
- `GET /api/stats` - Database statistics
- Various data endpoints for charts and comparisons

## Data Import

The project includes utilities to import benchmark data from CSV files:

```python
from csv_importer import import_csv

# Import CPU benchmark
import_csv('path/to/cpu_data.csv', 'Benchmark Name', unit_type='fps', resolution='1080p')

# Import GPU benchmark
import_csv('path/to/gpu_data.csv', 'Game Title', unit_type='fps', resolution='1440p')
```

## Roadmap

- [ ] Integration with hardware pricing APIs
- [ ] Cost-to-performance analysis tools
- [ ] Additional benchmark data sources
- [ ] Mobile-responsive design improvements
- [ ] Real-time data updates

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **GamersNexus** for providing high-quality benchmark data
- The open-source community for tools and libraries
- Contributors who help improve this project

## Disclaimer

This is an independent project not affiliated with hardware manufacturers or review sites. Benchmark data is sourced from publicly available reviews and testing. Always verify hardware specifications and performance claims before making purchase decisions.

## Support

Having issues or questions?

- Open an [Issue](https://github.com/stemcreations/techBenchmarkHub/issues)
- Check existing issues for solutions
- Review the documentation

---

**Made for the PC building community**
