"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchApi } from "@/lib/api";

export default function CampaignsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCampaigns();
  }, []);

  const loadCampaigns = async () => {
    try {
      const data = await fetchApi("/campaigns");

      // Fetch stats for each campaign
      const campaignsWithStats = await Promise.all(
        data.map(async (c: any) => {
          try {
            const stats = await fetchApi(`/campaigns/${c.id}/stats`);
            return { ...c, stats };
          } catch {
            return c;
          }
        })
      );

      setCampaigns(campaignsWithStats);
    } catch (error) {
      console.error("Failed to load campaigns:", error);
    } finally {
      setLoading(false);
    }
  };

  const getChannelIcon = (channel: string) => {
    switch (channel.toLowerCase()) {
      case "whatsapp":
        return (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
          </svg>
        );
      case "email":
        return (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
            <polyline points="22,6 12,13 2,6" />
          </svg>
        );
      case "sms":
        return (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        );
      default:
        return (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M22 2L11 13" />
            <path d="M22 2L15 22l-4-9-9-4 20-7z" />
          </svg>
        );
    }
  };

  return (
    <div className="animate-fade-in">
      {/* Page Header */}
      <div className="page-header">
        <div className="page-header-left">
          <h1>Campaigns</h1>
          <p className="subtitle">Track message delivery and customer engagement.</p>
        </div>
        <Link href="/chat" className="btn btn-primary">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          New Campaign
        </Link>
      </div>

      <div className="grid-cols-2 stagger-children">
        {loading ? (
          // Skeleton
          Array.from({ length: 4 }).map((_, idx) => (
            <div key={idx} className="campaign-card">
              <div className="campaign-header">
                <div>
                  <div className="skeleton skeleton-line skeleton-line-medium" style={{ marginBottom: 8, height: 20 }} />
                  <div className="skeleton skeleton-line skeleton-line-short" />
                </div>
                <div className="skeleton skeleton-line" style={{ width: 80, height: 24, borderRadius: 12 }} />
              </div>
              <div className="skeleton skeleton-line" style={{ width: "100%", height: 6, marginTop: 24 }} />
              <div className="campaign-stats-row">
                {Array.from({ length: 4 }).map((_, s) => (
                  <div key={s} className="campaign-stat">
                    <div className="skeleton skeleton-line" style={{ width: 32, height: 24, margin: "0 auto 8px" }} />
                    <div className="skeleton skeleton-line" style={{ width: 48, height: 12, margin: "0 auto" }} />
                  </div>
                ))}
              </div>
            </div>
          ))
        ) : campaigns.length === 0 ? (
          // Empty State
          <div style={{ gridColumn: "1 / -1" }}>
            <div className="card glass-panel-static empty-state">
              <div className="empty-state-icon" style={{ background: "var(--accent-glow)" }}>
                <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M22 2L11 13" />
                  <path d="M22 2L15 22l-4-9-9-4 20-7z" />
                </svg>
              </div>
              <h3>No campaigns yet</h3>
              <p>
                Launch omnichannel campaigns to your segments and track delivery
                rates here.
              </p>
              <Link href="/chat" className="btn btn-primary">
                Launch a campaign via AI
              </Link>
            </div>
          </div>
        ) : (
          // Campaign Cards
          campaigns.map((c) => {
            const deliveryRate = c.stats?.delivery_rate || 0;
            const openRate = c.stats?.open_rate || 0;
            const clickRate = c.stats?.click_rate || 0;

            const isSuccess = c.status === "completed";
            const isWarning = c.status === "in_progress" || c.status === "draft";
            
            return (
              <div key={c.id} className="campaign-card">
                <div className="campaign-header">
                  <div>
                    <h3 className="campaign-title">{c.name}</h3>
                    <div className="campaign-channel">
                      {getChannelIcon(c.channel)}
                      <span style={{ textTransform: "capitalize" }}>
                        {c.channel}
                      </span>
                    </div>
                  </div>
                  <span
                    className={`badge badge-${
                      isSuccess ? "success" : isWarning ? "warning" : "danger"
                    }`}
                  >
                    {c.status.toUpperCase()}
                  </span>
                </div>

                <div style={{ marginTop: 24, marginBottom: 8, display: "flex", justifyContent: "space-between", fontSize: 13 }}>
                  <span style={{ color: "var(--text-muted)" }}>Delivery Progress</span>
                  <span style={{ fontWeight: 500, color: "var(--primary-light)" }}>{deliveryRate}%</span>
                </div>
                <div className="progress-bar">
                  <div
                    className="progress-bar-fill"
                    style={{ width: `${deliveryRate}%` }}
                  />
                </div>

                <div className="campaign-stats-row">
                  <div className="campaign-stat">
                    <div className="campaign-stat-value">{c.sent_count}</div>
                    <div className="campaign-stat-label">Sent</div>
                  </div>
                  <div className="campaign-stat">
                    <div className="campaign-stat-value">{deliveryRate}%</div>
                    <div className="campaign-stat-label">Delivered</div>
                  </div>
                  <div className="campaign-stat">
                    <div className="campaign-stat-value">{openRate}%</div>
                    <div className="campaign-stat-label">Opened</div>
                  </div>
                  <div className="campaign-stat">
                    <div className="campaign-stat-value">{clickRate}%</div>
                    <div className="campaign-stat-label">Clicked</div>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
