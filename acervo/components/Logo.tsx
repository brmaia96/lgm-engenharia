// Cobogó "bandeira": moldura + diagonal — metade cheia (terracota), metade vazada.
export function Mark({ size = 32, title }: { size?: number; title?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 96 96" role={title ? "img" : undefined} aria-label={title} aria-hidden={title ? undefined : true}>
      <path
        fill="var(--frame)"
        fillRule="evenodd"
        d="M3 0h90a3 3 0 0 1 3 3v90a3 3 0 0 1-3 3H3a3 3 0 0 1-3-3V3a3 3 0 0 1 3-3Zm11 14v68h68V14Z"
      />
      <path fill="var(--accent)" d="M82 14V82H14Z" />
    </svg>
  );
}

export function Logo() {
  return (
    <span className="brand">
      <Mark size={30} />
      <span className="brand-word">
        <b>COBOGÓ</b>
        <span>ARQUITETURA</span>
      </span>
    </span>
  );
}

/** Painel de cobogós — quatro módulos girados formam o losango; repetido vira parede. */
export function CobogoWall({ cols = 6, rows = 8, seed = 7 }: { cols?: number; rows?: number; seed?: number }) {
  const cells = [];
  let s = seed;
  const rnd = () => ((s = (s * 9301 + 49297) % 233280) / 233280);
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      // padrão losango: a rotação depende do quadrante dentro do bloco 2x2
      const rot = [[0, 90], [270, 180]][y % 2][x % 2];
      const lit = rnd() > 0.82;
      cells.push(
        <g key={`${x}-${y}`} transform={`translate(${x * 100 + 50} ${y * 100 + 50}) rotate(${rot}) translate(-48 -48)`}>
          <path fill="#2b2925" fillRule="evenodd" d="M3 0h90a3 3 0 0 1 3 3v90a3 3 0 0 1-3 3H3a3 3 0 0 1-3-3V3a3 3 0 0 1 3-3Zm11 14v68h68V14Z" />
          <path fill={lit ? "#8a847a" : "#33312d"} d="M82 14V82H14Z" />
        </g>,
      );
    }
  }
  return (
    <svg viewBox={`0 0 ${cols * 100} ${rows * 100}`} preserveAspectRatio="xMidYMid slice" aria-hidden>
      <rect width="100%" height="100%" fill="#141311" />
      {cells}
    </svg>
  );
}
