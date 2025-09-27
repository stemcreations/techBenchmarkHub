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

The project includes utilities to import benchmark data from CSV files. Your CSV files must follow specific formats:

### CPU Benchmark CSV Format

```csv
CPU_Model,Core_Count,Date,Score
AMD R9 9950X Lexar 6000,(16C/32T),[8/24],204872
Intel i9-14900K,(8P/16E/32T),[7/24],187566
AMD R7 9700X,(8C/16T),[8/24],156420
```

**Required Columns:**

- `CPU_Model`: Full CPU name (extras like "Lexar 6000" will be cleaned)
- `Core_Count`: Core configuration (e.g., "(8C/16T)" or "(8P/16E/32T)")
- `Date`: Test date in format `[M/YY]` (e.g., `[8/24]`)
- `Score`: Numerical performance score

### GPU Benchmark CSV Format

```csv
GPU_Model,Date,AVG_FPS,1%_Low
RTX 4090,(7/24),145.2,118.7
RTX 4080,(7/24),128.4,105.1
RTX 4070 Ti,(7/24),112.8,92.3
```

**Required Columns:**

- `GPU_Model`: Full GPU name
- `Date`: Test date in format `[M/YY]` (e.g., `[7/24]`)
- `AVG_FPS`: Average frames per second
- `1%_Low`: 1% low FPS value

### Import Examples

````python
from csv_importer import import_csv

# Import CPU productivity benchmark (no resolution)
import_csv('7zip_compression.csv', 'Adobe Photoshop Puget Suite', unit_type='score')

# Import CPU gaming benchmark (with resolution)
import_csv('starfield_cpu_1080p.csv', 'Starfield CPU Performance', unit_type='fps', resolution='1080p')

# Import GPU gaming benchmark (with resolution)
import_csv('starfield_gpu_1440p.csv', 'Starfield GPU Ultra', unit_type='fps', resolution='1440p')
```## Roadmap

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
````
