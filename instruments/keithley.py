"""
Keithley Source Measurement Unit (SMU) Control Module

This module provides a Python interface for controlling Keithley instruments
(e.g., Keithley 2400, 2450, 6221) via VISA protocol.
"""

import pyvisa


class Keithley:
    """
    Class for controlling Keithley Source Measurement Units.
    
    Supports common Keithley models including 2400, 2450, 6221, etc.
    Uses VISA for communication over GPIB, USB, or Ethernet.
    
    Attributes:
        resource_name (str): VISA resource name for the instrument
        instrument: PyVISA instrument object
    """
    
    def __init__(self, resource_name):
        """
        Initialize connection to Keithley instrument.
        
        Args:
            resource_name (str): VISA resource name (e.g., 'GPIB0::24::INSTR')
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
            print(f"Failed to connect to Keithley: {e}")
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
        
    def set_source_voltage(self, voltage):
        """
        Set the source voltage.
        
        Args:
            voltage (float): Voltage to set in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(f":SOUR:VOLT {voltage}")
        
    def set_source_current(self, current):
        """
        Set the source current.
        
        Args:
            current (float): Current to set in amperes
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(f":SOUR:CURR {current}")
        
    def set_compliance_voltage(self, voltage):
        """
        Set the compliance (limit) voltage.
        
        Args:
            voltage (float): Compliance voltage in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(f":SENS:VOLT:PROT {voltage}")
        
    def set_compliance_current(self, current):
        """
        Set the compliance (limit) current.
        
        Args:
            current (float): Compliance current in amperes
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(f":SENS:CURR:PROT {current}")
        
    def output_on(self):
        """Turn on the output."""
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(":OUTP ON")
        
    def output_off(self):
        """Turn off the output."""
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        self.instrument.write(":OUTP OFF")
        
    def measure_voltage(self):
        """
        Measure voltage.
        
        Returns:
            float: Measured voltage in volts
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query(":MEAS:VOLT?")
        return float(response.strip())
        
    def measure_current(self):
        """
        Measure current.
        
        Returns:
            float: Measured current in amperes
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query(":MEAS:CURR?")
        return float(response.strip())
        
    def measure_resistance(self):
        """
        Measure resistance.
        
        Returns:
            float: Measured resistance in ohms
        """
        if not self.instrument:
            raise ConnectionError("Not connected to instrument")
        response = self.instrument.query(":MEAS:RES?")
        return float(response.strip())
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
