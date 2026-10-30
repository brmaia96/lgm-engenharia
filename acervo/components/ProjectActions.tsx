"use client";
import { useRouter } from "next/navigation";
import { useState } from "react";

async function call(url: string, method: string, body?: unknown) {
  const res = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error ?? `Erro ${res.status}`);
  return data;
}

export function RestoreButton({ code, compact }: { code: string; compact?: boolean }) {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  return (
    <button
      className={compact ? "chip" : "btn primary"}
      disabled={busy}
      onClick={async () => {
        setBusy(true);
        try {
          await call(`/api/projetos/${code}/restaurar`, "POST");
          router.refresh();
        } catch (e) {
          alert((e as Error).message);
        }
        setBusy(false);
      }}
    >
      {busy ? "Restaurando…" : "Restaurar"}
    </button>
  );
}

export function DeleteButton({ code }: { code: string }) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [motivo, setMotivo] = useState("");
  const [busy, setBusy] = useState(false);
  return (
    <>
      <button type="button" className="btn danger" onClick={() => setOpen(true)}>Excluir projeto</button>
      {open && (
        <div className="modal" role="dialog" aria-modal="true" onClick={(e) => e.target === e.currentTarget && setOpen(false)}>
          <div className="modal-box">
            <h3>Mover {code} para a lixeira?</h3>
            <p>Ele sai do acervo, mas fica na lixeira e pode ser restaurado a qualquer momento.</p>
            <label className="field">
              <span>Motivo (opcional)</span>
              <input value={motivo} onChange={(e) => setMotivo(e.target.value)} placeholder="ex.: era só orçamento" maxLength={200} />
            </label>
            <div className="modal-actions">
              <button className="btn" onClick={() => setOpen(false)}>Cancelar</button>
              <button
                className="btn danger solid"
                disabled={busy}
                onClick={async () => {
                  setBusy(true);
                  try {
                    await call(`/api/projetos/${code}`, "DELETE", { motivo });
                    router.push("/lixeira");
                    router.refresh();
                  } catch (e) {
                    alert((e as Error).message);
                    setBusy(false);
                  }
                }}
              >
                {busy ? "Excluindo…" : "Mover para a lixeira"}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export { call };
