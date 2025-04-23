"use client";

import { useState } from "react";
import ImageUploader from "./components/ImageUploader";
import ResultDisplay from "./components/ResultDisplay";
import StatusBar from "./components/StatusBar";
import { ChartStatus } from "./lib/types";

export default function Home() {
  const [chartId, setChartId] = useState<string | null>(null);
  const [status, setStatus] = useState<ChartStatus | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Handle successful upload
  const handleUploadSuccess = (id: string) => {
    setChartId(id);
    setStatus("pending");
    setError(null);
  };

  // Handle upload error
  const handleUploadError = (errorMessage: string) => {
    setError(errorMessage);
    setChartId(null);
    setStatus(null);
  };

  // Handle status change
  const handleStatusChange = (newStatus: ChartStatus) => {
    setStatus(newStatus);
  };

  return (
    <div className="flex flex-col space-y-6">
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">カルテ画像アップロード</h2>
        <ImageUploader
          onUploadSuccess={handleUploadSuccess}
          onUploadError={handleUploadError}
          disabled={!!chartId && status !== "completed" && status !== "failed"}
        />
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}

      {chartId && (
        <>
          <StatusBar 
            chartId={chartId} 
            onStatusChange={handleStatusChange} 
          />
          
          {status === "completed" && (
            <ResultDisplay chartId={chartId} />
          )}
        </>
      )}
    </div>
  );
}
