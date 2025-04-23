"use client";

import { useState } from "react";
import { downloadCsv } from "../lib/api";

interface CsvDownloaderProps {
  chartId: string;
}

export default function CsvDownloader({ chartId }: CsvDownloaderProps) {
  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDownload = async () => {
    try {
      setIsDownloading(true);
      setError(null);
      await downloadCsv(chartId);
    } catch (error) {
      console.error("Error downloading CSV:", error);
      setError("CSVのダウンロードに失敗しました。");
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div>
      <button
        onClick={handleDownload}
        disabled={isDownloading}
        className="btn-primary w-full flex justify-center items-center"
      >
        {isDownloading ? (
          <>
            <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full mr-2"></div>
            ダウンロード中...
          </>
        ) : (
          <>
            <svg
              className="h-4 w-4 mr-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            CSV形式でダウンロード
          </>
        )}
      </button>
      
      {error && (
        <div className="mt-2 text-sm text-red-600">{error}</div>
      )}
    </div>
  );
}
