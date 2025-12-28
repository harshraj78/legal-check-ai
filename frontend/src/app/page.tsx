"use client";

import { useEffect, useState } from "react";

type Result = {
  id: string;
  filename: string;
  status: string;
  risk_score: number;
  summary: string;
};

type Status = "idle" | "uploading" | "processing" | "completed";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [contractId, setContractId] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [result, setResult] = useState<Result | null>(null);

  // ------------------------------------------------
  // Poll backend for analysis status
  // ------------------------------------------------
  useEffect(() => {
    if (!contractId) return;

    const interval = setInterval(async () => {
      const res = await fetch(
        `http://localhost:8000/api/v1/contracts/${contractId}`
      );
      const data = await res.json();

      setStatus(data.status);

      if (data.status === "completed") {
        setResult(data);
        clearInterval(interval);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [contractId]);

  // ------------------------------------------------
  // Upload handler
  // ------------------------------------------------
  const handleUpload = async () => {
    if (!file) return;

    setStatus("uploading");

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(
      "http://localhost:8000/api/v1/contracts/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();
    setContractId(data.id);
    setStatus("processing");
  };

  // ------------------------------------------------
  // Reset flow for new upload
  // ------------------------------------------------
  const resetFlow = () => {
    setFile(null);
    setContractId(null);
    setResult(null);
    setStatus("idle");
  };

  // ------------------------------------------------
  // UI helpers
  // ------------------------------------------------
  const riskColor =
    result && result.risk_score < 30
      ? "bg-green-100 text-green-800"
      : result && result.risk_score <= 70
      ? "bg-yellow-100 text-yellow-800"
      : "bg-red-100 text-red-800";

  const statusBadge = {
    idle: "bg-gray-200 text-gray-700",
    uploading: "bg-blue-100 text-blue-700",
    processing: "bg-purple-100 text-purple-700",
    completed: "bg-green-100 text-green-700",
  }[status];

  return (
    <main className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
      <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg p-8">
        {/* Header */}
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-gray-800">
            Legal-Check AI
          </h1>
          <p className="text-gray-500 mt-1">
            Upload a contract to analyze legal risk
          </p>
        </header>

        {/* Upload Section */}
        <div className="border border-dashed rounded-lg p-6 bg-gray-50">
          <input
            type="file"
            onChange={(e) => {
              const selectedFile = e.target.files?.[0] || null;

              // IMPORTANT: reset first, then set file
              if (status === "completed") {
                resetFlow();
              }

              setFile(selectedFile);
            }}
            disabled={status === "uploading" || status === "processing"}
            className="block w-full text-sm text-gray-600
                       file:mr-4 file:py-2 file:px-4
                       file:rounded-md file:border-0
                       file:bg-blue-600 file:text-white
                       hover:file:bg-blue-700
                       disabled:opacity-50"
          />

          <button
            onClick={handleUpload}
            disabled={
              !file ||
              status === "uploading" ||
              status === "processing"
            }
            className="mt-4 w-full bg-blue-600 text-white py-2 rounded-md
                       hover:bg-blue-700 disabled:bg-gray-400 transition"
          >
            {status === "uploading"
              ? "Uploading..."
              : status === "processing"
              ? "Analyzing..."
              : "Analyze Contract"}
          </button>
        </div>

        {/* Status */}
        <div className="mt-6 flex items-center justify-between">
          <span className="text-gray-600">Status</span>
          <span
            className={`px-3 py-1 rounded-full text-sm font-medium ${statusBadge}`}
          >
            {status.toUpperCase()}
          </span>
        </div>

        {/* Result */}
        {result && (
          <div className="mt-8 border-t pt-6">
            <h2 className="text-lg font-semibold mb-4">
              Analysis Result
            </h2>

            <div className={`inline-block px-4 py-2 rounded-lg ${riskColor}`}>
              <span className="font-semibold">
                Risk Score: {result.risk_score}/100
              </span>
            </div>

            <p className="mt-4 text-gray-700 leading-relaxed">
              {result.summary}
            </p>

            <button
              onClick={resetFlow}
              className="mt-6 w-full border border-gray-300 py-2 rounded-md
                         hover:bg-gray-100 transition"
            >
              Analyze Another Contract
            </button>
          </div>
        )}
      </div>
    </main>
  );
}
