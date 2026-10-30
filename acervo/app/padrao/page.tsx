import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { NameBuilder } from "@/components/NameBuilder";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";

export const metadata: Metadata = { title: "Padrão" };

export default async function Padrao() {
  const user = await currentUser();
  if (!user) redirect("/login");
  return (
    <>
      <Topbar user={user} active="padrao" />
      <main className="wrap">
        <article className="doc">
          <div>
            <p className="eyebrow">Como o acervo se organiza</p>
            <h1 className="display">Padrão<br />de nomes</h1>
          </div>

          <section>
            <h2>01 · Gerador</h2>
            <NameBuilder />
          </section>

          <section>
            <h2>02 · Legenda</h2>
            <div className="legend">
              <code>ARQ</code><span>Disciplina — arquitetura</span>
              <code>R H C I M</code><span>Tipo — Residencial, Hospedagem/chalé, Comercial, Institucional, Misto</span>
              <code>15X20</code><span>Terreno frente × fundo em metros. <b>ND</b> = não definido / a confirmar (também em área e suítes)</span>
              <code>T TM S 3P SS</code><span>Pavimentos — Térreo, Térreo + mezanino, Sobrado, 3 pavimentos, com Subsolo</span>
              <code>150M2</code><span>Área total construída</span>
              <code>3SUITES</code><span>Quantidade de suítes (1SUITE no singular, 0SUITES quando não há)</span>
              <code>CB001</code><span>Código curto sequencial — único, nunca muda nem é reaproveitado. Use para falar do projeto: “manda o CB014”</span>
            </div>
          </section>

          <section>
            <h2>03 · Regras de privacidade</h2>
            <ul>
              <li>Nunca usar nome de cliente — nem no título, nem em legenda, nem no nome do arquivo.</li>
              <li>Pranchas com carimbo: cortar o carimbo antes de subir (o carimbo traz nome e endereço).</li>
              <li>O título é descritivo: “Casa térrea em L com piscina”, “Chalé com mezanino”.</li>
              <li>Os metadados das fotos (GPS, autor, software) são apagados automaticamente na entrada.</li>
            </ul>
          </section>

          <section>
            <h2>04 · Como incluir um projeto novo</h2>
            <ol>
              <li>Crie uma pasta em <code>acervo/incoming/</code> com as subpastas abaixo e o <code>projeto.json</code> (use o gerador acima).</li>
              <li>Rode <code>npm run acervo:add -- incoming/sua-pasta</code> — as imagens são otimizadas, criptografadas e o código CB é gerado.</li>
              <li>Faça commit da pasta <code>vault/</code> e push. O site atualiza sozinho em ~1 minuto.</li>
            </ol>
            <pre className="tree" style={{ marginTop: 16 }}>{`incoming/casa-nova/
├── projeto.json
├── fachada/      01.jpg  02.jpg  capa.jpg   ← "capa" vira a imagem principal
├── interna/      sala.jpg  cozinha.jpg  suite.jpg
├── planta/       planta-baixa.pdf           ← PDF vira imagem automaticamente
├── layout/       planta-humanizada.png
└── implantacao/  (opcional: cobertura/ corte/ outros/)`}</pre>
          </section>
        </article>
      </main>
    </>
  );
}
