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
