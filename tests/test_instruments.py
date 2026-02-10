"""
Basic tests for instrument control modules

These tests verify that the modules can be imported and instantiated
without requiring actual hardware connections.
"""

import unittest
from instruments import Keithley, SR830, ZurichInstrument


class TestKeithley(unittest.TestCase):
    """Test Keithley class basic functionality."""
    
    def test_import(self):
        """Test that Keithley class can be imported."""
        self.assertIsNotNone(Keithley)
    
    def test_instantiation(self):
        """Test that Keithley instance can be created."""
        keithley = Keithley("GPIB0::24::INSTR")
        self.assertIsNotNone(keithley)
        self.assertEqual(keithley.resource_name, "GPIB0::24::INSTR")
    
    def test_context_manager(self):
        """Test that Keithley supports context manager protocol."""
        self.assertTrue(hasattr(Keithley, '__enter__'))
        self.assertTrue(hasattr(Keithley, '__exit__'))


class TestSR830(unittest.TestCase):
    """Test SR830 class basic functionality."""
    
    def test_import(self):
        """Test that SR830 class can be imported."""
        self.assertIsNotNone(SR830)
    
    def test_instantiation(self):
        """Test that SR830 instance can be created."""
        sr830 = SR830("GPIB0::8::INSTR")
        self.assertIsNotNone(sr830)
        self.assertEqual(sr830.resource_name, "GPIB0::8::INSTR")
    
    def test_sensitivity_dict(self):
        """Test that sensitivity dictionary is defined."""
        self.assertIsInstance(SR830.SENSITIVITY, dict)
        self.assertIn(0, SR830.SENSITIVITY)
        self.assertIn(26, SR830.SENSITIVITY)
    
    def test_time_constant_dict(self):
        """Test that time constant dictionary is defined."""
        self.assertIsInstance(SR830.TIME_CONSTANT, dict)
        self.assertIn(0, SR830.TIME_CONSTANT)
        self.assertIn(19, SR830.TIME_CONSTANT)
    
    def test_context_manager(self):
        """Test that SR830 supports context manager protocol."""
        self.assertTrue(hasattr(SR830, '__enter__'))
        self.assertTrue(hasattr(SR830, '__exit__'))


class TestZurichInstrument(unittest.TestCase):
    """Test ZurichInstrument class basic functionality."""
    
    def test_import(self):
        """Test that ZurichInstrument class can be imported."""
        self.assertIsNotNone(ZurichInstrument)
    
    def test_instantiation(self):
        """Test that ZurichInstrument instance can be created."""
        zi = ZurichInstrument("dev1234")
        self.assertIsNotNone(zi)
        self.assertEqual(zi.device_id, "dev1234")
    
    def test_instantiation_uppercase(self):
        """Test that device ID is converted to lowercase."""
        zi = ZurichInstrument("DEV1234")
        self.assertEqual(zi.device_id, "dev1234")
    
    def test_default_parameters(self):
        """Test default connection parameters."""
        zi = ZurichInstrument("dev1234")
        self.assertEqual(zi.server_host, "localhost")
        self.assertEqual(zi.server_port, 8004)
        self.assertEqual(zi.api_level, 6)
    
    def test_custom_parameters(self):
        """Test custom connection parameters."""
        zi = ZurichInstrument("dev1234", server_host="192.168.1.100", 
                             server_port=8005, api_level=5)
        self.assertEqual(zi.server_host, "192.168.1.100")
        self.assertEqual(zi.server_port, 8005)
        self.assertEqual(zi.api_level, 5)
    
    def test_context_manager(self):
        """Test that ZurichInstrument supports context manager protocol."""
        self.assertTrue(hasattr(ZurichInstrument, '__enter__'))
        self.assertTrue(hasattr(ZurichInstrument, '__exit__'))


class TestModuleImports(unittest.TestCase):
    """Test that all classes are available from main module."""
    
    def test_all_imports(self):
        """Test that all instruments can be imported from main module."""
        import instruments
        self.assertTrue(hasattr(instruments, 'Keithley'))
        self.assertTrue(hasattr(instruments, 'SR830'))
        self.assertTrue(hasattr(instruments, 'ZurichInstrument'))
    
    def test_version(self):
        """Test that module version is defined."""
        import instruments
        self.assertTrue(hasattr(instruments, '__version__'))


if __name__ == '__main__':
    unittest.main()
