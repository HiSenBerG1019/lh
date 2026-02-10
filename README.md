# lh - Laboratory Instrument Control

Python library for controlling laboratory instruments including Keithley source measurement units, SR830 lock-in amplifiers, and Zurich Instruments devices.

## Features

- **Keithley Control**: Full support for Keithley source measurement units (SMU) such as Keithley 2400, 2450, 6221
  - Voltage and current sourcing
  - Voltage, current, and resistance measurements
  - Compliance settings
  - IV sweep capabilities

- **SR830 Control**: Complete interface for Stanford Research Systems SR830 lock-in amplifier
  - Frequency, amplitude, phase control
  - Sensitivity and time constant settings
  - X, Y, R, and θ measurements
  - Auto-phase and auto-gain features
  - Frequency sweep capabilities

- **Zurich Instruments Control**: Support for Zurich Instruments lock-in amplifiers (MFLI, UHFLI, HF2LI, etc.)
  - Oscillator and demodulator control
  - Signal input/output configuration
  - Real-time data acquisition
  - Advanced parameter access

## Installation

### Prerequisites

- Python 3.7 or higher
- For Keithley and SR830: VISA backend (NI-VISA or pyvisa-py)
- For Zurich Instruments: LabOne software and API

### Install from source

```bash
git clone https://github.com/HiSenBerG1019/lh.git
cd lh
pip install -r requirements.txt
pip install -e .
```

### Dependencies

```bash
pip install pyvisa pyvisa-py zhinst numpy
```

## Quick Start

### Keithley Example

```python
from instruments import Keithley

# Connect to Keithley SMU
with Keithley("GPIB0::24::INSTR") as keithley:
    # Identify device
    print(keithley.identify())
    
    # Configure as voltage source
    keithley.set_source_voltage(1.0)  # 1V
    keithley.set_compliance_current(0.01)  # 10mA compliance
    
    # Turn on output and measure
    keithley.output_on()
    current = keithley.measure_current()
    print(f"Current: {current*1e3:.3f} mA")
    
    # Turn off output
    keithley.output_off()
```

### SR830 Example

```python
from instruments import SR830

# Connect to SR830 lock-in amplifier
with SR830("GPIB0::8::INSTR") as lockin:
    # Set parameters
    lockin.set_frequency(1000.0)  # 1 kHz
    lockin.set_amplitude(1.0)  # 1V
    lockin.set_time_constant(9)  # 300 ms
    
    # Take measurements
    x, y = lockin.get_xy()
    r, theta = lockin.get_r_theta()
    print(f"X={x:.6e} V, Y={y:.6e} V")
    print(f"R={r:.6e} V, θ={theta:.2f}°")
```

### Zurich Instruments Example

```python
from instruments import ZurichInstrument

# Connect to Zurich Instrument (replace with your device ID)
with ZurichInstrument("dev1234") as zi:
    # Set oscillator frequency
    zi.set_oscillator_frequency(osc_index=0, frequency=1000.0)
    
    # Configure output
    zi.set_signal_output_amplitude(output_index=0, amplitude=0.5)
    zi.enable_signal_output(output_index=0, enable=True)
    
    # Get demodulator sample
    sample = zi.get_demod_sample(demod_index=0)
    print(f"R={sample['r']:.6e} V, θ={sample['theta']:.2f}°")
```

## Examples

Detailed examples for each instrument are available in the `examples/` directory:

- `keithley_example.py` - Basic usage, IV sweeps, current source mode
- `sr830_example.py` - Basic measurements, auto-setup, frequency sweeps, continuous monitoring
- `zurich_example.py` - Basic usage, frequency sweeps, continuous monitoring, advanced settings

## Documentation

### Keithley Class Methods

#### Connection
- `connect()` - Establish connection to instrument
- `disconnect()` - Close connection
- `identify()` - Get instrument ID string
- `reset()` - Reset to default settings

#### Source Configuration
- `set_source_voltage(voltage)` - Set output voltage (V)
- `set_source_current(current)` - Set output current (A)
- `set_compliance_voltage(voltage)` - Set voltage compliance (V)
- `set_compliance_current(current)` - Set current compliance (A)

#### Output Control
- `output_on()` - Enable output
- `output_off()` - Disable output

#### Measurements
- `measure_voltage()` - Measure voltage (returns float in V)
- `measure_current()` - Measure current (returns float in A)
- `measure_resistance()` - Measure resistance (returns float in Ω)

### SR830 Class Methods

#### Connection
- `connect()` - Establish connection
- `disconnect()` - Close connection
- `identify()` - Get instrument ID
- `reset()` - Reset instrument

#### Configuration
- `set_frequency(frequency)` - Set reference frequency (Hz)
- `set_amplitude(amplitude)` - Set sine output amplitude (V)
- `set_sensitivity(code)` - Set sensitivity (0-26)
- `set_time_constant(code)` - Set time constant (0-19)
- `set_phase(phase)` - Set reference phase (degrees)

#### Auto Functions
- `auto_phase()` - Automatically optimize phase
- `auto_gain()` - Automatically optimize sensitivity

#### Measurements
- `get_x()` - Get X output (V)
- `get_y()` - Get Y output (V)
- `get_r()` - Get R magnitude (V)
- `get_theta()` - Get phase (degrees)
- `get_xy()` - Get both X and Y (returns tuple)
- `get_r_theta()` - Get both R and θ (returns tuple)

### ZurichInstrument Class Methods

#### Connection
- `connect()` - Establish connection
- `disconnect()` - Close connection
- `identify()` - Get device information (returns dict)

#### Generic Access
- `set(path, value)` - Set any parameter
- `get(path)` - Get any parameter value

#### Oscillator Control
- `set_oscillator_frequency(osc_index, frequency)` - Set oscillator frequency (Hz)
- `get_oscillator_frequency(osc_index)` - Get oscillator frequency

#### Demodulator Control
- `set_demod_time_constant(demod_index, time_constant)` - Set time constant (s)
- `get_demod_time_constant(demod_index)` - Get time constant
- `get_demod_sample(demod_index)` - Get demodulator sample (returns dict with x, y, r, theta)

#### Signal Output
- `set_signal_output_amplitude(output_index, amplitude)` - Set output amplitude (V)
- `get_signal_output_amplitude(output_index)` - Get output amplitude
- `enable_signal_output(output_index, enable)` - Enable/disable output

#### Utility
- `sync()` - Wait for all commands to complete

## Hardware Setup

### GPIB/VISA Instruments (Keithley, SR830)

1. Install NI-VISA or use pyvisa-py backend
2. Connect instrument via GPIB, USB, or Ethernet
3. Find the VISA resource name using:
   ```python
   import pyvisa
   rm = pyvisa.ResourceManager()
   print(rm.list_resources())
   ```

### Zurich Instruments

1. Install LabOne software from Zurich Instruments
2. Start the LabOne Data Server
3. Connect instrument via Ethernet or USB
4. Note the device ID (e.g., 'dev1234')

## Troubleshooting

### VISA Connection Issues
- Ensure VISA backend is installed: `pip install pyvisa-py`
- Check instrument is powered on and connected
- Verify resource name using `pyvisa.ResourceManager().list_resources()`
- Check GPIB address settings on instrument

### Zurich Instruments Connection Issues
- Ensure LabOne Data Server is running
- Check device is visible in LabOne UI
- Verify network connection (ping the device)
- Use correct device ID (lowercase, e.g., 'dev1234')

### Timeout Errors
- Increase timeout: `instrument.instrument.timeout = 10000` (10 seconds)
- Check for conflicting connections (close other programs)
- Ensure instrument is responding (test with native software)

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Built using PyVISA for GPIB/VISA communication
- Zurich Instruments API (zhinst) for Zurich Instruments devices
- Inspired by the need for simple, Pythonic instrument control