import { useCallback } from "react";
import { embedDashboard } from "@superset-ui/embedded-sdk";

const fetchGuestToken = async () => {
  await fetch("http://localhost:8088/api/v1/security/login", {
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
  }).catch((error) => console.log(error));

  await fetch("http://localhost:8088/api/v1/security/guest_token", {
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
};

export const useSupersetEmbed = (id) => {
  const [mounted, setMounted] = useState(false);

  return async (mountPoint) => {
    if (!mountPoint || mounted) return;

    await embedDashboard({
      id,
      supersetDomain: "https://....",
      mountPoint,
      fetchGuestToken,
      // dashboardUiConfig: {},
      // debug: true,
    });

    setMounted(true);
  };
};

export const SupersetExampleDashboard = () => {
  const embed = useSupersetEmbed("your-dashboard-id-here");

  return <div ref={embed} />;
};
