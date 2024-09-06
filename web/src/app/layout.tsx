import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Header from "@/components/header";
import Footer from "@/components/footer";
import ThemeContextProvider from "../../context/theme-context";

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
    <html lang="en" className="!scroll-smooth">
      <body className={`${inter.className}`}>
        <ThemeContextProvider>
          <Header /> {children} <Footer />
        </ThemeContextProvider>
      </body>
    </html>
  );
}
