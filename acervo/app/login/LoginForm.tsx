"use client";
import { useState } from "react";

export function LoginForm({ next }: { next: string }) {
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError("");
    const fd = new FormData(e.currentTarget);
    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user: fd.get("user"), password: fd.get("password") }),
      });
      if (res.ok) {
        window.location.assign(next);
        return;
      }
      const data = await res.json().catch(() => ({}));
      setError(data.error ?? "Não foi possível entrar.");
    } catch {
      setError("Sem conexão. Tente de novo.");
    }
    setBusy(false);
  }

  return (
    <form onSubmit={onSubmit}>
      <div className="line-field">
        <label htmlFor="user">Usuário</label>
        <input id="user" name="user" autoComplete="username" autoCapitalize="none" spellCheck={false} required />
      </div>
      <div className="line-field">
        <label htmlFor="password">Senha</label>
        <input id="password" name="password" type="password" autoComplete="current-password" required />
      </div>
      <p className="form-error" role="alert">{error}</p>
      <button className="btn primary" disabled={busy}>{busy ? "Entrando…" : "Entrar"}</button>
    </form>
  );
}
