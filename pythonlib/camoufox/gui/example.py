#!/usr/bin/env python3
"""
Example script demonstrating how to launch the Camoufox GUI programmatically.

This script shows different ways to use the GUI feature.
"""

# Method 1: Direct import and launch
def method1():
    """Launch GUI directly from Python code"""
    from camoufox.gui import launch_gui
    launch_gui()


# Method 2: Using subprocess (useful for automation)
def method2():
    """Launch GUI using command line"""
    import subprocess
    subprocess.run(["python3", "-m", "camoufox", "gui"])


# Method 3: Using the CLI directly (from terminal)
# Just run: camoufox gui
# or: python3 -m camoufox gui


if __name__ == "__main__":
    print("Camoufox GUI Launch Examples")
    print("=" * 60)
    print()
    print("Method 1: Direct Python import")
    print("  from camoufox.gui import launch_gui")
    print("  launch_gui()")
    print()
    print("Method 2: Command line (subprocess)")
    print("  subprocess.run(['python3', '-m', 'camoufox', 'gui'])")
    print()
    print("Method 3: Direct CLI")
    print("  $ camoufox gui")
    print("  $ python3 -m camoufox gui")
    print()
    print("=" * 60)
    print()
    
    choice = input("Launch GUI now? (y/n): ")
    if choice.lower() == 'y':
        method1()
