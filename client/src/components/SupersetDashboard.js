import React from "react";
//import { embedDashboard } from "@superset-ui/embedded-sdk";

const SupersetDashboard = ({ embedDashboard }) => (
  <iframe title="supersetDashboard" src="http://localhost:8088/superset/dashboard/p/apL5qnEknAV/" width="100%" height="600" frameBorder="0"></iframe>
);

export default SupersetDashboard;
