import numpy as np
import pandas as pd

def calculate_accuracy(df):
  """
  Calculates the accuracy between a prediction column and a reference column in a DataFrame.

  Args:
    df (pd.DataFrame): The input DataFrame.

  Returns:
    float: The accuracy score, or 0 if the DataFrame is empty.
  """
  if df.empty:
    return 0.0
  
  correct_predictions = (df['entailment_judgment'] == df['pred_tratado']).sum()
  total_predictions = len(df)
  accuracy = correct_predictions / total_predictions
  return accuracy


def consistency_per_row(row, cols):
    """
    Calcula a consistência de um exemplo com base nas colunas de teste.
    
    Consistência = fração de previsões iguais ao valor majoritário.
    """
    values = row[cols].dropna().values
    if len(values) == 0:
        return np.nan

    counts = pd.Series(values).value_counts()
    majority_count = counts.iloc[0]

    return majority_count / len(values)


def compute_consistency(df, test_cols=None):
    """
    Calcula métricas de consistência para múltiplas execuções do modelo.
    
    Retorna:
    - DataFrame com consistência por exemplo
    - Consistência média global
    """
    if test_cols is None:
        test_cols = [f"test_{i}_tratado" for i in range(5)]

    df = df.copy()

    df["consistency"] = df.apply(
        consistency_per_row,
        axis=1,
        cols=test_cols
    )

    summary = {
        "mean_consistency": df["consistency"].mean(),
        "std_consistency": df["consistency"].std(),
        "min_consistency": df["consistency"].min(),
        "max_consistency": df["consistency"].max()
    }

    return summary