import holidays
import pandas as pd

def get_arg_holidays(start_year, end_year):
    # Obtengo los feriados de Argentina para los años especificados
    arg_holidays = holidays.Argentina(years=range(start_year, end_year))
    holiday_dates = set(arg_holidays.keys())
    
    # Creo el DataFrame con las fechas de los feriados
    df_holidays = pd.DataFrame(holiday_dates, columns=['date'])
    
    # Me aseguro que tenga formato date
    df_holidays['date'] = pd.to_datetime(df_holidays['date'])
    
    # Agrego una columna con 1 para utilizar como booleano después.
    df_holidays['holiday'] = 1
    
    df_holidays = df_holidays.sort_values(by='date').reset_index(drop=True)

    return df_holidays
