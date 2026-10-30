import Link from "next/link";
import { Mark } from "@/components/Logo";

export default function NotFound() {
  return (
    <main className="empty" style={{ minHeight: "80dvh", alignContent: "center" }}>
      <Mark size={56} />
      <p>Projeto não encontrado.</p>
      <Link className="btn" href="/">Voltar ao acervo</Link>
    </main>
  );
}
