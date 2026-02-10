"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  file_count: number;
  has_permission: boolean;
  permission_details: {
    max_files: number;
    max_file_size_mb: number;
  } | null;
}

interface PermissionRequest {
  id: number;
  user_email: string;
  user_name: string;
  requested_at: string;
  status: string;
}

export default function AdminPanel() {
  const router = useRouter();
  const [users, setUsers] = useState<User[]>([]);
  const [requests, setRequests] = useState<PermissionRequest[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [maxFiles, setMaxFiles] = useState(5);
  const [maxSizeMB, setMaxSizeMB] = useState(10);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [usersData, requestsData] = await Promise.all([
        apiClient.get("/api/admin/users"),
        apiClient.get("/api/admin/permission-requests"),
      ]);

      setUsers(usersData);
      setRequests(requestsData);
      setLoading(false);
    } catch (error) {
      console.error("Failed to load data:", error);
      alert("Failed to load admin data. Are you an admin?");
      router.push("/dashboard");
    }
  };

  const grantPermission = async (userEmail: string) => {
    try {
      await apiClient.post("/api/admin/permissions", {
        user_email: userEmail,
        max_files: maxFiles,
        max_file_size_mb: maxSizeMB,
      });

      alert(`✅ Permission granted to ${userEmail}`);
      setSelectedUser(null);
      loadData();
    } catch (error: any) {
      alert(`Failed to grant permission: ${error.message}`);
    }
  };

  const revokePermission = async (userEmail: string) => {
    if (!confirm(`Revoke file upload permission for ${userEmail}?`)) return;

    try {
      await apiClient.delete(`/api/admin/permissions/${userEmail}`);
      alert(`❌ Permission revoked for ${userEmail}`);
      loadData();
    } catch (error: any) {
      alert(`Failed to revoke permission: ${error.message}`);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-600">Loading admin panel...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Panel</h1>
          <p className="text-gray-600 mt-2">Manage file upload permissions</p>
        </div>

        {/* Permission Requests */}
        {requests.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-900">
              🔔 Pending Permission Requests ({requests.length})
            </h2>
            <div className="space-y-3">
              {requests.map((req) => (
                <div
                  key={req.id}
                  className="flex items-center justify-between p-4 bg-yellow-50 border border-yellow-200 rounded-lg"
                >
                  <div>
                    <div className="font-medium text-gray-900">{req.user_name}</div>
                    <div className="text-sm text-gray-600">{req.user_email}</div>
                    <div className="text-xs text-gray-500 mt-1">
                      Requested: {new Date(req.requested_at).toLocaleString()}
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      setSelectedUser(req.user_email);
                      setMaxFiles(5);
                      setMaxSizeMB(10);
                    }}
                    className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                  >
                    Grant Permission
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Grant Permission Modal */}
        {selectedUser && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg p-6 max-w-md w-full">
              <h3 className="text-xl font-semibold mb-4">Grant Permission</h3>
              <p className="text-gray-600 mb-4">
                User: <span className="font-medium">{selectedUser}</span>
              </p>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Max Files
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="100"
                    value={maxFiles}
                    onChange={(e) => setMaxFiles(parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Max File Size (MB)
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="100"
                    value={maxSizeMB}
                    onChange={(e) => setMaxSizeMB(parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              <div className="flex gap-2 mt-6">
                <button
                  onClick={() => grantPermission(selectedUser)}
                  className="flex-1 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                >
                  Grant
                </button>
                <button
                  onClick={() => setSelectedUser(null)}
                  className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Users List */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">
              All Users ({users.length})
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    User
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Role
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Files
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Permission
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {users.map((user) => (
                  <tr key={user.id}>
                    <td className="px-6 py-4">
                      <div className="font-medium text-gray-900">{user.name}</div>
                      <div className="text-sm text-gray-500">{user.email}</div>
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${
                          user.role === "admin"
                            ? "bg-purple-100 text-purple-800"
                            : "bg-gray-100 text-gray-800"
                        }`}
                      >
                        {user.role}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {user.file_count}
                    </td>
                    <td className="px-6 py-4">
                      {user.role === "admin" ? (
                        <span className="text-sm text-gray-500">Unlimited</span>
                      ) : user.has_permission && user.permission_details ? (
                        <div className="text-sm">
                          <div className="text-green-600 font-medium">✓ Granted</div>
                          <div className="text-gray-500 text-xs">
                            {user.permission_details.max_files} files, {user.permission_details.max_file_size_mb}MB max
                          </div>
                        </div>
                      ) : (
                        <span className="text-sm text-gray-500">None</span>
                      )}
                    </td>
                    <td className="px-6 py-4">
                      {user.role !== "admin" && (
                        <div className="flex gap-2">
                          {!user.has_permission ? (
                            <button
                              onClick={() => setSelectedUser(user.email)}
                              className="text-sm text-purple-600 hover:text-purple-700 font-medium"
                            >
                              Grant
                            </button>
                          ) : (
                            <button
                              onClick={() => revokePermission(user.email)}
                              className="text-sm text-red-600 hover:text-red-700 font-medium"
                            >
                              Revoke
                            </button>
                          )}
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
