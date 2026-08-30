const palettes = [
  ["#DDEEE7", "#276B5A", "#163D35", "#F2C7A5"],
  ["#E6ECF8", "#4569A0", "#263D62", "#D8A47F"],
  ["#F6E9D2", "#A96932", "#5B3821", "#E8B692"],
  ["#EDE5F2", "#76558E", "#402E4E", "#C98E6F"],
  ["#E4F0F1", "#34757D", "#1F454A", "#8F5E45"],
] as const;

export async function GET(
  _request: Request,
  context: { params: Promise<{ key: string }> },
) {
  const { key } = await context.params;
  const match = /^(doctor|patient)-(\d{2})$/.exec(key);
  if (!match) return new Response("Not found", { status: 404 });

  const role = match[1];
  const number = Number(match[2]);
  if (number < 1 || number > (role === "doctor" ? 32 : 30)) {
    return new Response("Not found", { status: 404 });
  }

  const [background, clothing, hair, skin] = palettes[(number - 1) % palettes.length];
  const hairPath = number % 3 === 0
    ? "M27 47c1-18 11-27 26-27 17 0 26 10 27 29-7-8-17-12-28-12-10 0-18 3-25 10Z"
    : number % 2 === 0
      ? "M28 47c2-19 12-27 26-27 15 0 24 8 26 25-9-5-18-8-29-8-8 0-16 3-23 10Z"
      : "M27 48c0-19 10-29 27-29 16 0 26 11 26 30-8-9-17-13-28-13-10 0-18 4-25 12Z";
  const accessory = role === "doctor"
    ? '<path d="M40 76v10c0 8 6 14 14 14s14-6 14-14V76" fill="none" stroke="#FFFFFF" stroke-width="3"/><circle cx="68" cy="78" r="4" fill="none" stroke="#FFFFFF" stroke-width="3"/>'
    : '<path d="M37 80c8 5 26 5 34 0" fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round"/>';
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 108 108" role="img" aria-label="Illustrated fictional ${role} avatar">
<rect width="108" height="108" rx="24" fill="${background}"/>
<circle cx="54" cy="49" r="23" fill="${skin}"/>
<path d="${hairPath}" fill="${hair}"/>
<circle cx="46" cy="50" r="2" fill="#263B37"/><circle cx="63" cy="50" r="2" fill="#263B37"/>
<path d="M49 61c3 3 8 3 11 0" fill="none" stroke="#713E31" stroke-width="2" stroke-linecap="round"/>
<path d="M18 108c2-25 15-38 36-38s34 13 36 38H18Z" fill="${clothing}"/>
${accessory}
<circle cx="91" cy="18" r="10" fill="#FFFFFF" opacity=".92"/><path d="M87 18h8M91 14v8" stroke="${clothing}" stroke-width="2.5" stroke-linecap="round"/>
</svg>`;

  return new Response(svg, {
    headers: {
      "Cache-Control": "public, max-age=31536000, immutable",
      "Content-Security-Policy": "default-src 'none'; style-src 'unsafe-inline'",
      "Content-Type": "image/svg+xml; charset=utf-8",
      "X-Content-Type-Options": "nosniff",
    },
  });
}
