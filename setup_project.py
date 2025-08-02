"""
Create project structure for Digital Wellness Coach
"""
import os

def create_project_structure():
    """Create all necessary directories and files"""
    
    print("🏗️ Creating Digital Wellness Coach project structure...")
    
    # Create directories
    directories = [
        'agents',
        'tools', 
        'tasks',
        'data',
        'utils',
        'tests',
        'docs',
        'outputs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}/")
        
        # Create __init__.py files for Python packages
        if directory in ['agents', 'tools', 'tasks', 'utils']:
            init_file = os.path.join(directory, '__init__.py')
            with open(init_file, 'w') as f:
                f.write(f'# {directory} package\n')
            print(f"   📄 Created {init_file}")
    
    print("\n✅ Project structure created successfully!")
    print("\n📊 Your project structure:")
    print("DigitalWellnessCoach/")
    for directory in directories:
        print(f"├── {directory}/")
    print("├── venv/")
    print("├── .git/")
    print("├── requirements.txt")
    print("└── setup_project.py")
    
    return True

if __name__ == "__main__":
    create_project_structure()