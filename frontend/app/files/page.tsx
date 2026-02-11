"use client";

import { useState, useEffect } from "react";
import FileUpload from "@/components/FileUpload";
import { apiClient } from "@/lib/api-client";

interface UploadedFile {
  id: number;
  filename: string;
  file_size: number;
  file_type: string;
  upload_date: string;
  processed: boolean;
}

interface PermissionStatus {
  has_permission: boolean;
  is_admin: boolean;
  max_files?: number | string;
  max_file_size_mb?: number;
  current_file_count?: number;
  message?: string;
}

export default function FilesPage() {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [permission, setPermission] = useState<PermissionStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [requesting, setRequesting] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [filesData, permData] = await Promise.all([
        apiClient.get<{ files: UploadedFile[] }>("/api/files"),
        apiClient.get<PermissionStatus>("/api/files/permission/status"),
      ]);

      setFiles(filesData.files || []);
      setPermission(permData);
      setLoading(false);
    } catch (error) {
      console.error("Failed to load files:", error);
      setLoading(false);
    }
  };

  const deleteFile = async (fileId: number) => {
    if (!confirm("Delete this file? This cannot be undone.")) return;

    try {
      await apiClient.delete(`/api/files/${fileId}`);
      alert("File deleted successfully");
      loadData();
    } catch (error: any) {
      alert(`Failed to delete file: ${error.message}`);
    }
  };

  const requestPermission = async () => {
    setRequesting(true);
    try {
      const result = await apiClient.post<{ message: string }>("/api/files/request-permission", {});
      alert(result.message || "Permission request sent to admin");
      loadData();
    } catch (error: any) {
      alert(`Failed to request permission: ${error.message}`);
    }
    setRequesting(false);
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading...</div>
      </div>
    );
  }

  const canUpload = permission?.has_permission || permission?.is_admin;

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Documents</h1>
          <p className="text-gray-600 mt-2">
            Upload files to give the AI chatbot context about your projects
          </p>
        </div>

        {/* Permission Status */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-lg font-semibold mb-3 text-gray-900">
            Upload Permission Status
          </h2>

          {permission?.is_admin ? (
            <div className="flex items-center gap-2 text-green-600">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="font-medium">Admin - Unlimited Access</span>
            </div>
          ) : permission?.has_permission ? (
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-green-600">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="font-medium">Upload Enabled</span>
              </div>
              <div className="text-sm text-gray-600">
                <div>Max files: {permission.max_files}</div>
                <div>Max size: {permission.max_file_size_mb}MB per file</div>
                <div>
                  Current: {permission.current_file_count} / {permission.max_files} files
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-red-600">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
                <span className="font-medium">No Upload Permission</span>
              </div>
              <p className="text-sm text-gray-600">
                You need permission from the admin to upload files.
              </p>
              <button
                onClick={requestPermission}
                disabled={requesting}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 text-sm"
              >
                {requesting ? "Requesting..." : "Request Permission"}
              </button>
            </div>
          )}
        </div>

        {/* Upload Section */}
        {canUpload && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-lg font-semibold mb-4 text-gray-900">
              Upload New Document
            </h2>
            <FileUpload onUploadSuccess={loadData} />
          </div>
        )}

        {/* Files List */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Uploaded Documents ({files.length})
            </h2>
          </div>

          {files.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              No files uploaded yet
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {files.map((file) => (
                <div key={file.id} className="p-6 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                      <svg
                        className="w-6 h-6 text-purple-600"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
                        />
                      </svg>
                    </div>

                    <div>
                      <div className="font-medium text-gray-900">
                        {file.filename}
                      </div>
                      <div className="text-sm text-gray-500">
                        {formatFileSize(file.file_size)} •{" "}
                        {file.file_type.toUpperCase()} •{" "}
                        {new Date(file.upload_date).toLocaleDateString()}
                      </div>
                      <div className="text-xs mt-1">
                        {file.processed ? (
                          <span className="text-green-600">✓ Processed</span>
                        ) : (
                          <span className="text-yellow-600">⏳ Processing...</span>
                        )}
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => deleteFile(file.id)}
                    className="text-red-600 hover:text-red-700 text-sm font-medium"
                  >
                    Delete
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
