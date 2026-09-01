import { useState } from "react";
import { Link } from "react-router-dom";

import type { AdSummary } from "../../types/api";
import { formatNumber, formatPercentage } from "../../utils/formatters";

import "./CampaignAds.scss";

interface CampaignAdsProps {
  ads: AdSummary[];
}

export const CampaignAds = ({ ads }: CampaignAdsProps) => {
  const [selectedAdId, setSelectedAdId] = useState(ads[0]?.ad_id ?? "");

  if (ads.length === 0) {
    return null;
  }

  const selectedAd = ads.find((ad) => ad.ad_id === selectedAdId) ?? ads[0];

  return (
    <section className="campaign-ads">
      <header className="campaign-ads__header">
        <div>
          <span className="campaign-ads__eyebrow">Creative performance</span>

          <h2>Campaign ads</h2>

          <p>Compare ad performance and select a creative to inspect.</p>
        </div>
      </header>

      <div className="campaign-ads__workspace">
        <div className="campaign-ads__list">
          <div className="campaign-ads__list-header">
            <span>Creative</span>
            <span>CTR</span>
            <span>Eng.</span>
          </div>

          {ads.map((ad) => {
            const isSelected = ad.ad_id === selectedAd.ad_id;

            return (
              <button
                key={ad.ad_id}
                type="button"
                className={`campaign-ads__row${
                  isSelected ? " campaign-ads__row--selected" : ""
                }`}
                aria-pressed={isSelected}
                onClick={() => setSelectedAdId(ad.ad_id)}
              >
                <span className="campaign-ads__creative">
                  <img src={`/ads/${ad.image}`} alt="" />

                  <span>
                    <strong>{ad.title}</strong>

                    <small>{formatNumber(ad.total_impressions)} impressions</small>
                  </span>
                </span>

                <span className="campaign-ads__metric">{formatPercentage(ad.ctr)}</span>

                <span className="campaign-ads__metric">
                  {formatPercentage(ad.engagement_rate)}
                </span>
              </button>
            );
          })}
        </div>

        <article className="campaign-ads__preview">
          <div className="campaign-ads__preview-image">
            <img
              src={`/ads/${selectedAd.image}`}
              alt={`${selectedAd.title} creative`}
            />
          </div>

          <div className="campaign-ads__preview-content">
            <div>
              <span className="campaign-ads__preview-label">Selected creative</span>

              <h3>{selectedAd.title}</h3>
            </div>

            <dl className="campaign-ads__preview-metrics">
              <div>
                <dt>Impressions</dt>
                <dd>{formatNumber(selectedAd.total_impressions)}</dd>
              </div>

              <div>
                <dt>Clicks</dt>
                <dd>{formatNumber(selectedAd.total_clicks)}</dd>
              </div>

              <div>
                <dt>CTR</dt>
                <dd>{formatPercentage(selectedAd.ctr)}</dd>
              </div>

              <div>
                <dt>Engagement</dt>
                <dd>{formatPercentage(selectedAd.engagement_rate)}</dd>
              </div>
            </dl>

            <Link to={`/ads/${selectedAd.ad_id}`} className="campaign-ads__details-link">
              View full analysis
              <span aria-hidden="true">→</span>
            </Link>
          </div>
        </article>
      </div>
    </section>
  );
};
