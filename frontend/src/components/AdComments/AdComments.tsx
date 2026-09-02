import type { AdComment } from "../../types/api";
import { formatDate } from "../../utils/formatters";

import "./AdComments.scss";

interface AdCommentsProps {
  comments: AdComment[];
}

export const AdComments = ({ comments }: AdCommentsProps) => (
  <section className="ad-comments">
    <header className="ad-comments__header">
      <h2>Audience feedback</h2>

      <span className="ad-comments__count">{comments.length} comments</span>
    </header>

    {comments.length === 0 ? (
      <p className="ad-comments__empty">No comments available for this ad.</p>
    ) : (
      <div className="ad-comments__list">
        {comments.map((comment, index) => (
          <article
            className="ad-comments__item"
            key={`${comment.date}-${comment.platform}-${index}`}
          >
            <div className="ad-comments__meta">
              <span className="ad-comments__platform">{comment.platform}</span>

              <time dateTime={comment.date}>{formatDate(comment.date)}</time>
            </div>

            <p>{comment.comment}</p>
          </article>
        ))}
      </div>
    )}
  </section>
);
