# Como atualizar as questões da avaliação

Tudo que os juízes veem vem de um único arquivo: **`questoes.csv`**. Para trocar
uma pergunta, corrigir uma resposta da Nery ou completar um trecho de manual,
basta editar esse arquivo e recarregar a página do app. Nenhum código muda.

## As cinco colunas

| coluna | conteúdo | obrigatória |
|---|---|---|
| `id_pergunta` | identificador curto e único, como `P1-03`. É por ele que as respostas dos juízes são reconhecidas | sim |
| `perfil` | perfil de quem faz a pergunta (por exemplo `mulher idosa`, `homem jovem`). **Não aparece para o juiz**, só é registrado nos resultados | não |
| `pergunta` | a pergunta do cuidador, como ela chega à Nery | sim |
| `resposta` | a resposta gerada pela Nery, que será avaliada | sim |
| `gabarito` | os trechos dos manuais oficiais que o sistema recuperou | não |

A ordem das linhas no arquivo é a ordem em que as questões aparecem para o juiz.

## O campo `gabarito`

Este é o único campo com uma regra especial. Quando a recuperação trouxe mais de
um trecho, separe os trechos por uma linha contendo apenas três hifens:

```
Texto do primeiro trecho do manual.
---
Texto do segundo trecho do manual.
---
Texto do terceiro trecho.
```

O app exibe isso como "Trecho 1 de 3", "Trecho 2 de 3" e assim por diante. Se
você colar um texto sem nenhum `---`, ele mostra tudo como um trecho só, e
funciona igual.

**Quando o sistema não recuperou nada**, deixe a célula vazia ou escreva
`Não encontrou`. Nesse caso o app avisa o juiz e libera a opção
"Não se aplica" no critério de Acurácia, já que não há material com o que
comparar a resposta.

## Trechos truncados

Cinco questões vieram da planilha original com o trecho cortado no meio, porque
o processo que gerou a planilha limitou o texto. Elas estão marcadas assim, no
fim do campo:

```
[TRECHO TRUNCADO NA PLANILHA ORIGINAL: completar]
```

São as questões **P1-04, P2-12, P2-14, P3-19 e P3-20**. Para corrigir, cole o
trecho completo vindo do pipeline de recuperação e apague essa marca. Enquanto a
marca estiver lá, o juiz vê que aquele trecho está incompleto, o que é melhor do
que ele avaliar fidelidade contra um texto cortado sem saber.

## Editando no Excel ou no Google Sheets

**Excel:** abra o `questoes.csv`, edite e salve em
`Arquivo > Salvar como > CSV UTF-8 (delimitado por vírgula)`. É importante ser a
opção **UTF-8**, senão os acentos quebram. O Excel pode avisar que o formato não
suporta várias planilhas: pode confirmar.

**Google Sheets:** `Arquivo > Importar > Fazer upload`, edite, e depois
`Arquivo > Fazer download > Valores separados por vírgula (.csv)`. Renomeie o
arquivo baixado para `questoes.csv` e coloque no lugar do antigo.

Nos dois casos, para escrever várias linhas dentro de uma mesma célula (o caso
dos trechos separados por `---`), use `Alt+Enter` no Excel ou `Ctrl+Enter` no
Google Sheets. Não aperte só Enter, senão vira outra questão.

## Depois de editar

Salve o arquivo e recarregue a página do app no navegador. As mudanças aparecem
na hora, sem reiniciar nada.

Se você mudar o `id_pergunta` de uma questão já avaliada por alguém, o app
passa a tratá-la como uma questão nova, e as respostas antigas ficam órfãs na
planilha de resultados. Mudar o texto sem mexer no id é seguro.
