"use client";
import { useState } from "react";

export function CopyButton({ text }: { text: string }) {
  const [ok, setOk] = useState(false);
  return (
    <button
      onClick={async () => {
        try {
          await navigator.clipboard.writeText(text);
          setOk(true);
          setTimeout(() => setOk(false), 1600);
        } catch {}
      }}
    >
      {ok ? "copiado" : "copiar"}
    </button>
  );
}
