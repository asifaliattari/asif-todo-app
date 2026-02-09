import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "@/components/Providers";

export const metadata: Metadata = {
  title: "TaskFlow - Asif Ali AstolixGen",
  description: "AI-Powered Project Management System by Asif Ali AstolixGen for GIAIC Hackathon",
  authors: [{ name: "Asif Ali AstolixGen" }],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased min-h-screen bg-gray-950">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
