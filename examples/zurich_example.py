"""
Example script for controlling Zurich Instruments devices

This example demonstrates basic operations with Zurich Instruments:
- Connecting to the instrument
- Setting up demodulator parameters
- Reading lock-in data
- Using signal outputs
"""

from instruments import ZurichInstrument
import time
import numpy as np


def basic_example():
    """Basic usage example with context manager."""
    # Replace with your device ID (e.g., 'dev1234')
    device_id = "dev1234"
    
    with ZurichInstrument(device_id) as zi:
        # Identify the instrument
        info = zi.identify()
        print("Connected to Zurich Instrument:")
        print(f"  Device ID: {info['device_id']}")
        print(f"  Device Type: {info['device_type']}")
        print(f"  Serial: {info['serial']}")
        
        # Set oscillator frequency (1 kHz)
        zi.set_oscillator_frequency(osc_index=0, frequency=1000.0)
        freq = zi.get_oscillator_frequency(osc_index=0)
        print(f"\nOscillator frequency: {freq:.1f} Hz")
        
        # Set demodulator time constant (10 ms)
        zi.set_demod_time_constant(demod_index=0, time_constant=0.01)
        tc = zi.get_demod_time_constant(demod_index=0)
        print(f"Time constant: {tc*1000:.1f} ms")
        
        # Enable signal output
        zi.set_signal_output_amplitude(output_index=0, amplitude=0.5)
        zi.enable_signal_output(output_index=0, enable=True)
        amp = zi.get_signal_output_amplitude(output_index=0)
        print(f"Output amplitude: {amp:.3f} V")
        
        # Wait for settling
        zi.sync()
        time.sleep(0.1)
        
        # Get a demodulator sample
        sample = zi.get_demod_sample(demod_index=0)
        print(f"\nDemodulator sample:")
        print(f"  X = {sample['x']*1e6:.3f} µV")
        print(f"  Y = {sample['y']*1e6:.3f} µV")
        print(f"  R = {sample['r']*1e6:.3f} µV")
        print(f"  θ = {sample['theta']:.2f}°")
        
        # Disable output
        zi.enable_signal_output(output_index=0, enable=False)


def frequency_sweep_example():
    """Example: Perform a frequency sweep."""
    device_id = "dev1234"
    
    with ZurichInstrument(device_id) as zi:
        print("Starting frequency sweep...")
        
        # Setup
        zi.set_signal_output_amplitude(output_index=0, amplitude=0.1)
        zi.enable_signal_output(output_index=0, enable=True)
        zi.set_demod_time_constant(demod_index=0, time_constant=0.01)
        
        # Frequency sweep parameters
        f_start = 100.0
        f_stop = 10000.0
        num_points = 20
        frequencies = np.logspace(np.log10(f_start), np.log10(f_stop), num_points)
        
        results = []
        
        for freq in frequencies:
            zi.set_oscillator_frequency(osc_index=0, frequency=freq)
            zi.sync()
            time.sleep(0.05)  # Wait for settling
            
            sample = zi.get_demod_sample(demod_index=0)
            results.append((freq, sample['r'], sample['theta']))
            print(f"f = {freq:.1f} Hz, R = {sample['r']*1e3:.3f} mV, θ = {sample['theta']:.1f}°")
        
        # Cleanup
        zi.enable_signal_output(output_index=0, enable=False)
        
        print(f"\nSweep complete. Collected {len(results)} data points.")
        
        return results


def continuous_monitoring_example():
    """Example: Continuously monitor demodulator output."""
    device_id = "dev1234"
    
    with ZurichInstrument(device_id) as zi:
        print("Continuous monitoring (Ctrl+C to stop)...")
        
        # Setup
        zi.set_oscillator_frequency(osc_index=0, frequency=1000.0)
        zi.set_demod_time_constant(demod_index=0, time_constant=0.001)
        zi.set_signal_output_amplitude(output_index=0, amplitude=0.5)
        zi.enable_signal_output(output_index=0, enable=True)
        zi.sync()
        
        try:
            while True:
                sample = zi.get_demod_sample(demod_index=0)
                print(f"X = {sample['x']*1e6:8.3f} µV, "
                      f"Y = {sample['y']*1e6:8.3f} µV, "
                      f"R = {sample['r']*1e6:8.3f} µV, "
                      f"θ = {sample['theta']:6.2f}°", end='\r')
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
        finally:
            zi.enable_signal_output(output_index=0, enable=False)


def advanced_settings_example():
    """Example: Using low-level set/get methods for advanced settings."""
    device_id = "dev1234"
    
    with ZurichInstrument(device_id) as zi:
        print("Advanced settings example...")
        
        # Use generic set/get methods for any parameter
        # Set demodulator order (1 to 8)
        zi.set('demods/0/order', 4)
        order = zi.get('demods/0/order')
        print(f"Demodulator filter order: {order}")
        
        # Set input range
        zi.set('sigins/0/range', 1.0)  # 1V range
        input_range = zi.get('sigins/0/range')
        print(f"Input range: {input_range} V")
        
        # Set output offset
        zi.set('sigouts/0/offset', 0.0)
        offset = zi.get('sigouts/0/offset')
        print(f"Output offset: {offset} V")
        
        # Enable input AC coupling
        zi.set('sigins/0/ac', 0)  # 0=DC, 1=AC
        ac_coupling = zi.get('sigins/0/ac')
        print(f"AC coupling: {'enabled' if ac_coupling else 'disabled'}")


if __name__ == "__main__":
    print("=== Zurich Instruments Control Examples ===\n")
    
    # Uncomment the example you want to run:
    
    # basic_example()
    # frequency_sweep_example()
    # continuous_monitoring_example()
    # advanced_settings_example()
    
    print("\nNote: Update the device_id with your instrument's serial number")
    print("Make sure the LabOne Data Server is running")
    print("Examples are commented out to prevent errors without hardware connected")
