# Render ultra realista do Chalé Analândia (tarefa para uma sessão no computador)

Esta tarefa precisa do Chrome do cliente, com o ChatGPT (ou o Gemini) já logado.
Não usar API paga: o cliente quer usar só as assinaturas que já tem.

## O que fazer

1. Com a extensão Claude in Chrome conectada, abrir uma conversa nova no ChatGPT.
2. Anexar `base/analandia-1-frente.jpg` e enviar o texto de `PROMPT.txt` (a parte
   que começa em "Transforme este render").
3. Na mesma conversa, anexar cada uma das outras cinco imagens de `base/`, na
   ordem, com a frase: "Agora esta vista. Mesmas regras, mesmos materiais e mesma
   luz da imagem anterior."
4. Baixar cada resultado e salvar em `ia/` com o mesmo nome da imagem-base.
5. Conferir cada resultado contra a imagem-base antes de aceitar. Recusar e gerar
   de novo se houver qualquer um destes erros:
   - geometria diferente (inclinação do telhado, volume lateral, aberturas);
   - guarda-corpo, vidro ou escada flutuando ou atravessando o telhado;
   - elemento que muda de uma vista para outra (porta, janela, bancada, piscina);
   - árvore, portão ou muro em lugar impossível; pessoas, carros, texto ou marca.
6. Commit e push de `ia/` no branch `claude/dazzling-mccarthy-s9z5h2`.

## Depois

Com as imagens em `ia/`, a sessão que mantém o site troca as seis imagens da
página `o-chale-analandia.html` (com o tratamento de cor padrão do site),
reconstrói, publica e envia. O chalé continua no ar com os renders de `base/`
até lá.
