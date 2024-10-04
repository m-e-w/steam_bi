"use client";
import React, { useEffect } from "react";
import { embedDashboard } from "@superset-ui/embedded-sdk";

interface SupersetDashboardProps {
  token: string;
  supersetID: string;
}

const SupersetDashboardClient: React.FC<SupersetDashboardProps> = ({ token, supersetID }) => {
  useEffect(() => {
    const embed = async () => {
      await embedDashboard({
        id: supersetID, 
        supersetDomain: "http://localhost:8088",
        mountPoint: document.getElementById("dashboard") as HTMLElement, 
        fetchGuestToken: () => Promise.resolve(token), 
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
  }, [token, supersetID]);

  return <div id="dashboard" />;
};

export default SupersetDashboardClient;