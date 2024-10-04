"use client";

import { useState, useEffect } from "react";
import { SunIcon } from "lucide-react";
import { MoonIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";

export default function ThemeSwitch() {
  const [mounted, setMounted] = useState(false);
  const { setTheme, resolvedTheme } = useTheme();
  useEffect(() => setMounted(true), []);
  if (!mounted)
    return (
      <Button variant="outline" size="icon">
        <div className="h-5 w-5 animate-spin rounded-full border-b-2 border-border"></div>
      </Button>
    );
  else
    return (
      <div>
        {resolvedTheme === "dark" ? (
          <Button
            variant="outline"
            size="icon"
            onClick={() => setTheme("light")}
          >
            <SunIcon className="h-4 w-4" />
          </Button>
        ) : (
          <Button
            variant="outline"
            size="icon"
            onClick={() => setTheme("dark")}
          >
            <MoonIcon className="h-4 w-4" />
          </Button>
        )}
      </div>
    );
}
