"use client";

import { useEffect, useState } from "react";
import { getChartStatus } from "../lib/api";
import { ChartStatus } from "../lib/types";

interface StatusBarProps {
  chartId: string;
  onStatusChange: (status: ChartStatus) => void;
}

export default function StatusBar({ chartId, onStatusChange }: StatusBarProps) {
  const [status, setStatus] = useState<ChartStatus>("pending");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isPolling, setIsPolling] = useState(true);

  useEffect(() => {
    // No need to poll if we're completed or failed
    if (status === "completed" || status === "failed") {
      setIsPolling(false);
      return;
    }

    // Poll the status every 3 seconds
    const pollInterval = setInterval(async () => {
      try {
        const response = await getChartStatus(chartId);
        setStatus(response.status as ChartStatus);
        setErrorMessage(response.error_message || null);
        onStatusChange(response.status as ChartStatus);

        // Stop polling once we reach a terminal state
        if (response.status === "completed" || response.status === "failed") {
          clearInterval(pollInterval);
          setIsPolling(false);
        }
      } catch (error) {
        console.error("Error polling status:", error);
        setStatus("failed");
        setErrorMessage("ステータスの取得に失敗しました。");
        onStatusChange("failed");
        clearInterval(pollInterval);
        setIsPolling(false);
      }
    }, 3000);

    // Initial status check
    getChartStatus(chartId)
      .then((response) => {
        setStatus(response.status as ChartStatus);
        setErrorMessage(response.error_message || null);
        onStatusChange(response.status as ChartStatus);

        // Check if we should stop polling
        if (response.status === "completed" || response.status === "failed") {
          clearInterval(pollInterval);
          setIsPolling(false);
        }
      })
      .catch((error) => {
        console.error("Error checking initial status:", error);
        setStatus("failed");
        setErrorMessage("ステータスの取得に失敗しました。");
        onStatusChange("failed");
        clearInterval(pollInterval);
        setIsPolling(false);
      });

    return () => clearInterval(pollInterval);
  }, [chartId, status, onStatusChange]);

  const getStatusLabel = () => {
    switch (status) {
      case "pending":
        return "処理待ち";
      case "processing":
        return "処理中...";
      case "completed":
        return "処理完了";
      case "failed":
        return "処理失敗";
      default:
        return "不明";
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case "pending":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "processing":
        return "bg-blue-100 text-blue-800 border-blue-200";
      case "completed":
        return "bg-green-100 text-green-800 border-green-200";
      case "failed":
        return "bg-red-100 text-red-800 border-red-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <div className={`border rounded-lg p-4 ${getStatusColor()}`}>
      <div className="flex items-center">
        <div className="mr-3">
          {(status === "pending" || status === "processing") && isPolling && (
            <div className="animate-spin h-5 w-5 border-2 border-current border-t-transparent rounded-full"></div>
          )}
          {status === "completed" && (
            <svg
              className="h-5 w-5 text-green-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
          {status === "failed" && (
            <svg
              className="h-5 w-5 text-red-500"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          )}
        </div>
        <div>
          <p className="font-medium">ステータス: {getStatusLabel()}</p>
          {errorMessage && <p className="text-sm mt-1">{errorMessage}</p>}
        </div>
      </div>
    </div>
  );
}
