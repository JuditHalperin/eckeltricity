import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_monthly_consumption(monthly: pd.DataFrame, output_dir: str):
    plt.figure(figsize=(8, 5))
    plt.plot(monthly.index, monthly['consumption'], marker='o', linewidth=2)

    plt.title('Monthly Electricity Consumption')
    plt.ylabel('Total kWh')
    plt.ylim(0, monthly['consumption'].max() * 1.1)
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/monthly_consumption.png')
    plt.close()


def plot_monthly_plan_comparison(monthly: pd.DataFrame, output_dir: str):
    plt.figure(figsize=(10, 5))
    monthly.plot(kind='bar', ax=plt.gca())
    plt.title('Monthly Plans Comparison')
    plt.ylabel('Total energy cost units')
    plt.xticks(rotation=45, ha='right')
    plt.grid(alpha=0.3)
    plt.legend(title='Plan')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/monthly_plans.png')
    plt.close()


def plot_monthly_plan_heatmap(monthly: pd.DataFrame, output_dir: str):
    plans = [c for c in monthly.columns if 'plan' in c]
    data_vals = monthly[plans].T.values
    plt.figure(figsize=(10, 4))
    plt.imshow(np.ones_like(data_vals), cmap='Greys', alpha=0) 
    plt.imshow(np.zeros_like(data_vals), cmap='gray', alpha=0) 
    plt.imshow(np.ones_like(data_vals), alpha=0)             

    for i, plan in enumerate(plans):
        for j, month in enumerate(monthly.index):
            color = '#e74c3c' if monthly[plans].idxmin(axis=1)[month] == plan else '#d0d0d0'
            plt.gca().add_patch(plt.Rectangle((j-0.5, i-0.5), 1, 1, color=color))
            plt.text(j, i, f'{monthly.loc[month, plan]:.0f}', ha='center', va='center', fontsize=9)

    plt.yticks(range(len(plans)), [p.replace('_',' ').title() for p in plans])
    plt.xticks(range(len(monthly.index)), monthly.index, rotation=45, ha='right')
    plt.title('Best Plan per Month')
    plt.ylabel(' ')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/monthly_plans_heatmap.png')
    plt.close()


def plot_mean_hourly_consumption(data: pd.DataFrame, work_at_office_days: list[int] | None = None, work_at_home_days: list[int] | None = None, output_dir: str = '.'):
    DAY_GROUPS = {
        'Friday': [4],  # Friday
        'Shabbat': [5]  # Saturday
    }
    if work_at_office_days is not None:
        DAY_GROUPS['Work-at-Office'] = work_at_office_days
    if work_at_home_days is not None:
        DAY_GROUPS['Work-at-Home'] = work_at_home_days
    
    plt.figure(figsize=(8, 5))
    for day, idxs in DAY_GROUPS.items():
        daily_data = data[data.index.weekday.isin(idxs)]
        hourly_mean = daily_data['consumption'].groupby(daily_data.index.hour).mean()
        plt.plot(hourly_mean.index, hourly_mean.values, marker='o', linewidth=2, label=day)
    plt.title('Average Hourly Electricity Consumption')
    plt.xlabel('Hour of Day')
    plt.ylabel('Average kWh')
    plt.xticks(range(0, 24))
    plt.grid(alpha=0.3)
    plt.legend(title='Day Type')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/mean_hourly_consumption.png')
    plt.close()
