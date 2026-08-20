"use client";

import { useEffect, useState } from "react";

interface StatusSummary {
  total_detections: number;
  unique_objects: number;
  total_videos: number;
  last_video: string;
  last_processed_at: string;
}

interface Anomaly {
  id: number;
  frame_number: number;
  timestamp: string;
  video_name: string;
  object_id: number;
  class_name: string;
  speed: number;
}

interface VideoSummary {
  video_name: string;
  total_detections: number;
  unique_objects: number;
  anomaly_count: number;
  processed_at: string;
}

export default function Dashboard() {
  const [status, setStatus] = useState<StatusSummary | null>(null);
  const [anomalies, setAnomalies] = useState<Anomaly[]>([]);
  const [videos, setVideos] = useState<VideoSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const API_BASE = "http://localhost:8000/api";

  const fetchData = async () => {
    try {
      const [resStatus, resAnomalies, resVideos] = await Promise.all([
        fetch(`${API_BASE}/status`),
        fetch(`${API_BASE}/anomalies`),
        fetch(`${API_BASE}/videos`),
      ]);

      if (resStatus.ok) setStatus(await resStatus.json());
      if (resAnomalies.ok) {
        const data = await resAnomalies.json();
        setAnomalies(data.anomalies);
      }
      if (resVideos.ok) {
        const data = await resVideos.json();
        setVideos(data.videos);
      }
    } catch (err) {
      console.error("Error fetching Dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(() => {
      fetchData();
    }, 5000); // Auto refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      <header className="mb-8 border-b border-slate-800 pb-4 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-sky-400">📹 Real-Time Video Monitor</h1>
          <p className="text-slate-400 text-sm mt-1">Industrial Line Monitoring & Tracking System</p>
        </div>
        <div className="flex items-center gap-3">
          <span className="flex h-3 w-3 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
          </span>
          <span className="text-xs text-emerald-400 font-mono font-semibold">LIVE (Auto 5s)</span>
          <button
            onClick={fetchData}
            className="bg-sky-600 hover:bg-sky-500 text-white px-3 py-1.5 rounded-lg text-xs transition"
          >
            🔄 Refresh
          </button>
        </div>
      </header>

      {loading && !status ? (
        <div className="text-center py-20 text-slate-400">Loading Dashboard Data...</div>
      ) : (
        <div className="space-y-8">
          {/* Top Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-slate-800 border border-slate-700 p-5 rounded-xl">
              <span className="text-slate-400 text-xs uppercase font-semibold">Total Detections</span>
              <p className="text-3xl font-extrabold text-white mt-2">{status?.total_detections ?? 0}</p>
            </div>
            <div className="bg-slate-800 border border-slate-700 p-5 rounded-xl">
              <span className="text-slate-400 text-xs uppercase font-semibold">Unique Tracked Objects</span>
              <p className="text-3xl font-extrabold text-emerald-400 mt-2">{status?.unique_objects ?? 0}</p>
            </div>
            <div className="bg-slate-800 border border-slate-700 p-5 rounded-xl">
              <span className="text-slate-400 text-xs uppercase font-semibold">Videos Processed</span>
              <p className="text-3xl font-extrabold text-purple-400 mt-2">{status?.total_videos ?? 0}</p>
            </div>
            <div className="bg-slate-800 border border-slate-700 p-5 rounded-xl">
              <span className="text-slate-400 text-xs uppercase font-semibold">Latest Processed Video</span>
              <p className="text-lg font-bold text-amber-400 mt-2 truncate">{status?.last_video ?? "N/A"}</p>
            </div>
          </div>

          {/* Videos Summary Table */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <h2 className="text-xl font-bold mb-4 text-slate-200">📊 Processed Videos Summary</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-700 text-slate-400 text-xs uppercase">
                    <th className="py-3 px-4">Video Name</th>
                    <th className="py-3 px-4">Detections</th>
                    <th className="py-3 px-4">Unique Objects</th>
                    <th className="py-3 px-4">Anomalies</th>
                    <th className="py-3 px-4">Processed At</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700 text-sm">
                  {videos.map((v, i) => (
                    <tr key={i} className="hover:bg-slate-750">
                      <td className="py-3 px-4 font-mono text-sky-300">{v.video_name}</td>
                      <td className="py-3 px-4">{v.total_detections}</td>
                      <td className="py-3 px-4">{v.unique_objects}</td>
                      <td className="py-3 px-4 font-bold text-rose-400">{v.anomaly_count}</td>
                      <td className="py-3 px-4 text-slate-400">{v.processed_at}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Anomalies Log Table */}
          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">
            <h2 className="text-xl font-bold mb-4 text-rose-400 flex items-center gap-2">
              🚨 Speed Anomalies Logged ({anomalies.length})
            </h2>
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="border-b border-slate-700 text-slate-400 text-xs uppercase">
                    <th className="py-3 px-4">Frame</th>
                    <th className="py-3 px-4">Video</th>
                    <th className="py-3 px-4">Object ID</th>
                    <th className="py-3 px-4">Class</th>
                    <th className="py-3 px-4">Speed (px/f)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700 text-sm">
                  {anomalies.map((a) => (
                    <tr key={a.id} className="hover:bg-slate-750">
                      <td className="py-3 px-4 font-mono">{a.frame_number}</td>
                      <td className="py-3 px-4 font-mono text-slate-300">{a.video_name}</td>
                      <td className="py-3 px-4 font-bold text-amber-300">ID: {a.object_id}</td>
                      <td className="py-3 px-4">{a.class_name}</td>
                      <td className="py-3 px-4 font-mono font-bold text-rose-400">{a.speed}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
