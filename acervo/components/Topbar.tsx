import Link from "next/link";
import { Logo } from "./Logo";
import { ThemeToggle } from "./ThemeToggle";

export function Topbar({ user, active }: { user: string; active?: "acervo" | "padrao" }) {
  return (
    <header className="topbar">
      <div className="wrap">
        <Link href="/" aria-label="Início"><Logo /></Link>
        <nav className="nav">
          <Link href="/" aria-current={active === "acervo" ? "page" : undefined}>Acervo</Link>
          <Link href="/padrao" aria-current={active === "padrao" ? "page" : undefined}>Padrão</Link>
        </nav>
        <div className="top-right">
          <ThemeToggle />
          <span className="user-chip"><span>{user}</span><i>{user.slice(0, 1).toUpperCase()}</i></span>
          <form action="/api/auth/logout" method="post">
            <button className="icon-btn" title="Sair" aria-label="Sair">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M15 4h3a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-3M10 17l5-5-5-5M15 12H3" /></svg>
            </button>
          </form>
        </div>
      </div>
    </header>
  );
}
