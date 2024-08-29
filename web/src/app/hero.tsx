import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Hero() {
  return (
    <section className="w-full pt-32">
      <div className="px-4 md:px-6 space-y-10 xl:space-y-16">
        <div className="mx-auto grid max-w-[750px] gap-4 px-4 sm:px-6 md:px-10 md:gap-16">
          <div>
            <h1 className="lg:leading-tighter text-3xl font-bold tracking-tighter pb-10 sm:text-4xl md:text-5xl xl:text-[3.4rem] 2xl:text-[3.75rem]">
              A Data Visualization tool for your Steam Account.
            </h1>
            <p className="mx-auto max-w-[700px] text-muted-foreground md:text-xl">
              Enter your Steam ID to view personalized insights and data of your
              Steam account. Powered by Superset.
            </p>
            <form className="flex gap-2 mt-6">
              <Input
                type="text"
                placeholder="Enter your Steam ID"
                className="max-w-lg flex-1"
              />
              <Button type="submit">Submit</Button>
            </form>
          </div>

        </div>
      </div>
    </section>
  );
}
