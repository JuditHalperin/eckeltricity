# Eckeltricity

Analyze household electricity consumption data and compare pricing plans.

> *"They run off eckeltricity, do they?"* — Arthur Weasley

## Usage

```bash
pip install -r requirements.txt
```

```bash
python main.py \
    --input_file path_to_meter_csv \
    --start_date 2025-01-01 \
    --end_date 2026-01-01 \
    --work_at_office_days 0 2 3 \
    --work_at_home_days 6 1 \
    --output_dir output
```
