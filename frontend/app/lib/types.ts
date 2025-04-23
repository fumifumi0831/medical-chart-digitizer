// Chart processing status
export type ChartStatus = "pending" | "processing" | "completed" | "failed";

// Extracted data item
export interface ExtractedDataItem {
  item_name: string;
  item_value: string | null;
}

// Chart result from API
export interface ChartResult {
  chart_id: string;
  original_filename?: string;
  gcs_uri?: string;
  status: ChartStatus;
  extracted_data?: ExtractedDataItem[];
  message?: string;
  error_message?: string;
}
