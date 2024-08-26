"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import React from "react";
import { Sheet, SheetContent, SheetTrigger } from "./ui/sheet";
import { Button } from "./ui/button";
import { GamepadIcon, MenuIcon } from "lucide-react";
import { Darkmode } from "./darkmode";

export default function Header() {
  return (
    <motion.header
      className="fixed top-0 z-50 w-full bg-background/80 backdrop-blur-sm border-b"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
    >
      <div className="container flex h-16 items-center justify-between md:px-6 border-opacity-40">
        <Link
          href="#home"
          className="flex items-center gap-1 text-lg text-primary"
          prefetch={false}
        >
          <GamepadIcon />
          Steam-Set
        </Link>
        <nav>
          <ul className="text-muted-foreground hidden items-center gap-7 sm:flex">
            <li>
              <Darkmode />
            </li>
          </ul>
        </nav>
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="outline" size="icon" className="sm:hidden">
              <MenuIcon className="h-6 w-6" />
              <span className="sr-only">Toggle navigation</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="md:hidden"></SheetContent>
        </Sheet>
      </div>
    </motion.header>
  );
}
