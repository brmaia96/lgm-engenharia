# Gerador do site L. Engenharia

`site/` é a saída pronta para hospedar. Esta pasta guarda o que gera essa saída.

- `data.py` — conteúdo de cada projeto: nome, cidade, texto, ficha técnica, galeria.
- `static_pages.py` — páginas de INSS e Sobre.
- `build.py` — monta as páginas e trata as imagens.
- `grade.py` — padrão de imagem (cor graduada, tinta sobre papel, modelo em fundo escuro, capa em duotone).
- `portrait.py` — retrato: mantém a pessoa e troca o fundo por estúdio liso.
- `styles.css`, `site.js` — estilo e comportamento (comparador, filtro, galeria, vídeo).
- `video/film.html` + `video/cap.js` — vídeo de apresentação, renderizado quadro a quadro e codificado com ffmpeg.
- `recife_block.txt` e `data_com_recife.py` — projeto de Recife, fora do ar até o cliente confirmar. Reativação testada: `SITE_DATA=data_com_recife.py` gera as 11 páginas.

As imagens de origem (renders limpos por projeto) não estão no repositório: vêm
do Drive do cliente. Os caminhos em `build.py` apontam para a pasta de trabalho
usada na geração; ajuste `S` antes de rodar em outra máquina.

## Novembro de 2026: básico, direto e real

Regra do cliente: texto básico e direto, sem entregar o passo a passo; fonte só pelo título; obras com o mínimo;
imagem de projeto real, que siga o projeto. Detalhes no `CLAUDE.md` da raiz.

- `inss_page.py`: página de INSS (cálculo breve, calculadora por estado, formulário de contato, mapa com contadores,
  sistemas, perguntas). Fonte única dos números que a home repete.
- `vau_uf.json`: VAU de cada estado, residencial unifamiliar, com o mês de referência. **Atualizar todo mês.**
- `brasil.json`: contorno do Brasil e posição das cidades do mapa.
- `blog.py`: artigos do blog, em versão curta.
- `data.py`: os projetos completos e, no fim, a camada `LEAN`/`HELD`, que escolhe o que vai ao ar.
- `arquivo/`: versões longas e conferidas da página de INSS e do blog. Só para consulta, não voltam ao ar.
- `video/`: filme da home. `node cap.js` grava todos os quadros; `node cap_range.js 300 590` regrava só um trecho;
  `python3 musica.py` gera a trilha; ffmpeg junta quadros e áudio.
- `test_inss.js`: teste da calculadora e do formulário (`node test_inss.js <pasta do site>`).
