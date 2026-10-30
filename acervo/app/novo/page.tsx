import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { NewProject } from "@/components/NewProject";
import { Topbar } from "@/components/Topbar";
import { currentUser } from "@/lib/auth";
import { storeMode } from "@/lib/store";

export const metadata: Metadata = { title: "Novo projeto" };
export const dynamic = "force-dynamic";

export default async function Novo() {
  const user = await currentUser();
  if (!user) redirect("/login");
  return (
    <>
      <Topbar user={user} active="novo" />
      {storeMode() === "readonly" ? (
        <main className="wrap doc"><p>Para adicionar projetos pelo site, falta ativar o armazenamento (Vercel → Storage → Blob).</p></main>
      ) : (
        <NewProject />
      )}
    </>
  );
}
