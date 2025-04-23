"use client";

import { useEffect, useState } from "react";
import { getChartResult, downloadCsv } from "../lib/api";
import { ChartResult, ExtractedDataItem } from "../lib/types";
import CsvDownloader from "./CsvDownloader";

interface ResultDisplayProps {
  chartId: string;
}

export default function ResultDisplay({ chartId }: ResultDisplayProps) {
  const [result, setResult] = useState<ChartResult | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        setIsLoading(true);
        const data = await getChartResult(chartId);
        setResult(data);
        setError(null);
      } catch (error) {
        console.error("Error fetching result:", error);
        setError("結果の取得に失敗しました。");
      } finally {
        setIsLoading(false);
      }
    };

    fetchResult();
  }, [chartId]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center p-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
        {error || "結果を取得できませんでした。"}
      </div>
    );
  }

  // Check if result has the expected data
  if (result.status !== "completed" || !result.extracted_data) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 text-yellow-700 px-4 py-3 rounded-lg">
        処理が完了していないか、データが見つかりませんでした。
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="p-6">
        <h2 className="text-xl font-semibold mb-4">抽出結果</h2>
        
        <div className="flex flex-col lg:flex-row">
          {/* Left side - Image viewer */}
          <div className="w-full lg:w-3/5 mb-6 lg:mb-0 lg:pr-6">
            <div className="border rounded-lg p-2 bg-gray-50 flex items-center justify-center h-full">
              <div className="text-center">
                <p className="text-gray-500 mb-2">元の画像ファイル: {result.original_filename}</p>
                <p className="text-xs text-gray-400">{result.gcs_uri}</p>
                {/* When implementing direct image display, it would go here */}
              </div>
            </div>
          </div>
          
          {/* Right side - Extracted text viewer */}
          <div className="w-full lg:w-2/5">
            <div className="border rounded-lg p-4 bg-gray-50 h-full">
              <div className="space-y-4">
                {result.extracted_data.map((item: ExtractedDataItem, index) => (
                  <div key={index} className="border-b pb-3 last:border-b-0 last:pb-0">
                    <h3 className="font-semibold text-gray-700">{item.item_name}</h3>
                    <p className="mt-1 text-gray-600 whitespace-pre-line">
                      {item.item_value || "(記載なし)"}
                    </p>
                  </div>
                ))}
              </div>
            </div>
            
            {/* CSV Download button */}
            <div className="mt-4">
              <CsvDownloader chartId={chartId} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
