import { Link } from "react-router-dom";

import { useAds } from "../../hooks/useAds";

import "./AdNavigation.scss";

interface AdNavigationProps {
  currentAdId: string;
}

export const AdNavigation = ({ currentAdId }: AdNavigationProps) => {
  const adsQuery = useAds();
  const ads = adsQuery.data ?? [];
  const currentIndex = ads.findIndex((ad) => ad.ad_id === currentAdId);

  if (currentIndex === -1 || ads.length < 2) {
    return null;
  }

  const previousAd = ads[currentIndex - 1];
  const nextAd = ads[currentIndex + 1];

  return (
    <nav className="ad-navigation" aria-label="Ad navigation">
      {previousAd ? (
        <Link className="ad-navigation__link" to={`/ads/${previousAd.ad_id}`}>
          Previous
        </Link>
      ) : (
        <span
          className="ad-navigation__link ad-navigation__link--disabled"
          aria-disabled="true"
        >
          Previous
        </span>
      )}

      <span className="ad-navigation__divider" aria-hidden="true">
        |
      </span>

      {nextAd ? (
        <Link className="ad-navigation__link" to={`/ads/${nextAd.ad_id}`}>
          Next
        </Link>
      ) : (
        <span
          className="ad-navigation__link ad-navigation__link--disabled"
          aria-disabled="true"
        >
          Next
        </span>
      )}
    </nav>
  );
};
