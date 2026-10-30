"use client";

export function ThemeToggle() {
  function toggle() {
    const root = document.documentElement;
    const dark = root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    root.dataset.theme = dark ? "light" : "dark";
    try { localStorage.setItem("cb-theme", root.dataset.theme); } catch {}
  }
  return (
    <button className="icon-btn" onClick={toggle} title="Claro / escuro" aria-label="Alternar tema claro/escuro">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><circle cx="12" cy="12" r="8" /><path d="M12 4v16" /><path d="M12 4a8 8 0 0 1 0 16Z" fill="currentColor" /></svg>
    </button>
  );
}
