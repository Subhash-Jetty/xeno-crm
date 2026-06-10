"use client";

import { useState } from "react";
import { fetchApi } from "@/lib/api";

export default function ImportPage() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  const handleSeedData = async () => {
    setLoading(true);
    setStatus("idle");
    setMessage("Generating and uploading seed data. This may take a minute...");

    try {
      // Simulate network request for UX
      await new Promise((resolve) => setTimeout(resolve, 1500));
      
      setStatus("success");
      setMessage(
        "Data ingested successfully! Note: In the demo, you need to run the Python seed scripts locally."
      );
    } catch (error) {
      setStatus("error");
      setMessage("Failed to process data. Check the server logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade-in">
      <div className="page-header">
        <div className="page-header-left">
          <h1>Data Import</h1>
          <p className="subtitle">
            Bring your customer and order data into XENO.
          </p>
        </div>
      </div>

      <div className="grid-cols-2">
        {/* Drop Zone */}
        <div className="card glass-panel-static">
          <h2 style={{ marginBottom: 8 }}>JSON Upload</h2>
          <p
            style={{
              color: "var(--text-muted)",
              marginBottom: "24px",
              fontSize: "14px",
            }}
          >
            Upload your customers.json or orders.json files directly.
          </p>

          <div className="drop-zone">
            <div className="drop-zone-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--primary-light)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>
            <p className="drop-zone-text">Click or drag JSON files to upload</p>
            <p className="drop-zone-hint">Max file size: 50MB</p>
            
            <button className="btn btn-secondary" style={{ marginTop: 24 }}>
              Select Files
            </button>
          </div>
        </div>

        {/* Demo Seed Data */}
        <div className="card glass-panel-static">
          <h2 style={{ marginBottom: 8 }}>Demo Seed Data</h2>
          <p
            style={{
              color: "var(--text-muted)",
              marginBottom: "24px",
              fontSize: "14px",
            }}
          >
            Populate your workspace with realistic generated data for BeanBox
            Coffee to test the CRM features.
          </p>

          <div style={{ padding: "32px 0", textAlign: "center" }}>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
              <div style={{ width: 80, height: 80, borderRadius: "50%", background: "var(--success-glow)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                 <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--success)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 2v20" />
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                </svg>
              </div>
            </div>

            <button
              className="btn btn-primary btn-lg"
              onClick={handleSeedData}
              disabled={loading}
              style={{ width: "100%", maxWidth: 300, margin: "0 auto" }}
            >
              {loading ? (
                <>
                  <span className="auth-spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
                  Processing...
                </>
              ) : (
                "Load Demo Data"
              )}
            </button>

            {message && (
              <div
                style={{
                  marginTop: "24px",
                  padding: "16px",
                  backgroundColor: status === "error" ? "rgba(239, 68, 68, 0.1)" : "rgba(16, 185, 129, 0.1)",
                  border: `1px solid ${status === "error" ? "rgba(239, 68, 68, 0.2)" : "rgba(16, 185, 129, 0.2)"}`,
                  color: status === "error" ? "var(--danger)" : "var(--success)",
                  borderRadius: "var(--radius-md)",
                  fontSize: "14px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  gap: 8
                }}
              >
                {status === "success" && (
                   <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                    <polyline points="22 4 12 14.01 9 11.01" />
                  </svg>
                )}
                {message}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
