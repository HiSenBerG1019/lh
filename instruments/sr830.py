"""
Stanford Research Systems SR830 Lock-in Amplifier Control Module

This module provides a Python interface for controlling the SR830 lock-in amplifier
via VISA protocol.
"""

import pyvisa
import time


class SR830:
    """
    Class for controlling SR830 Lock-in Amplifier.
    
    The SR830 is a digital lock-in amplifier with frequency range from 1 mHz to 102.4 kHz.
    Uses VISA for communication over GPIB, USB, or RS-232.
    
    Attributes:
        resource_name (str): VISA resource name for the instrument
        instrument: PyVISA instrument object
    """
    
    # Sensitivity settings (V)
    SENSITIVITY = {
        0: 2e-9, 1: 5e-9, 2: 10e-9, 3: 20e-9, 4: 50e-9, 5: 100e-9,
        6: 200e-9, 7: 500e-9, 8: 1e-6, 9: 2e-6, 10: 5e-6, 11: 10e-6,
        12: 20e-6, 13: 50e-6, 14: 100e-6, 15: 200e-6, 16: 500e-6,
        17: 1e-3, 18: 2e-3, 19: 5e-3, 20: 10e-3, 21: 20e-3, 22: 50e-3,
        23: 100e-3, 24: 200e-3, 25: 500e-3, 26: 1.0
    }
    
    # Time constant settings (s)
    TIME_CONSTANT = {
        0: 10e-6, 1: 30e-6, 2: 100e-6, 3: 300e-6, 4: 1e-3, 5: 3e-3,
        6: 10e-3, 7: 30e-3, 8: 100e-3, 9: 300e-3, 10: 1.0, 11: 3.0,
        12: 10.0, 13: 30.0, 14: 100.0, 15: 300.0, 16: 1e3, 17: 3e3,
        18: 10e3, 19: 30e3
    }
    
    def __init__(self, resource_name):
        """
        Initialize connection to SR830 lock-in amplifier.
        
        Args:
            resource_name (str): VISA resource name (e.g., 'GPIB0::8::INSTR')
        """
        self.resource_name = resource_name
        self.rm = pyvisa.ResourceManager()
        self.instrument = None
        
    def connect(self):
        """
        Establish connection to the instrument.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.instrument = self.rm.open_resource(self.resource_name)
            self.instrument.timeout = 5000  # 5 second timeout
            return True
        except Exception as e:
            print(f"Failed to connect to SR830: {e}")
            return False
            
    def disconnect(self):
        """Close connection to the instrument."""
        if self.instrument:
            self.instrument.close()
            self.instrument = None
            
    def identify(self):
        """
        Get instrument identification string.
        
        Returns:
            str: Identification string from the instrument
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        return self.instrument.query("*IDN?").strip()
        
    def reset(self):
        """Reset the instrument to default settings."""
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write("*RST")
        
    def set_frequency(self, frequency):
        """
        Set the reference frequency.
        
        Args:
            frequency (float): Frequency in Hz (0.001 to 102000)
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(f"FREQ {frequency}")
        
    def get_frequency(self):
        """
        Get the reference frequency.
        
        Returns:
            float: Frequency in Hz
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("FREQ?")
        return float(response.strip())
        
    def set_amplitude(self, amplitude):
        """
        Set the sine output amplitude.
        
        Args:
            amplitude (float): Amplitude in volts (0.004 to 5.0)
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(f"SLVL {amplitude}")
        
    def get_amplitude(self):
        """
        Get the sine output amplitude.
        
        Returns:
            float: Amplitude in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("SLVL?")
        return float(response.strip())
        
    def set_sensitivity(self, sensitivity_code):
        """
        Set the sensitivity.
        
        Args:
            sensitivity_code (int): Sensitivity code (0-26, see SENSITIVITY dict)
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        if sensitivity_code not in self.SENSITIVITY:
            raise ValueError(f"Invalid sensitivity code. Must be 0-26")
        self.instrument.write(f"SENS {sensitivity_code}")
        
    def get_sensitivity(self):
        """
        Get the sensitivity code.
        
        Returns:
            int: Sensitivity code
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("SENS?")
        return int(response.strip())
        
    def set_time_constant(self, tc_code):
        """
        Set the time constant.
        
        Args:
            tc_code (int): Time constant code (0-19, see TIME_CONSTANT dict)
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        if tc_code not in self.TIME_CONSTANT:
            raise ValueError(f"Invalid time constant code. Must be 0-19")
        self.instrument.write(f"OFLT {tc_code}")
        
    def get_time_constant(self):
        """
        Get the time constant code.
        
        Returns:
            int: Time constant code
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("OFLT?")
        return int(response.strip())
        
    def set_phase(self, phase):
        """
        Set the reference phase shift.
        
        Args:
            phase (float): Phase in degrees (-360 to 729.99)
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(f"PHAS {phase}")
        
    def get_phase(self):
        """
        Get the reference phase shift.
        
        Returns:
            float: Phase in degrees
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("PHAS?")
        return float(response.strip())
        
    def auto_phase(self):
        """Automatically set the phase."""
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write("APHS")
        
    def auto_gain(self):
        """Automatically set the gain (sensitivity)."""
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write("AGAN")
        
    def get_x(self):
        """
        Get the X channel output.
        
        Returns:
            float: X value in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("OUTP? 1")
        return float(response.strip())
        
    def get_y(self):
        """
        Get the Y channel output.
        
        Returns:
            float: Y value in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("OUTP? 2")
        return float(response.strip())
        
    def get_r(self):
        """
        Get the R (magnitude) output.
        
        Returns:
            float: R value in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("OUTP? 3")
        return float(response.strip())
        
    def get_theta(self):
        """
        Get the theta (phase) output.
        
        Returns:
            float: Theta value in degrees
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("OUTP? 4")
        return float(response.strip())
        
    def get_xy(self):
        """
        Get both X and Y outputs simultaneously.
        
        Returns:
            tuple: (X, Y) values in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("SNAP? 1,2")
        values = response.strip().split(',')
        return float(values[0]), float(values[1])
        
    def get_r_theta(self):
        """
        Get both R and theta outputs simultaneously.
        
        Returns:
            tuple: (R, theta) where R is in volts and theta in degrees
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query("SNAP? 3,4")
        values = response.strip().split(',')
        return float(values[0]), float(values[1])
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
