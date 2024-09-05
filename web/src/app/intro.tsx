import React from "react";

export default function Intro() {
  return (
    <section className="w-full py-12 md:py-24 lg:py-32">
      <div className="container space-y-12 px-4 md:px-6">
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className="space-y-2">
            <h2 className="text-3xl font-bold tracking-tighter sm:text-5xl">
              Compare your gaming data with your friends!
            </h2>
            <p className="max-w-[900px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
              Lorem ipsum, dolor sit amet consectetur adipisicing elit. Animi,
              quaerat voluptas laudantium doloribus, commodi itaque nulla
              assumenda beatae totam repudiandae dolor voluptates quas ad
              eveniet. Ullam minima animi quis voluptates.
            </p>
          </div>
        </div>
        <div className="mx-auto grid items-start gap-8 sm:max-w-4xl sm:grid-cols-2 md:gap-12 lg:max-w-5xl lg:grid-cols-3">
          <div className="grid gap-1">
            <h3 className="text-lg font-bold">1. Get your Steam ID</h3>
            <p className="text-sm text-muted-foreground">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Earum
              quisquam, praesentium rem accusantium nam illo vitae? Magnam
              reprehenderit voluptate distinctio.
            </p>
          </div>
          <div className="grid gap-1">
            <h3 className="text-lg font-bold">
              2. Enter your Steam ID in the{" "}
            </h3>
            <p className="text-sm text-muted-foreground">
              Lorem ipsum dolor sit amet consectetur adipisicing elit. Earum
              quisquam, praesentium rem accusantium nam illo vitae? Magnam
              reprehenderit voluptate distinctio.
            </p>
          </div>
          <div className="grid gap-1">
            <h3 className="text-lg font-bold">Connect with the Community</h3>
            <p className="text-sm text-muted-foreground">
              Lorem ipsum dolor sit amet consectetur, adipisicing elit. Nam,
              minus temporibus velit eligendi nobis ipsa. Qui, aperiam? Debitis,
              voluptatibus laboriosam!
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
