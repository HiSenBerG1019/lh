"""
Example script for controlling a Keithley Source Measurement Unit

This example demonstrates basic operations with a Keithley instrument:
- Connecting to the instrument
- Identifying the device
- Setting up voltage source
- Taking measurements
- IV sweep example
"""

from instruments import Keithley
import time
import numpy as np


def basic_example():
    """Basic usage example with context manager."""
    # Replace with your instrument's VISA address
    resource_name = "GPIB0::24::INSTR"
    
    with Keithley(resource_name) as keithley:
        # Identify the instrument
        print("Connected to:", keithley.identify())
        
        # Reset to default state
        keithley.reset()
        time.sleep(1)
        
        # Configure as voltage source with current measurement
        keithley.set_source_voltage(1.0)  # Set to 1V
        keithley.set_compliance_current(0.01)  # 10mA compliance
        
        # Turn on output
        keithley.output_on()
        time.sleep(0.5)
        
        # Measure current
        current = keithley.measure_current()
        print(f"Measured current: {current*1e3:.3f} mA")
        
        # Turn off output
        keithley.output_off()


def iv_sweep_example():
    """Example: Perform an I-V sweep."""
    resource_name = "GPIB0::24::INSTR"
    
    with Keithley(resource_name) as keithley:
        print("Starting I-V sweep...")
        keithley.reset()
        time.sleep(1)
        
        # Set compliance
        keithley.set_compliance_current(0.1)  # 100mA compliance
        
        # Voltage sweep parameters
        v_start = 0.0
        v_stop = 5.0
        v_step = 0.1
        voltages = np.arange(v_start, v_stop + v_step, v_step)
        
        results = []
        keithley.output_on()
        
        try:
            for voltage in voltages:
                keithley.set_source_voltage(voltage)
                time.sleep(0.1)  # Wait for settling
                
                current = keithley.measure_current()
                results.append((voltage, current))
                print(f"V = {voltage:.2f} V, I = {current*1e3:.3f} mA")
                
        finally:
            # Always turn off output
            keithley.output_off()
        
        # You can now plot or save the results
        print(f"\nSweep complete. Collected {len(results)} data points.")
        
        return results


def current_source_example():
    """Example: Use Keithley as a current source."""
    resource_name = "GPIB0::24::INSTR"
    
    with Keithley(resource_name) as keithley:
        print("Current source mode...")
        keithley.reset()
        time.sleep(1)
        
        # Configure as current source
        keithley.set_source_current(0.001)  # 1mA
        keithley.set_compliance_voltage(10.0)  # 10V compliance
        
        keithley.output_on()
        time.sleep(0.5)
        
        # Measure voltage
        voltage = keithley.measure_voltage()
        print(f"Measured voltage: {voltage:.3f} V")
        
        keithley.output_off()


if __name__ == "__main__":
    print("=== Keithley Control Examples ===\n")
    
    # Uncomment the example you want to run:
    
    # basic_example()
    # iv_sweep_example()
    # current_source_example()
    
    print("\nNote: Update the resource_name with your instrument's VISA address")
    print("Examples are commented out to prevent errors without hardware connected")
