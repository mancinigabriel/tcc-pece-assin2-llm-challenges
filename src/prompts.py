def zero_shot_prompt(premise, hypothesis):
  return f"""
   Você é um sistema de Reconhecimento de Inferência Textual (RTE) em Português Brasileiro.

    Tarefa:
    Dada uma PREMISSA e uma HIPÓTESE, responda *apenas* com um único caractere:
    - 0 se a hipótese não é inferida da premissa.
    - 1 se a hipótese é logicamente inferida da premissa.

    Regras obrigatórias:
    - NÃO explique.
    - NÃO acrescente texto.
    - NÃO repita o enunciado.
    - NÃO responda nada além de 0 ou 1.

    Premissa: {premise}
    Hipótese: {hypothesis}

    Resposta:
    """