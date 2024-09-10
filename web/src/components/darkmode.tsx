"use client";

import React, { useContext } from "react";
import { SunIcon } from "lucide-react";
import { MoonIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useTheme } from "../../context/theme-context";

export function Darkmode() {
const {theme, toggleTheme} =  useTheme();
  return (
    <Button variant="outline" size="icon" onClick={toggleTheme}>
      {theme === "dark" ? (
        <SunIcon className="h-4 w-4" />
      ) : (
        <MoonIcon className="h-4 w-4" />
      )}
    </Button>
  );
}
