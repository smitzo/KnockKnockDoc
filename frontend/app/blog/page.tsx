import type { Metadata } from "next";
import { ArticleCard, FeaturedArticleCard } from "@/components/blog/article-cards";
import { SiteFooter, SiteHeader } from "@/components/site-header";
import { getBlogArticles } from "@/lib/blog-content";
import styles from "@/styles/content.module.css";

export const metadata: Metadata = {
  title: "Evidence and planning insights",
  description: "Sourced, dated guidance for understanding cross-border planned-care referrals to India.",
};

export default function BlogPage() {
  const blogArticles = getBlogArticles();
  const [featured, ...articles] = blogArticles;
  return <><SiteHeader /><main className={styles.blogPage}>
    <section className="blog-hero page-shell"><div><span className="eyebrow">Knock Knock Doc blogs</span><h1>Clear guides for better referrals and medical travel planning.</h1><p>Explore {blogArticles.length} practical articles on choosing providers, comparing cities, understanding costs, and keeping the home doctor involved.</p></div></section>
    <FeaturedArticleCard article={featured} />
    <section className="article-grid page-shell" aria-label="All insight articles">{articles.map((article) => <ArticleCard article={article} key={article.slug} />)}</section>
  </main><SiteFooter /></>;
}
