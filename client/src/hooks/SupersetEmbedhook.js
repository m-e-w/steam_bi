import { useState } from "react";
import { embedDashboard } from "@superset-ui/embedded-sdk";

const fetchGuestToken = async () => {
  try {
    const adminResponse = await fetch("http://localhost:8088/api/v1/security/login", {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: {
        password: "admin",
        provider: "db",
        refresh: true,
        username: "admin",
      },
    });
    const adminData = await adminResponse.json();
    console.log(adminData);
    const adminToken = adminData.admin;
    const guestResponse = await fetch("http://localhost:8088/api/v1/security/guest_token", {
      method: "POST",
      mode: "cors",
      authorization: adminToken,
      headers: {
        "Content-Type": "application/json",
      },
      body: {
        user:{
          username: "guest",
          first_name: "Guest User",
          last_name: "Guest User",
          resources: [{
            type: "dashboard",
            id: "8cbc3302-4594-4d1e-8638-a18cf68bb172"
          }],
        }
      },
    });
    const guestData = await guestResponse.json();
    console.log(guestData);
    return guestData.token;
  } catch (err) {
    console.log("Something went wrong...");
    console.log(err);
  }
};

export const useSupersetEmbed = (id) => {
  const [mounted, setMounted] = useState(false);

  return async (mountPoint) => {
    if (!mountPoint || mounted) return;

    await embedDashboard({
      id,
      supersetDomain: "http://localhost:8088",
      mountPoint,
      fetchGuestToken,
      // dashboardUiConfig: {},
      // debug: true,
    });

    setMounted(true);
  };
};

export const SupersetExampleDashboard = () => {
  const embed = useSupersetEmbed("8cbc3302-4594-4d1e-8638-a18cf68bb172");

  return <div ref={embed} />;
};
