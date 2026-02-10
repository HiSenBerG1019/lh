# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/HiSenBerG1019/lh.git
cd lh

# Install dependencies
pip install -r requirements.txt

# Install the package in development mode
pip install -e .
```

## Usage Examples

### 1. Keithley SMU Control

```python
from instruments import Keithley

# Connect and perform a simple measurement
with Keithley("GPIB0::24::INSTR") as smu:
    smu.set_source_voltage(1.0)
    smu.set_compliance_current(0.01)
    smu.output_on()
    
    current = smu.measure_current()
    print(f"Current: {current*1000} mA")
    
    smu.output_off()
```

### 2. SR830 Lock-in Amplifier

```python
from instruments import SR830

# Connect and measure lock-in signal
with SR830("GPIB0::8::INSTR") as lockin:
    lockin.set_frequency(1000.0)  # 1 kHz
    lockin.set_amplitude(1.0)      # 1 V
    lockin.set_time_constant(9)    # 300 ms
    
    x, y = lockin.get_xy()
    r, theta = lockin.get_r_theta()
    print(f"X={x}, Y={y}, R={r}, θ={theta}°")
```

### 3. Zurich Instruments

```python
from instruments import ZurichInstrument

# Connect and configure Zurich device
with ZurichInstrument("dev1234") as zi:
    zi.set_oscillator_frequency(0, 1000.0)
    zi.set_signal_output_amplitude(0, 0.5)
    zi.enable_signal_output(0, True)
    
    sample = zi.get_demod_sample(0)
    print(f"R={sample['r']}, θ={sample['theta']}°")
```

## Finding Your Instrument

### GPIB/VISA Instruments

```python
import pyvisa

rm = pyvisa.ResourceManager()
print(rm.list_resources())
# Example output: ('GPIB0::8::INSTR', 'GPIB0::24::INSTR')
```

### Zurich Instruments

1. Start LabOne software
2. Check the Web Server interface at http://localhost:8006
3. Note the device ID (e.g., 'dev1234')

## Troubleshooting

- **VISA not found**: Install backend with `pip install pyvisa-py`
- **Cannot connect**: Check instrument is on and cables are connected
- **Timeout errors**: Increase timeout or check for conflicting software
- **Zurich connection fails**: Ensure LabOne Data Server is running

## More Examples

See the `examples/` directory for complete usage examples:
- `keithley_example.py` - IV sweeps, current source mode
- `sr830_example.py` - Frequency sweeps, auto-phase/gain
- `zurich_example.py` - Advanced parameter control

## Documentation

Full API documentation is available in README.md
