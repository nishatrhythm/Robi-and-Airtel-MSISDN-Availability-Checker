# Robi and Airtel MSISDN Availability Checker

This repository contains scripts for checking the availability of Robi and Airtel MSISDN numbers. It supports concurrent requests, retry mechanisms, and logging of available numbers into timestamped files.

## Features
- **Concurrent Requests:** Speeds up processing with multi-threading.
- **Retry Mechanism:** Handles failed requests with automatic retries.
- **Customizable Fixed Digits:** Allows fixing specific digits in the number generation process.
- **Dynamic Logging:** Saves results with timestamps for better tracking.
- **Color-Coded Output:** Uses colorama for easier identification of results.

---

## Scripts
### 1. `script_robi.py`
- **Purpose:** Checks MSISDN availability for Robi numbers.
- **Base Prefix:** `8801886`
- **Custom Fixed Digits:** Allows defining specific positions for fixed digits in the number.
- **File Output:** Results saved as `available_numbers_robi_YYYYMMDD_HHMMSS.txt`

### 2. `script_airtel.py`
- **Purpose:** Checks MSISDN availability for Airtel numbers.
- **Base Prefix:** `8801601`
- **Custom Fixed Digits:** Allows defining specific positions for fixed digits in the number.
- **File Output:** Results saved as `available_numbers_airtel_YYYYMMDD_HHMMSS.txt`

---

## Requirements
- Python 3.8 or higher
- Libraries:
  - `requests`
  - `colorama`

### Install Dependencies
```bash
pip install requests colorama
```

---

## Usage
### For Robi Numbers:
```bash
python script_robi.py
```

### For Airtel Numbers:
```bash
python script_airtel.py
```

---

## Configuration
1. **Fixed Digits:**
   - Open the script and modify the `fixed_positions` dictionary.
   - Example:
     ```python
     fixed_positions = {
         0: 8,    # Fix first digit to 8
         1: 6     # Fix second digit to 6
     }
     ```
2. **Number of Workers:**
   - Adjust `max_workers` for concurrency.
   - Example:
     ```python
     checker.run(max_workers=10)
     ```

---

## Output
- Available numbers are saved in timestamped text files:
  - `available_numbers_robi_YYYYMMDD_HHMMSS.txt`
  - `available_numbers_airtel_YYYYMMDD_HHMMSS.txt`

---

## License
This project is licensed under the MIT License.