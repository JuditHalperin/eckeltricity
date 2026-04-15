import os
import argparse
from analysis import read_data, run_analysis
from plots import plot_monthly_consumption, plot_monthly_plan_comparison, plot_monthly_plan_heatmap, plot_mean_hourly_consumption


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input CSV file downloaded from the electricity provider')
    parser.add_argument('--start_date', type=str, default=None, help='Start date for analysis (format: YYYY-MM-DD)')
    parser.add_argument('--end_date', type=str, default=None, help='End date for analysis (format: YYYY-MM-DD)')
    parser.add_argument('--work_at_office_days', type=int, nargs='*', default=None, help='List of weekday numbers (0=Monday, 6=Sunday) for work-at-office days')
    parser.add_argument('--work_at_home_days', type=int, nargs='*', default=None, help='List of weekday numbers (0=Monday, 6=Sunday) for work-at-home days')
    parser.add_argument('--output_dir', type=str, default='.', help='Directory to save the output plots')
    args = parser.parse_args()

    data = read_data(args.input_file, args.start_date, args.end_date)
    monthly_data = run_analysis(data)

    os.makedirs(args.output_dir, exist_ok=True)
    plot_monthly_consumption(monthly_data, args.output_dir)
    plot_monthly_plan_comparison(monthly_data, args.output_dir)
    plot_monthly_plan_heatmap(monthly_data, args.output_dir)
    plot_mean_hourly_consumption(data, work_at_office_days=args.work_at_office_days, work_at_home_days=args.work_at_home_days, output_dir=args.output_dir)


if __name__ == '__main__':
    main()
