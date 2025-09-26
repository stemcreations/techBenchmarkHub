# import_data.py
# Script to import CSV benchmark data into the database
from csv_importer import import_csv, main
from models import create_tables

def import_benchmark_data():
    """
    Import benchmark data from CSV files
    Configure your CSV files here before running
    """
    
    # Create database tables first
    create_tables()
    
    # Import your CSV files - configure these paths to match your actual CSV files
    csv_files = [
        # CPU productivity benchmarks (no resolution)
        {
            'file': 'cpuBench/photoshop_puget_suite.csv',  # Update path as needed
            'name': 'Adobe Photoshop Puget Suite',
            'description': 'Adobe Photoshop performance using Puget Systems benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/blender_render_csv.txt',  # This file exists in your cpuBench folder
            'name': 'Blender Render Time',
            'description': 'Blender rendering performance benchmark',
            'unit': 'seconds',
            'resolution': None
        },
        {
            'file': 'cpuBench/7zip_compression_csv.txt',
            'name': '7-Zip Compression',
            'description': '7-Zip compression benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/7zip_decompression_csv.txt',
            'name': '7-Zip Decompression',
            'description': '7-Zip decompression benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/chromium_compile_csv.txt',
            'name': 'Chromium Compile',
            'description': 'Chromium code compilation benchmark',
            'unit': 'seconds',
            'resolution': None
        },
        
        # CPU gaming benchmarks (with resolution)
        {
            'file': 'cpuBench/baldurs_gate_3_1080p_cpu.txt',
            'name': "Baldur's Gate 3 CPU Performance",
            'description': "Baldur's Gate 3 CPU gaming performance",
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/dragons_dogma_2_1080p_cpu.txt',
            'name': "Dragon's Dogma 2 CPU Performance",
            'description': "Dragon's Dogma 2 CPU gaming performance",
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/f1_24_1080p_cpu.txt',
            'name': 'F1 24 CPU Performance',
            'description': 'F1 24 CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/f1_24_1440p_cpu.txt',
            'name': 'F1 24 CPU Performance',
            'description': 'F1 24 CPU gaming performance',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'cpuBench/ffxiv_dawntrail_1080p_cpu.txt',
            'name': 'FFXIV Dawntrail CPU Performance',
            'description': 'Final Fantasy XIV Dawntrail CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/ffxiv_dawntrail_1440p_cpu.txt',
            'name': 'FFXIV Dawntrail CPU Performance',
            'description': 'Final Fantasy XIV Dawntrail CPU gaming performance',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'cpuBench/ffxiv_dawntrail_1440p_extended_cpu.txt',
            'name': 'FFXIV Dawntrail Extended CPU Performance',
            'description': 'Final Fantasy XIV Dawntrail extended CPU gaming performance',
            'unit': 'fps',
            'resolution': '1440p'
        },
        
        # Add GPU benchmark files from gpuBench folder when available
        # {
        #     'file': 'gpuBench/starfield_gpu_1080p_ultra.csv',
        #     'name': 'Starfield GPU Ultra',
        #     'description': 'Starfield GPU performance at Ultra settings',
        #     'unit': 'fps',
        #     'resolution': '1080p'
        # },
    ]
    
    print("Starting benchmark data import...")
    print(f"Found {len(csv_files)} CSV files to import")
    
    successful_imports = 0
    failed_imports = 0
    
    for csv_info in csv_files:
        print(f"\n{'='*50}")
        print(f"Importing: {csv_info['file']}")
        print(f"Benchmark: {csv_info['name']}")
        if csv_info.get('resolution'):
            print(f"Resolution: {csv_info['resolution']}")
        print('='*50)
        
        try:
            success = import_csv(
                csv_info['file'],
                csv_info['name'],
                csv_info['description'],
                csv_info['unit'],
                csv_info.get('resolution')
            )
            if success:
                successful_imports += 1
                print(f"✅ Successfully imported {csv_info['file']}")
            else:
                failed_imports += 1
                print(f"❌ Failed to import {csv_info['file']}")
        except Exception as e:
            failed_imports += 1
            print(f"❌ Error importing {csv_info['file']}: {str(e)}")
    
    print(f"\n{'='*50}")
    print("IMPORT SUMMARY")
    print(f"{'='*50}")
    print(f"Total files: {len(csv_files)}")
    print(f"Successful imports: {successful_imports}")
    print(f"Failed imports: {failed_imports}")
    print(f"{'='*50}")

if __name__ == '__main__':
    import_benchmark_data()