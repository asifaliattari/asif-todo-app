import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',

  // Disable telemetry in production
  // productionBrowserSourceMaps: false,
};

export default nextConfig;
