import React, { useState } from "react";

function SteamIDForm() {
  const [steamID, setSteamID] = useState("");

  const handleClick = () => {
    const steamIdJson = { steamid: steamID };
    const response = fetch("/api/1.0/task/steam/", {
      method: "POST",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(steamIdJson),
    }).catch((error) => console.log(error));

    if (response.status === 200) {
      console.log(response);
    }
  };

  return (
    <form>
      <input
        placeholder="SteamID"
        value={steamID}
        onChange={(e) => setSteamID(e.target.value)}
      />
      <button type="button" onClick={handleClick}>
        Submit
      </button>
    </form>
  );
}

export default SteamIDForm;
