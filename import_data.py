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
            'file': 'cpuBench/photoshop_puget_csv.csv',
            'name': 'Adobe Photoshop Puget Suite',
            'description': 'Adobe Photoshop performance using Puget Systems benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/premiere_puget_csv.csv',
            'name': 'Adobe Premiere Puget Suite',
            'description': 'Adobe Premiere performance using Puget Systems benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/blender_render_csv.csv',
            'name': 'Blender Render Time',
            'description': 'Blender rendering performance benchmark',
            'unit': 'seconds',
            'resolution': None
        },
        {
            'file': 'cpuBench/7zip_compression_csv.csv',
            'name': '7-Zip Compression',
            'description': '7-Zip compression benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/7zip_decompression_csv.csv',
            'name': '7-Zip Decompression',
            'description': '7-Zip decompression benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/chromium_compile_csv.csv',
            'name': 'Chromium Compile',
            'description': 'Chromium code compilation benchmark',
            'unit': 'seconds',
            'resolution': None
        },
        {
            'file': 'cpuBench/specws_financial_services_csv.csv',
            'name': 'SpecWS Financial Services',
            'description': 'SpecWS Financial Services benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/specws_lammps_csv.csv',
            'name': 'SpecWS LAMMPS',
            'description': 'SpecWS LAMMPS benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'cpuBench/specws_rodiniacfd_csv.csv',
            'name': 'SpecWS RodiniaCFD',
            'description': 'SpecWS RodiniaCFD benchmark',
            'unit': 'score',
            'resolution': None
        },
        
        # CPU gaming benchmarks (with resolution)
        {
            'file': 'cpuBench/baldurs_gate_3_1080p_cpu.csv',
            'name': "Baldur's Gate 3 CPU Performance",
            'description': "Baldur's Gate 3 CPU gaming performance",
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/dragons_dogma_2_1080p_cpu.csv',
            'name': "Dragon's Dogma 2 CPU Performance",
            'description': "Dragon's Dogma 2 CPU gaming performance",
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/f1_24_1080p_cpu.csv',
            'name': 'F1 24 CPU Performance',
            'description': 'F1 24 CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/f1_24_1440p_cpu.csv',
            'name': 'F1 24 CPU Performance',
            'description': 'F1 24 CPU gaming performance',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'cpuBench/ffxiv_dawntrail_1080p_cpu.csv',
            'name': 'FFXIV Dawntrail CPU Performance',
            'description': 'Final Fantasy XIV Dawntrail CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/ffxiv_dawntrail_1440p_cpu.csv',
            'name': 'FFXIV Dawntrail CPU Performance',
            'description': 'Final Fantasy XIV Dawntrail CPU gaming performance',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'cpuBench/ffxiv_dawntrail_1440p_extended_cpu.csv',
            'name': 'FFXIV Dawntrail Extended CPU Performance',
            'description': 'Final Fantasy XIV Dawntrail extended CPU gaming performance',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'cpuBench/rainbow_six_siege_1080p_cpu.csv',
            'name': 'Rainbow Six Siege CPU Performance',
            'description': 'Rainbow Six Siege CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/starfield_1080p_low_cpu.csv',
            'name': 'Starfield CPU Performance',
            'description': 'Starfield CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/stellaris_1080p_cpu_extended.csv',
            'name': 'Stellaris CPU Performance',
            'description': 'Stellaris CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'cpuBench/total_war_warhammer_3_1080p_cpu.csv',
            'name': 'Total War Warhammer III CPU Performance',
            'description': 'Total War Warhammer III CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        
        # GPU gaming benchmarks (with resolution and settings)
        {
            'file': 'gpuBench/black_myth_wukong_1080p_high.csv',
            'name': 'Black Myth Wukong High',
            'description': 'Black Myth Wukong GPU performance at High settings',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'gpuBench/black_myth_wukong_1080p_high_rt_fsr.csv',
            'name': 'Black Myth Wukong High RT FSR',
            'description': 'Black Myth Wukong GPU performance with Ray Tracing and FSR',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'gpuBench/black_myth_wukong_1440p_high.csv',
            'name': 'Black Myth Wukong High',
            'description': 'Black Myth Wukong GPU performance at High settings',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'gpuBench/black_myth_wukong_1440p_high_rt_fsr.csv',
            'name': 'Black Myth Wukong High RT FSR',
            'description': 'Black Myth Wukong GPU performance with Ray Tracing and FSR',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'gpuBench/black_myth_wukong_4k_high.csv',
            'name': 'Black Myth Wukong High',
            'description': 'Black Myth Wukong GPU performance at High settings',
            'unit': 'fps',
            'resolution': '4K'
        },
        {
            'file': 'gpuBench/black_myth_wukong_4k_high_rt_fsr.csv',
            'name': 'Black Myth Wukong High RT FSR',
            'description': 'Black Myth Wukong GPU performance with Ray Tracing and FSR',
            'unit': 'fps',
            'resolution': '4K'
        },
        {
            'file': 'gpuBench/cyberpunk_2077_1080p_ultra.csv',
            'name': 'Cyberpunk 2077 Ultra',
            'description': 'Cyberpunk 2077 GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'gpuBench/cyberpunk_2077_1440p_ultra.csv',
            'name': 'Cyberpunk 2077 Ultra',
            'description': 'Cyberpunk 2077 GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'gpuBench/cyberpunk_2077_4k_ultra.csv',
            'name': 'Cyberpunk 2077 Ultra',
            'description': 'Cyberpunk 2077 GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '4K'
        },
        {
            'file': 'gpuBench/dragons_dogma_2_1080p_max.csv',
            'name': "Dragon's Dogma 2 Max",
            'description': "Dragon's Dogma 2 GPU performance at Max settings",
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'gpuBench/dragons_dogma_2_1080p_max_rt.csv',
            'name': "Dragon's Dogma 2 Max RT",
            'description': "Dragon's Dogma 2 GPU performance with Ray Tracing",
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'gpuBench/dragons_dogma_2_1440p_max.csv',
            'name': "Dragon's Dogma 2 Max",
            'description': "Dragon's Dogma 2 GPU performance at Max settings",
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'gpuBench/dragons_dogma_2_1440p_max_rt.csv',
            'name': "Dragon's Dogma 2 Max RT",
            'description': "Dragon's Dogma 2 GPU performance with Ray Tracing",
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'gpuBench/dragons_dogma_2_4k_max_rt.csv',
            'name': "Dragon's Dogma 2 Max RT",
            'description': "Dragon's Dogma 2 GPU performance with Ray Tracing",
            'unit': 'fps',
            'resolution': '4K'
        },
        {
            'file': 'gpuBench/starfield_1080p_ultra_gpu.csv',
            'name': 'Starfield Ultra',
            'description': 'Starfield GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'gpuBench/starfield_1440p_ultra_gpu.csv',
            'name': 'Starfield Ultra',
            'description': 'Starfield GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'gpuBench/starfield_4k_ultra_gpu.csv',
            'name': 'Starfield Ultra',
            'description': 'Starfield GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '4K'
        },
        {
            'file': 'gpuBench/ffxiv_dawntrail_1440p_maximum.csv',
            'name': 'FFXIV Dawntrail Maximum',
            'description': 'Final Fantasy XIV Dawntrail GPU performance at Maximum settings',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'gpuBench/ffxiv_dawntrail_4k_maximum.csv',
            'name': 'FFXIV Dawntrail Maximum',
            'description': 'Final Fantasy XIV Dawntrail GPU performance at Maximum settings',
            'unit': 'fps',
            'resolution': '4K'
        },
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