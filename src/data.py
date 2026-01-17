import pandas as pd

def gera_df():

  splits = {'train': 'data/train-00000-of-00001.parquet', 'test': 'data/test-00000-of-00001.parquet', 'validation': 'data/validation-00000-of-00001.parquet'}
  df_assin_2_treino = pd.read_parquet("hf://datasets/nilc-nlp/assin2/" + splits["train"])
  df_assin_2_teste = pd.read_parquet("hf://datasets/nilc-nlp/assin2/" + splits["test"])
  df_assin_2_val = pd.read_parquet("hf://datasets/nilc-nlp/assin2/" + splits["validation"])

  df_assin_2 = pd.concat([df_assin_2_treino, df_assin_2_teste, df_assin_2_val])

  df_assin_2['premise_hypothesis'] = df_assin_2['premise'] + ' ' + df_assin_2['hypothesis']

  occurrence_counts = df_assin_2['premise_hypothesis'].value_counts().reset_index()
  occurrence_counts.columns = ['premise_hypothesis', 'occurrence_count']

  df_assin_2 = df_assin_2.merge(occurrence_counts, on='premise_hypothesis', how='left')

  df_assin_2 = df_assin_2.loc[df_assin_2['occurrence_count'] == 1]

  df_assin_2 = df_assin_2[['sentence_pair_id', 'premise', 'hypothesis', 'relatedness_score',
        'entailment_judgment']]

  df_assin_2.reset_index(drop=True, inplace=True)

  return df_assin_2


def load_dados_acarretamento_sinteticos():
  
  df = pd.read_json("dados_acarretamento_sinteticos.json")
  df['rotulo'] = df['rotulo'].map({'acarretamento': 1, 'não_acarretamento': 0})

  return df