import "server-only";

import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";

export interface ArticleSource {
  publisher: string;
  title: string;
  url: string;
  supports: string;
}

export interface ArticleSection {
  heading: string;
  paragraphs: string[];
  bullets?: string[];
}

export interface BlogArticle {
  order: number;
  slug: string;
  category: string;
  title: string;
  dek: string;
  readMinutes: number;
  reviewed: string;
  image: string;
  imageAlt: string;
  keyNumber?: { value: string; label: string };
  sections: ArticleSection[];
  sources: ArticleSource[];
}

const contentDirectory = path.join(process.cwd(), "content", "blog");
let cachedArticles: readonly BlogArticle[] | undefined;

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function requiredString(record: Record<string, unknown>, key: string, fileName: string) {
  const value = record[key];
  if (typeof value !== "string" || value.trim() === "") {
    throw new Error(`Blog content ${fileName} requires a non-empty "${key}" string.`);
  }
  return value;
}

function requiredStringArray(record: Record<string, unknown>, key: string, fileName: string) {
  const value = record[key];
  if (!Array.isArray(value) || value.length === 0 || value.some((entry) => typeof entry !== "string" || entry.trim() === "")) {
    throw new Error(`Blog content ${fileName} requires a non-empty "${key}" string array.`);
  }
  return value as string[];
}

function parseSource(value: unknown, fileName: string): ArticleSource {
  if (!isRecord(value)) throw new Error(`Blog content ${fileName} contains an invalid source.`);
  const url = requiredString(value, "url", fileName);
  const parsedUrl = new URL(url);
  if (parsedUrl.protocol !== "https:") throw new Error(`Blog source URLs must use HTTPS in ${fileName}.`);
  return {
    publisher: requiredString(value, "publisher", fileName),
    title: requiredString(value, "title", fileName),
    url,
    supports: requiredString(value, "supports", fileName),
  };
}

function parseSection(value: unknown, fileName: string): ArticleSection {
  if (!isRecord(value)) throw new Error(`Blog content ${fileName} contains an invalid section.`);
  const bullets = value.bullets === undefined ? undefined : requiredStringArray(value, "bullets", fileName);
  return {
    heading: requiredString(value, "heading", fileName),
    paragraphs: requiredStringArray(value, "paragraphs", fileName),
    ...(bullets ? { bullets } : {}),
  };
}

function parseArticle(raw: unknown, fileName: string): BlogArticle {
  if (!isRecord(raw)) throw new Error(`Blog content ${fileName} must be a JSON object.`);
  const order = raw.order;
  const readMinutes = raw.readMinutes;
  if (!Number.isInteger(order) || Number(order) < 1) throw new Error(`Blog content ${fileName} requires a positive integer "order".`);
  if (!Number.isInteger(readMinutes) || Number(readMinutes) < 1) throw new Error(`Blog content ${fileName} requires positive integer "readMinutes".`);

  const slug = requiredString(raw, "slug", fileName);
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) throw new Error(`Blog content ${fileName} has an unsafe slug.`);
  const image = requiredString(raw, "image", fileName);
  if (!image.startsWith("/images/")) throw new Error(`Blog content ${fileName} must use a local /images/ asset.`);

  const sections = raw.sections;
  const sources = raw.sources;
  if (!Array.isArray(sections) || sections.length === 0) throw new Error(`Blog content ${fileName} requires sections.`);
  if (!Array.isArray(sources) || sources.length === 0) throw new Error(`Blog content ${fileName} requires sources.`);

  const keyNumber = raw.keyNumber;
  if (keyNumber !== undefined && !isRecord(keyNumber)) throw new Error(`Blog content ${fileName} has an invalid keyNumber.`);

  return {
    order: Number(order),
    slug,
    category: requiredString(raw, "category", fileName),
    title: requiredString(raw, "title", fileName),
    dek: requiredString(raw, "dek", fileName),
    readMinutes: Number(readMinutes),
    reviewed: requiredString(raw, "reviewed", fileName),
    image,
    imageAlt: requiredString(raw, "imageAlt", fileName),
    ...(keyNumber
      ? { keyNumber: { value: requiredString(keyNumber, "value", fileName), label: requiredString(keyNumber, "label", fileName) } }
      : {}),
    sections: sections.map((section) => parseSection(section, fileName)),
    sources: sources.map((source) => parseSource(source, fileName)),
  };
}

export function getBlogArticles(): readonly BlogArticle[] {
  if (cachedArticles) return cachedArticles;
  const files = readdirSync(contentDirectory)
    .filter((fileName) => fileName.endsWith(".json"))
    .sort();
  if (files.length === 0) throw new Error("The blog content collection is empty.");

  const articles = files.map((fileName) => {
    const raw = JSON.parse(readFileSync(path.join(contentDirectory, fileName), "utf8")) as unknown;
    return parseArticle(raw, fileName);
  });
  const uniqueSlugs = new Set(articles.map((article) => article.slug));
  if (uniqueSlugs.size !== articles.length) throw new Error("Blog article slugs must be unique.");

  cachedArticles = Object.freeze(articles.sort((left, right) => left.order - right.order));
  return cachedArticles;
}

export function getBlogArticle(slug: string) {
  return getBlogArticles().find((article) => article.slug === slug);
}
