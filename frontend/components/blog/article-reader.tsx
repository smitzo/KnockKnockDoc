import type { BlogArticle } from "@/lib/blog-content";

import { Icon } from "../icons";

export function ArticleBody({ article }: { article: BlogArticle }) {
  return (
    <article className="article-body">
      {article.keyNumber && <div className="article-key-number"><strong>{article.keyNumber.value}</strong><span>{article.keyNumber.label}</span></div>}
      {article.sections.map((section) => (
        <section key={section.heading}>
          <h2>{section.heading}</h2>
          {section.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
          {section.bullets && <ul>{section.bullets.map((bullet) => <li key={bullet}>{bullet}</li>)}</ul>}
        </section>
      ))}
      <div className="article-disclaimer">
        <Icon name="shield" />
        <p><strong>Scope boundary.</strong> This article is educational. Suitability, risk, cost, visa eligibility and follow-up must be confirmed by the relevant licensed clinicians, facility, government channels and qualified advisers.</p>
      </div>
    </article>
  );
}

export function ArticleSources({ article }: { article: BlogArticle }) {
  return (
    <aside className="article-sources">
      <span className="eyebrow">Direct sources</span>
      <h2>Check the evidence</h2>
      {article.sources.map((source, index) => (
        <a href={source.url} key={source.url} rel="noreferrer" target="_blank">
          <span>{String(index + 1).padStart(2, "0")}</span>
          <div><strong>{source.title}</strong><small>{source.publisher}</small><p>{source.supports}</p></div>
          <Icon name="arrow" />
        </a>
      ))}
      <small>Links and policies can change. The review date is shown so readers can refresh them.</small>
    </aside>
  );
}
