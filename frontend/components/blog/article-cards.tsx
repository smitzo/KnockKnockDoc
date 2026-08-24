import Image from "next/image";
import Link from "next/link";

import type { BlogArticle } from "@/lib/blog-content";

import { Icon } from "../icons";

export function FeaturedArticleCard({ article }: { article: BlogArticle }) {
  return (
    <section className="featured-article page-shell">
      <Image alt={article.imageAlt} height={900} priority sizes="(max-width: 800px) 100vw, 55vw" src={article.image} width={1600} />
      <div>
        <span>{article.category} · {article.readMinutes} min</span>
        <h2>{article.title}</h2>
        <p>{article.dek}</p>
        {article.keyNumber && <div className="article-number"><strong>{article.keyNumber.value}</strong><small>{article.keyNumber.label}</small></div>}
        <Link className="button" href={`/blog/${article.slug}`}>Read the evidence brief <Icon name="arrow" /></Link>
      </div>
    </section>
  );
}

export function ArticleCard({ article }: { article: BlogArticle }) {
  return (
    <article>
      <span>{article.category} · {article.readMinutes} min</span>
      <h2><Link href={`/blog/${article.slug}`}>{article.title}</Link></h2>
      <p>{article.dek}</p>
      <div><small>Reviewed {article.reviewed}</small><Link href={`/blog/${article.slug}`}>Read article <Icon name="arrow" /></Link></div>
    </article>
  );
}
