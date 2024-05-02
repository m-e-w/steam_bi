import React from "react";
import { embedDashboard } from "@superset-ui/embedded-sdk";


//c7345ecf-0595-442c-b65c-afd3216ff6a7
embedDashboard({
  id: "c7345ecf-0595-442c-b65c-afd3216ff6a7", // given by the Superset embedding UI
  supersetDomain: "https://localhost:8088",
  mountPoint: document.getElementById("superset-container"), // html element in which iframe render
  fetchGuestToken: () => token,
  dashboardUiConfig: { hideTitle: true },
});
const SupersetDashboard = ({ embedDashboard }) => (
  <iframe src={embedDashboard} width="100%" height="600" frameBorder="0"></iframe>
);

export default SupersetDashboard;
