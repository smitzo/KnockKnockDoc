const PALETTES = [
  ["#dcece4", "#156c63", "#f4c9a7", "#173d3a"],
  ["#e4ebf7", "#3568a9", "#d9a77f", "#243d5c"],
  ["#f5e8d2", "#a9681f", "#8c5d3f", "#4e3528"],
  ["#e9e1f1", "#6e4f8e", "#efc7a1", "#382d48"],
  ["#e2efec", "#2f7b70", "#70462f", "#2e2926"],
];

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ key: string }> },
) {
  const { key } = await params;
  if (!/^(doctor|patient)-\d{2}$/.test(key)) return new Response(null, { status: 404 });
  const number = Number(key.slice(-2));
  const [background, accent, skin, hair] = PALETTES[number % PALETTES.length];
  const isDoctor = key.startsWith("doctor");
  const label = `${isDoctor ? "D" : "P"}${String(number).padStart(2, "0")}`;
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="144" height="144" viewBox="0 0 144 144" role="img" aria-label="Generated synthetic avatar ${label}">
    <rect width="144" height="144" rx="34" fill="${background}"/>
    <circle cx="116" cy="28" r="20" fill="${accent}" opacity=".12"/>
    <path d="M28 137c3-28 20-44 44-44s41 16 44 44" fill="${accent}"/>
    <ellipse cx="72" cy="62" rx="29" ry="34" fill="${skin}"/>
    <path d="M43 62c0-28 13-42 31-42 18 0 30 14 30 38-8-7-16-10-25-12-12 9-23 13-36 12z" fill="${hair}"/>
    <circle cx="61" cy="65" r="2.3" fill="#173d3a"/><circle cx="84" cy="65" r="2.3" fill="#173d3a"/>
    <path d="M64 78c5 4 11 4 16 0" fill="none" stroke="#8f5b4e" stroke-width="2.2" stroke-linecap="round"/>
    ${isDoctor ? '<path d="M55 99l17 20 17-20" fill="#fff" opacity=".94"/><circle cx="72" cy="122" r="4" fill="none" stroke="#fff" stroke-width="2"/>' : '<path d="M52 105c13 8 27 8 40 0" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".8"/>'}
    <rect x="99" y="107" width="33" height="24" rx="12" fill="#fff" opacity=".94"/><text x="115.5" y="123" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" font-weight="700" fill="${accent}">${label}</text>
  </svg>`;
  return new Response(svg, {
    headers: {
      "Content-Type": "image/svg+xml; charset=utf-8",
      "Cache-Control": "public, max-age=31536000, immutable",
      "X-Content-Type-Options": "nosniff",
    },
  });
}
