"use client";
import React, { useEffect } from "react";
import { embedDashboard } from "@superset-ui/embedded-sdk";

const supersetID = process.env.SUPERSET_EMBED_ID ?? "";

export default function Dashboard() {
  const getToken = async () => {
    console.log("Fetching guest token...");
    const response = await fetch("/api/guest-token");
    const token = await response.json();
    console.log("Fetched token:", token);
    return token;
  };

  useEffect(() => {
    const embed = async () => {
      await embedDashboard({
        id: supersetID, // given by the Superset embedding UI
        supersetDomain: "http://localhost:8088",
        mountPoint: document.getElementById("dashboard") as HTMLElement, // html element in which iframe render
        fetchGuestToken: () => getToken(),
        dashboardUiConfig: {
          hideTitle: true,
          filters: {
            expanded: true,
          },
          hideChartControls: true,
          hideTab: true,
        },
      });
    };

    if (document.getElementById("dashboard")) {
      embed();
    }
  }, []);
  return (
    <section>
      <div id="dashboard" />
    </section>
  );
}
