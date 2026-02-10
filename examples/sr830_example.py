"""
Example script for controlling a Stanford Research Systems SR830 Lock-in Amplifier

This example demonstrates basic operations with an SR830:
- Connecting to the instrument
- Setting up measurement parameters
- Reading lock-in data
- Frequency sweep example
"""

from instruments import SR830
import time
import numpy as np


def basic_example():
    """Basic usage example with context manager."""
    # Replace with your instrument's VISA address
    resource_name = "GPIB0::8::INSTR"
    
    with SR830(resource_name) as lockin:
        # Identify the instrument
        print("Connected to:", lockin.identify())
        
        # Reset to default state
        lockin.reset()
        time.sleep(2)
        
        # Set measurement parameters
        lockin.set_frequency(1000.0)  # 1 kHz
        lockin.set_amplitude(1.0)  # 1V sine output
        lockin.set_time_constant(9)  # 300 ms (code 9)
        lockin.set_sensitivity(12)  # 20 µV (code 12)
        
        # Read current settings
        freq = lockin.get_frequency()
        amp = lockin.get_amplitude()
        print(f"Frequency: {freq:.1f} Hz")
        print(f"Amplitude: {amp:.3f} V")
        
        # Take measurements
        time.sleep(5 * 0.3)  # Wait ~5 time constants
        
        x, y = lockin.get_xy()
        r, theta = lockin.get_r_theta()
        
        print(f"\nMeasurements:")
        print(f"X = {x*1e6:.3f} µV")
        print(f"Y = {y*1e6:.3f} µV")
        print(f"R = {r*1e6:.3f} µV")
        print(f"θ = {theta:.2f}°")


def auto_setup_example():
    """Example: Use auto-phase and auto-gain features."""
    resource_name = "GPIB0::8::INSTR"
    
    with SR830(resource_name) as lockin:
        print("Auto-setup example...")
        
        # Set basic parameters
        lockin.set_frequency(1000.0)
        lockin.set_amplitude(1.0)
        lockin.set_time_constant(10)  # 1 s
        
        # Wait for settling
        time.sleep(5)
        
        # Automatically optimize phase
        print("Running auto-phase...")
        lockin.auto_phase()
        time.sleep(2)
        
        phase = lockin.get_phase()
        print(f"Optimized phase: {phase:.2f}°")
        
        # Automatically optimize gain (sensitivity)
        print("Running auto-gain...")
        lockin.auto_gain()
        time.sleep(2)
        
        sens_code = lockin.get_sensitivity()
        sens_value = SR830.SENSITIVITY[sens_code]
        print(f"Optimized sensitivity: {sens_value:.2e} V (code {sens_code})")
        
        # Take measurement
        r = lockin.get_r()
        print(f"Signal magnitude: {r:.6e} V")


def frequency_sweep_example():
    """Example: Perform a frequency sweep."""
    resource_name = "GPIB0::8::INSTR"
    
    with SR830(resource_name) as lockin:
        print("Starting frequency sweep...")
        
        # Setup
        lockin.set_amplitude(1.0)
        lockin.set_time_constant(8)  # 100 ms
        lockin.set_sensitivity(20)  # 10 mV
        
        # Frequency sweep parameters
        f_start = 100.0
        f_stop = 10000.0
        num_points = 20
        frequencies = np.logspace(np.log10(f_start), np.log10(f_stop), num_points)
        
        results = []
        
        for freq in frequencies:
            lockin.set_frequency(freq)
            time.sleep(5 * 0.1)  # Wait 5 time constants
            
            r, theta = lockin.get_r_theta()
            results.append((freq, r, theta))
            print(f"f = {freq:.1f} Hz, R = {r*1e3:.3f} mV, θ = {theta:.1f}°")
        
        print(f"\nSweep complete. Collected {len(results)} data points.")
        
        return results


def continuous_monitoring_example():
    """Example: Continuously monitor the signal."""
    resource_name = "GPIB0::8::INSTR"
    
    with SR830(resource_name) as lockin:
        print("Continuous monitoring (Ctrl+C to stop)...")
        
        lockin.set_frequency(1000.0)
        lockin.set_amplitude(1.0)
        lockin.set_time_constant(7)  # 30 ms
        lockin.set_sensitivity(15)  # 200 µV
        
        try:
            while True:
                x, y = lockin.get_xy()
                r = np.sqrt(x**2 + y**2)
                print(f"X = {x*1e6:8.3f} µV, Y = {y*1e6:8.3f} µV, R = {r*1e6:8.3f} µV", end='\r')
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")


if __name__ == "__main__":
    print("=== SR830 Lock-in Amplifier Control Examples ===\n")
    
    # Uncomment the example you want to run:
    
    # basic_example()
    # auto_setup_example()
    # frequency_sweep_example()
    # continuous_monitoring_example()
    
    print("\nNote: Update the resource_name with your instrument's VISA address")
    print("Examples are commented out to prevent errors without hardware connected")
