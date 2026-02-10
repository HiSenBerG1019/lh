"""
Zurich Instruments Control Module

This module provides a Python interface for controlling Zurich Instruments devices
(e.g., MFLI, UHFLI, HF2LI) using the Zurich Instruments API (zhinst).
"""

import zhinst.core
import numpy as np


class ZurichInstrument:
    """
    Class for controlling Zurich Instruments lock-in amplifiers and similar devices.
    
    Supports various Zurich Instruments models including MFLI, UHFLI, HF2LI, etc.
    Uses the zhinst API for communication via Ethernet.
    
    Attributes:
        device_id (str): Device serial number (e.g., 'dev1234')
        api_level (int): API level (default: 6)
        daq: Data acquisition module
        device: Device instance
    """
    
    def __init__(self, device_id, server_host='localhost', server_port=8004, api_level=6):
        """
        Initialize connection to Zurich Instruments device.
        
        Args:
            device_id (str): Device serial number (e.g., 'dev1234')
            server_host (str): LabOne Data Server host (default: 'localhost')
            server_port (int): LabOne Data Server port (default: 8004)
            api_level (int): API level (default: 6)
        """
        self.device_id = device_id.lower()
        self.server_host = server_host
        self.server_port = server_port
        self.api_level = api_level
        self.daq = None
        self.device = None
        
    def connect(self):
        """
        Establish connection to the instrument.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Create API session
            self.daq = zhinst.core.ziDAQServer(
                self.server_host, 
                self.server_port, 
                self.api_level
            )
            
            # Connect to device
            self.daq.connectDevice(self.device_id, '1GbE')
            self.device = self.device_id
            
            return True
        except Exception as e:
            print(f"Failed to connect to Zurich Instrument: {e}")
            return False
            
    def disconnect(self):
        """Close connection to the instrument."""
        if self.daq and self.device:
            self.daq.disconnectDevice(self.device)
            self.device = None
            self.daq = None
            
    def identify(self):
        """
        Get instrument identification information.
        
        Returns:
            dict: Dictionary with device information
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        info = {}
        info['device_id'] = self.device_id
        info['device_type'] = self.daq.getString(f'/{self.device}/features/devtype')
        info['serial'] = self.daq.getString(f'/{self.device}/features/serial')
        info['options'] = self.daq.getString(f'/{self.device}/features/options')
        
        return info
        
    def set(self, path, value):
        """
        Set a parameter value.
        
        Args:
            path (str): Parameter path (without device prefix)
            value: Value to set (type depends on parameter)
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        full_path = f'/{self.device}/{path}'
        if isinstance(value, (int, float)):
            self.daq.setDouble(full_path, value)
        else:
            self.daq.set(full_path, value)
        
    def get(self, path):
        """
        Get a parameter value.
        
        Args:
            path (str): Parameter path (without device prefix)
            
        Returns:
            Value of the parameter
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        full_path = f'/{self.device}/{path}'
        result = self.daq.get(full_path, True)
        
        # Extract value from result dictionary
        if full_path in result:
            return result[full_path][0]['value']
        return None
        
    def set_oscillator_frequency(self, osc_index=0, frequency=1000.0):
        """
        Set oscillator frequency.
        
        Args:
            osc_index (int): Oscillator index (default: 0)
            frequency (float): Frequency in Hz
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        path = f'/{self.device}/oscs/{osc_index}/freq'
        self.daq.setDouble(path, frequency)
        
    def get_oscillator_frequency(self, osc_index=0):
        """
        Get oscillator frequency.
        
        Args:
            osc_index (int): Oscillator index (default: 0)
            
        Returns:
            float: Frequency in Hz
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        path = f'/{self.device}/oscs/{osc_index}/freq'
        return self.daq.getDouble(path)
        
    def set_demod_time_constant(self, demod_index=0, time_constant=0.001):
        """
        Set demodulator time constant.
        
        Args:
            demod_index (int): Demodulator index (default: 0)
            time_constant (float): Time constant in seconds
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        path = f'/{self.device}/demods/{demod_index}/timeconstant'
        self.daq.setDouble(path, time_constant)
        
    def get_demod_time_constant(self, demod_index=0):
        """
        Get demodulator time constant.
        
        Args:
            demod_index (int): Demodulator index (default: 0)
            
        Returns:
            float: Time constant in seconds
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        path = f'/{self.device}/demods/{demod_index}/timeconstant'
        return self.daq.getDouble(path)
        
    def set_signal_output_amplitude(self, output_index=0, amplitude=1.0):
        """
        Set signal output amplitude.
        
        Args:
            output_index (int): Output channel index (default: 0)
            amplitude (float): Amplitude in volts
        
        Note:
            The wildcard '*' in the path sets all amplitude components.
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        # The wildcard '*' sets all amplitude components for the output
        path = f'/{self.device}/sigouts/{output_index}/amplitudes/*'
        self.daq.setDouble(path, amplitude)
        
    def get_signal_output_amplitude(self, output_index=0):
        """
        Get signal output amplitude.
        
        Args:
            output_index (int): Output channel index (default: 0)
            
        Returns:
            float: Amplitude in volts
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        path = f'/{self.device}/sigouts/{output_index}/amplitudes/0'
        return self.daq.getDouble(path)
        
    def enable_signal_output(self, output_index=0, enable=True):
        """
        Enable or disable signal output.
        
        Args:
            output_index (int): Output channel index (default: 0)
            enable (bool): True to enable, False to disable
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        path = f'/{self.device}/sigouts/{output_index}/on'
        self.daq.setInt(path, 1 if enable else 0)
        
    def get_demod_sample(self, demod_index=0):
        """
        Get a single demodulator sample.
        
        Args:
            demod_index (int): Demodulator index (default: 0)
            
        Returns:
            dict: Dictionary with 'x', 'y', 'r', 'theta' values
        """
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        
        path = f'/{self.device}/demods/{demod_index}/sample'
        sample = self.daq.getSample(path)
        
        result = {
            'x': sample['x'][0],
            'y': sample['y'][0],
            'r': np.sqrt(sample['x'][0]**2 + sample['y'][0]**2),
            'theta': np.arctan2(sample['y'][0], sample['x'][0]) * 180 / np.pi
        }
        
        return result
        
    def sync(self):
        """Wait for all commands to complete."""
        if not self.daq:
            raise ConnectionError("Not connected to instrument")
        self.daq.sync()
        
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
