import { getGuestToken } from "../../../actions/fetchAccessToken";
import SupersetDashboardClient from "@/components/superset-dashboard-client";

export default async function Dashboard() {
  const token = await getGuestToken(); 
  const supersetID = process.env.SUPERSET_EMBED_ID ?? ""; 

  if (!token) {
    return <div>Failed to load dashboard. Please try again later.</div>;
  }

  return (
    <section>
      <SupersetDashboardClient token={token} supersetID={supersetID} />
    </section>
  );
}