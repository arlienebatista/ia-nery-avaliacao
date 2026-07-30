# Avaliação humana das respostas da Nery

Interface web para juízes humanos avaliarem as respostas do assistente Nery,
com nota de 1 a 5 em três critérios (Acurácia, Clareza e Segurança).

## Arquivos

| arquivo | para que serve |
|---|---|
| `app.py` | a interface Streamlit |
| `armazenamento.py` | grava as respostas no Google Sheets ou em CSV local |
| `questoes.csv` | **os dados avaliados**. Trocar este arquivo troca a avaliação |
| `gerar_csv.py` | regenera o `questoes.csv` a partir da planilha original |
| `INSTRUCOES_CSV.md` | como editar o `questoes.csv` |
| `DEPLOY.md` | como publicar na web e configurar o Google Sheets |
| `resultados/respostas.csv` | criado sozinho quando não há Google Sheets configurado |

## Como rodar no seu computador

Uma vez só, para instalar as dependências:

```bash
pip3 install -r requirements.txt
```

Depois, sempre que quiser abrir:

```bash
streamlit run app.py
```

O navegador abre em `http://localhost:8501`. Para outra pessoa avaliar, ela
precisa estar na mesma máquina, ou o app precisa estar publicado (veja
`DEPLOY.md`).

## Como funciona a avaliação

1. O juiz informa um **código** (por exemplo `J1`). Não há nome nem login: o
   código serve só para agrupar as respostas e permitir retomar depois.
2. Uma questão por tela, na ordem do `questoes.csv`. Em cada uma, a resposta da
   Nery aparece ao lado dos trechos dos manuais que o sistema recuperou.
3. As três notas são obrigatórias. Se alguma for 1 ou 2, aparece um campo de
   justificativa obrigatório. O comentário por questão é opcional.
4. Quando a questão não tem trecho recuperado, a Acurácia ganha a opção
   **"Não se aplica"**.
5. Ao final, um comentário geral opcional e o envio.

O `perfil` de quem fez a pergunta não é mostrado ao juiz, mas vai gravado junto
de cada resposta, para você poder analisar por perfil depois.

## Onde ficam as respostas

Cada questão concluída vira uma linha, gravada na hora. Se o juiz fechar a aba,
nada se perde: ele volta com o mesmo código e continua de onde parou.

Colunas gravadas:

`timestamp`, `codigo_juiz`, `id_pergunta`, `perfil`, `acuracia`, `clareza`,
`seguranca`, `justificativa`, `comentario`, `comentario_geral`

A linha com `id_pergunta = _GERAL_` é o comentário final do juiz, e a presença
dela indica que aquele juiz concluiu a avaliação.

A gravação é append-only: se o juiz voltar e mudar uma nota, entra uma linha
nova. Na análise, vale **a última linha de cada par (codigo_juiz, id_pergunta)**.

O destino é escolhido sozinho: Google Sheets se a credencial estiver configurada
(veja `DEPLOY.md`), senão `resultados/respostas.csv`. A barra lateral do app
mostra qual dos dois está em uso.

## Atualizar as questões avaliadas

Edite o `questoes.csv` e recarregue a página. Não precisa mexer em código.
Detalhes em `INSTRUCOES_CSV.md`.

Se a planilha original (`Avaliacao_Humano_Juiz.xlsx`) mudar e você quiser
recomeçar do zero:

```bash
python3 gerar_csv.py
```

Atenção: isso sobrescreve o `questoes.csv`, inclusive correções feitas à mão.
