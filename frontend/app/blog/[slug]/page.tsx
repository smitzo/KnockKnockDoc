import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";

import { ArticleBody, ArticleSources } from "@/components/blog/article-reader";
import { Icon } from "@/components/icons";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import { getBlogArticle, getBlogArticles } from "@/lib/blog-content";
import styles from "@/styles/content.module.css";

export function generateStaticParams() {
  return getBlogArticles().map((article) => ({ slug: article.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const article = getBlogArticle((await params).slug);
  return article ? { title: article.title, description: article.dek } : {};
}

export default async function ArticlePage({ params }: { params: Promise<{ slug: string }> }) {
  const article = getBlogArticle((await params).slug);
  if (!article) notFound();
  return <><SiteHeader /><main className={styles.articlePage}>
    <header className="article-header page-shell"><Link href="/blog"><Icon name="arrow" /> All insights</Link><span>{article.category} · {article.readMinutes} min read</span><h1>{article.title}</h1><p>{article.dek}</p><small>Evidence last reviewed {article.reviewed}</small></header>
    <figure className="article-image page-shell"><Image alt={article.imageAlt} height={900} priority sizes="(max-width: 1200px) 100vw, 1180px" src={article.image} width={1600} /><figcaption>{article.imageAlt} The scene is illustrative and AI-generated; it depicts no real person, provider or outcome.</figcaption></figure>
    <div className="article-layout page-shell"><ArticleBody article={article} /><ArticleSources article={article} /></div>
  </main><SiteFooter /></>;
}
