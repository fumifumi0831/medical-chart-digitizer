"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { uploadChart } from "../lib/api";

interface ImageUploaderProps {
  onUploadSuccess: (chartId: string) => void;
  onUploadError: (error: string) => void;
  disabled?: boolean;
}

export default function ImageUploader({
  onUploadSuccess,
  onUploadError,
  disabled = false,
}: ImageUploaderProps) {
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      // Validate file
      if (acceptedFiles.length === 0) {
        return;
      }

      const file = acceptedFiles[0];

      // Validate file type
      if (!["image/jpeg", "image/png"].includes(file.type)) {
        onUploadError("ファイル形式はJPEGまたはPNGのみです。");
        return;
      }

      // Validate file size (10MB)
      if (file.size > 10 * 1024 * 1024) {
        onUploadError("ファイルサイズは10MBまでです。");
        return;
      }

      setIsUploading(true);

      try {
        // Upload file using API
        const result = await uploadChart(file);
        onUploadSuccess(result.chart_id);
      } catch (error) {
        console.error("Upload error:", error);
        onUploadError(error instanceof Error ? error.message : "アップロードに失敗しました。");
      } finally {
        setIsUploading(false);
      }
    },
    [onUploadSuccess, onUploadError]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/jpeg": [],
      "image/png": [],
    },
    multiple: false,
    disabled: disabled || isUploading,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive ? "border-primary-500 bg-primary-50" : "border-gray-300 hover:border-primary-400"} ${
          disabled || isUploading ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        <input {...getInputProps()} />
        {isUploading ? (
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600 mb-2"></div>
            <p>アップロード中...</p>
          </div>
        ) : (
          <div>
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
            <p className="mt-2 text-sm text-gray-600">
              {isDragActive
                ? "ドロップしてアップロード"
                : "クリックしてファイルを選択、またはドラッグ＆ドロップ"}
            </p>
            <p className="mt-1 text-xs text-gray-500">
              JPEG または PNG, 最大10MB
            </p>
          </div>
        )}
      </div>
      {!isUploading && !disabled && (
        <div className="mt-4 flex justify-center">
          <button
            type="button"
            className="btn-primary w-full max-w-md"
            onClick={() => document.getElementById("file-input")?.click()}
            disabled={disabled || isUploading}
          >
            画像を選択
          </button>
        </div>
      )}
    </div>
  );
}
