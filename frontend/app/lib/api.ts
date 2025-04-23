import axios from "axios";
import { ChartStatus, ChartResult } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";
const API_KEY = process.env.NEXT_PUBLIC_API_KEY || "development_api_key";

// Axios instance with common configuration
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "X-API-KEY": API_KEY,
  },
});

// Upload a chart image
export const uploadChart = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await api.post("/charts", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "アップロードに失敗しました。");
    }
    throw new Error("アップロードに失敗しました。");
  }
};

// Get chart processing status
export const getChartStatus = async (chartId: string) => {
  try {
    const response = await api.get(`/charts/${chartId}/status`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "ステータスの取得に失敗しました。");
    }
    throw new Error("ステータスの取得に失敗しました。");
  }
};

// Get chart processing result
export const getChartResult = async (chartId: string): Promise<ChartResult> => {
  try {
    const response = await api.get(`/charts/${chartId}`);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "結果の取得に失敗しました。");
    }
    throw new Error("結果の取得に失敗しました。");
  }
};

// Download CSV
export const downloadCsv = async (chartId: string) => {
  try {
    const response = await api.get(`/charts/${chartId}/csv`, {
      responseType: "blob",
    });

    // Create a download link and trigger download
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    
    // Get filename from Content-Disposition header or use default
    const contentDisposition = response.headers["content-disposition"];
    let filename = `chart_${chartId}.csv`;
    
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename=(.+)/);
      if (filenameMatch && filenameMatch.length > 1) {
        filename = filenameMatch[1].replace(/\"/g, "");
      }
    }
    
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || "CSVのダウンロードに失敗しました。");
    }
    throw new Error("CSVのダウンロードに失敗しました。");
  }
};
