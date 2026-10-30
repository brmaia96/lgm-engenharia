import type { NextConfig } from "next";

const csp = [
  "default-src 'self'",
  "script-src 'self' 'unsafe-inline'",
  "style-src 'self' 'unsafe-inline'",
  "img-src 'self' blob: data:",
  "font-src 'self'",
  "connect-src 'self'",
  "frame-ancestors 'none'",
  "base-uri 'self'",
  "form-action 'self'",
  "object-src 'none'",
].join("; ");

const config: NextConfig = {
  poweredByHeader: false,
  reactStrictMode: true,
  // o cofre criptografado precisa acompanhar as funções serverless
  outputFileTracingIncludes: {
    ...Object.fromEntries([..."0123456789abcdef"].map((c) => [`/api/m${c}/[id]/[size]`, [`./vault/media/${c}*`]])),
    "/": ["./vault/catalog.enc"],
    "/p/[code]": ["./vault/catalog.enc"],
    "/p/[code]/editar": ["./vault/catalog.enc"],
    "/lixeira": ["./vault/catalog.enc"],
    "/historico": ["./vault/catalog.enc"],
    "/api/projetos": ["./vault/catalog.enc"],
    "/api/projetos/[code]": ["./vault/catalog.enc"],
    "/api/projetos/[code]/restaurar": ["./vault/catalog.enc"],
  },
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "Content-Security-Policy", value: csp },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "Referrer-Policy", value: "same-origin" },
          { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains" },
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=(), interest-cohort=()" },
          { key: "X-Robots-Tag", value: "noindex, nofollow, noarchive, noimageindex" },
        ],
      },
    ];
  },
};

export default config;
