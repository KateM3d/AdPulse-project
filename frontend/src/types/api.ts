export type Platform = "Google" | "LinkedIn" | "Meta";

export interface CampaignSummary {
  total_impressions: number;
  total_clicks: number;
  total_engagements: number;
  ctr: number;
  engagement_rate: number;
  start_date: string | null;
  end_date: string | null;
}

export interface TimelinePoint {
  date: string;
  impressions: number;
  clicks: number;
  engagements: number;
  ctr: number;
  engagement_rate: number;
}

export interface PlatformSummary {
  platform: Platform;
  impressions: number;
  clicks: number;
  engagements: number;
  ctr: number;
  engagement_rate: number;
}

export interface CampaignResponse {
  summary: CampaignSummary;
  timeline: TimelinePoint[];
  platforms: PlatformSummary[];
}

export interface AdSummary {
  ad_id: string;
  title: string;
  image: string;
  total_impressions: number;
  total_clicks: number;
  total_engagements: number;
  ctr: number;
  engagement_rate: number;
}

export interface AdComment {
  date: string;
  platform: Platform;
  comment: string;
}

export interface AdDetail extends AdSummary {
  body: string;
  timeline: TimelinePoint[];
  platforms: PlatformSummary[];
  comments: AdComment[];
}
