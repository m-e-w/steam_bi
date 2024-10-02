import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/header";
import Footer from "@/components/footer";
import { Providers } from "./providers";
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Steam-Set",
  description: "An anonymous data vis app for your Steam Account!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.className}`} suppressHydrationWarning>
      <body className={`bg-background dark:bg-background text-foreground dark:text-foreground !scroll-smooth`}>
        <Providers>
          <Header /> {children} <Footer />
        </Providers>
      </body>
    </html>
  );
}
