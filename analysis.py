import pandas as pd


BASIC_SAVE = 0.06
NIGHT_SAVE = 0.20
DAY_SAVE = 0.15


is_not_weekend = lambda time: time.weekday() in [6, 0, 1, 2, 3]  # Sunday-Thursday
basic_factor = lambda time: (1 - BASIC_SAVE)
night_factor = lambda time: (1 - NIGHT_SAVE) if (is_not_weekend(time) and (time.hour >= 23 or time.hour <= 7)) else 1
day_factor = lambda time: (1 - DAY_SAVE) if (is_not_weekend(time) and (7 <= time.hour <= 17)) else 1


def read_data(input_file: str, start_date: str | None = None, end_date: str | None = None) -> pd.DataFrame:
    try:
        data = pd.read_csv(input_file, skiprows=12, names=['code', 'type', 'date', 'time', 'consumption', 'flow'], usecols=[0, 1, 2, 3, 4, 5])
        data = data.drop(columns=['code', 'type', 'flow'])
    except:
        data = pd.read_csv(input_file, skiprows=12, names=['date', 'time', 'consumption'], usecols=[0, 1, 2])

    data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'], format='%d/%m/%Y %H:%M')
    data = data.set_index('datetime').drop(columns=['date', 'time'])
    assert all(data.resample('15min').mean().interpolate() == data)
    start_day = pd.to_datetime(start_date).replace(hour=0, minute=0) if start_date else data.index.min()
    end_day = pd.to_datetime(end_date).replace(hour=23, minute=59) if end_date else data.index.max()
    data = data[(data.index >= start_day) & (data.index <= end_day)]
    return data


def run_analysis(data: pd.DataFrame) -> pd.DataFrame:
    data['basic_plan'] = data['consumption'] * data.index.map(basic_factor)
    data['night_plan'] = data['consumption'] * data.index.map(night_factor)
    data['day_plan'] = data['consumption'] * data.index.map(day_factor)

    print(data.sum().round().astype(int))

    monthly = data.resample('ME').sum()
    monthly.index = monthly.index.strftime('%b %Y')
    return monthly
