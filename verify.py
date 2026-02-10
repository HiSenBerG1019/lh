"""
Verification script to check that all instrument modules are properly structured.

This script performs basic checks without requiring external dependencies to be installed.
"""

import sys
import os
import ast

def check_file_syntax(filepath):
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r') as f:
            ast.parse(f.read())
        return True, "OK"
    except SyntaxError as e:
        return False, str(e)

def check_module_structure():
    """Verify the module structure is correct."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    required_files = [
        'instruments/__init__.py',
        'instruments/keithley.py',
        'instruments/sr830.py',
        'instruments/zurich.py',
        'examples/keithley_example.py',
        'examples/sr830_example.py',
        'examples/zurich_example.py',
        'requirements.txt',
        'setup.py',
        '.gitignore',
        'README.md'
    ]
    
    print("Checking module structure...")
    all_good = True
    
    for filepath in required_files:
        full_path = os.path.join(base_dir, filepath)
        if os.path.exists(full_path):
            print(f"✓ {filepath} exists")
            
            # Check Python files for syntax
            if filepath.endswith('.py'):
                success, msg = check_file_syntax(full_path)
                if success:
                    print(f"  ✓ Valid Python syntax")
                else:
                    print(f"  ✗ Syntax error: {msg}")
                    all_good = False
        else:
            print(f"✗ {filepath} missing")
            all_good = False
    
    return all_good

def check_class_definitions():
    """Verify that key classes are defined."""
    print("\nChecking class definitions...")
    
    classes_to_check = [
        ('instruments/keithley.py', 'Keithley'),
        ('instruments/sr830.py', 'SR830'),
        ('instruments/zurich.py', 'ZurichInstrument'),
    ]
    
    all_good = True
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for filepath, classname in classes_to_check:
        full_path = os.path.join(base_dir, filepath)
        with open(full_path, 'r') as f:
            content = f.read()
            if f"class {classname}" in content:
                print(f"✓ {classname} class defined in {filepath}")
                
                # Check for key methods
                methods = ['connect', 'disconnect', '__enter__', '__exit__']
                for method in methods:
                    if f"def {method}" in content:
                        print(f"  ✓ {method}() method found")
                    else:
                        print(f"  ✗ {method}() method missing")
                        all_good = False
            else:
                print(f"✗ {classname} class not found in {filepath}")
                all_good = False
    
    return all_good

def check_requirements():
    """Check requirements.txt content."""
    print("\nChecking requirements...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    req_file = os.path.join(base_dir, 'requirements.txt')
    
    required_packages = ['pyvisa', 'pyvisa-py', 'zhinst', 'numpy']
    
    with open(req_file, 'r') as f:
        content = f.read()
    
    all_good = True
    for package in required_packages:
        if package in content:
            print(f"✓ {package} in requirements.txt")
        else:
            print(f"✗ {package} missing from requirements.txt")
            all_good = False
    
    return all_good

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Laboratory Instrument Control - Verification Script")
    print("=" * 60)
    
    results = []
    
    # Run checks
    results.append(("Module Structure", check_module_structure()))
    results.append(("Class Definitions", check_class_definitions()))
    results.append(("Requirements", check_requirements()))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "PASSED" if passed else "FAILED"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {check_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All verification checks passed!")
        print("\nThe instrument control modules are ready to use.")
        print("Install dependencies with: pip install -r requirements.txt")
        return 0
    else:
        print("\n✗ Some verification checks failed.")
        print("Please review the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
