import type { Metadata } from "next";
import { ArticleCard, FeaturedArticleCard } from "@/components/blog/article-cards";
import { PrototypeBanner, SiteHeader } from "@/components/site-header";
import { getBlogArticles } from "@/lib/blog-content";
import styles from "@/styles/content.module.css";

export const metadata: Metadata = {
  title: "Evidence and planning insights",
  description: "Sourced, dated guidance for understanding cross-border planned-care referrals to India.",
};

export default function BlogPage() {
  const blogArticles = getBlogArticles();
  const [featured, ...articles] = blogArticles;
  return <><PrototypeBanner /><SiteHeader /><main className={styles.blogPage}>
    <section className="blog-hero page-shell"><div><span className="eyebrow">Evidence, not destination hype</span><h1>Plan cross-border care with sources, uncertainty, and a trusted home-doctor loop.</h1><p>{blogArticles.length} editorial explainers reviewed on 11 August 2026. This content supports questions and planning; it is not medical, legal, visa, or financial advice.</p></div></section>
    <FeaturedArticleCard article={featured} />
    <section className="article-grid page-shell" aria-label="All insight articles">{articles.map((article) => <ArticleCard article={article} key={article.slug} />)}</section>
  </main></>;
}
