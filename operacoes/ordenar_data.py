import pandas as pd

def _convertDia(value: str) -> int:
    return int(value.split('/')[1])*100 + int(value.split('/')[0])

def ordenar_porData(df: pd.DataFrame) -> pd.DataFrame:
    df['Data'] = df['Dia']
    df['Data'] = df['Data'].apply(_convertDia)

    df_sorted = df.sort_values(by='Data', ascending=True)
    df_sorted = df_sorted.drop('Data', axis=1)
    return df_sorted