import React from "react";
import Hero from "./hero";

export default function Home() {
  return (
    <div className="flex flex-col min-h-dvh">
      <main className="flex-1">
        <Hero />
      </main>
    </div>
  );
}
