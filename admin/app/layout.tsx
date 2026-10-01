import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "LocateX Admin",
  description: "LocateX transportation administration dashboard",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body style={{ fontFamily: "Arial, sans-serif", margin: 0 }}>{children}</body>
    </html>
  );
}
