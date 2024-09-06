import React from "react";
import Link from "next/link";
import { Github } from "lucide-react";

export default function Footer() {
  return (
    <footer className="fixed bottom-0 z-50 w-full bg-background/80 backdrop-blur-sm border-t">
      <div className="container flex h-16 items-center justify-between md:px-6 border-opacity-40">
        <p className="text-xs text-muted-foreground">
          &copy; 2024 Matt Walls/Nick Giuliani
        </p>
        <nav className="sm:ml-auto flex gap-4 sm:gap-6">
          <Link
            href="https://github.com/thereeling"
            target="_blank"
            prefetch={false}
          >
            <Github className="h-5 w-5" />
            <span className="sr-only">Github</span>
          </Link>
        </nav>
      </div>
    </footer>
  );
}
