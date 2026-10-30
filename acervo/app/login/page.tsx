import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { CobogoWall, Logo } from "@/components/Logo";
import { currentUser } from "@/lib/auth";
import { LoginForm } from "./LoginForm";

export const metadata: Metadata = { title: "Entrar" };

export default async function LoginPage(props: PageProps<"/login">) {
  if (await currentUser()) redirect("/");
  const { next } = await props.searchParams;
  const dest = typeof next === "string" && next.startsWith("/") && !next.startsWith("//") ? next : "/";
  return (
    <main className="login">
      <div className="login-art">
        <CobogoWall />
        <div className="tag">
          <span className="eyebrow">Uso interno · acesso restrito</span>
          <div className="display">Acervo<br /><em>de projetos</em></div>
          <p>Plantas, layouts, interiores e fachadas de todos os projetos do escritório, num só lugar.</p>
        </div>
      </div>
      <div className="login-panel">
        <Logo />
        <div>
          <p className="eyebrow accent">Bem-vindo</p>
          <h1>Entrar</h1>
        </div>
        <LoginForm next={dest} />
        <p className="login-foot">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="4" y="10" width="16" height="11" rx="2" /><path d="M8 10V7a4 4 0 0 1 8 0v3" /></svg>
          Conexão criptografada · acervo cifrado em AES-256 · uso interno
        </p>
      </div>
    </main>
  );
}
