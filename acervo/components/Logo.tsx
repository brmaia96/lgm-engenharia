// Cobogó "bandeira": moldura fina + diagonal — metade cheia, metade vazada.
const FRAME = "M0 0h96v96H0Zm7 7v82h82V7Z";
const HALF = "M82 14V82H14Z";

export function Mark({ size = 28, title }: { size?: number; title?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 96 96" role={title ? "img" : undefined} aria-label={title} aria-hidden={title ? undefined : true}>
      <path fill="currentColor" fillRule="evenodd" d={FRAME} />
      <path fill="currentColor" d={HALF} />
    </svg>
  );
}

export function Logo() {
  return (
    <span className="brand">
      <Mark size={26} />
      <span className="brand-word">
        <b>Cobogó</b>
        <span>ACERVO DE ARQUITETURA</span>
      </span>
    </span>
  );
}

/** Parede de cobogós em relevo, tom sobre tom — quatro módulos girados formam o losango. */
export function CobogoWall({ cols = 7, rows = 9 }: { cols?: number; rows?: number }) {
  const cells = [];
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < cols; x++) {
      const rot = [[0, 90], [270, 180]][y % 2][x % 2];
      cells.push(
        <g key={`${x}-${y}`} transform={`translate(${x * 100 + 50} ${y * 100 + 50}) rotate(${rot}) translate(-48 -48)`}>
          <path fill="#221e1a" fillRule="evenodd" d={FRAME} />
          <path fill="#1c1916" d={HALF} />
          <path fill="none" stroke="#2c2722" strokeWidth="1" d="M14 82L82 14" />
        </g>,
      );
    }
  }
  return (
    <svg viewBox={`0 0 ${cols * 100} ${rows * 100}`} preserveAspectRatio="xMidYMid slice" aria-hidden>
      <rect width="100%" height="100%" fill="#141210" />
      {cells}
      <defs>
        <linearGradient id="fadeWall" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#141210" stopOpacity="0" />
          <stop offset="1" stopColor="#141210" stopOpacity=".92" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#fadeWall)" />
    </svg>
  );
}
