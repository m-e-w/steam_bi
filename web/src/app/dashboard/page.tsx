"use client";
import React, { useEffect } from "react";
import { embedDashboard } from "@superset-ui/embedded-sdk";
import { getGuestToken } from "../../../actions/fetchAccessToken";

const supersetID = process.env.SUPERSET_EMBED_ID ?? "";

export default function Dashboard() {
  const token = getGuestToken();
  console.log(token);
  useEffect(() => {
    const embed = async () => {
      await embedDashboard({
        id: supersetID, // given by the Superset embedding UI
        supersetDomain: "http://localhost:8088",
        mountPoint: document.getElementById("dashboard") as HTMLElement, // html element in which iframe render
        fetchGuestToken: () => token as Promise<string>,
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
