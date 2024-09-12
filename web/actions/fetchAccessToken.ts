"use server";

const supersetID = process.env.SUPERSET_EMBED_ID ?? "";

const fetchAccessToken = async (): Promise<string | undefined> => {
  try {
    const body = {
      username: "admin",
      password: "admin",
      provider: "db",
      refresh: true,
    };

    const response = await fetch(
      "http://localhost:8088/api/v1/security/login",
      {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    const jsonResponse = await response.json();
    return jsonResponse?.access_token;
  } catch (error) {
    console.error(error);
  }
};

const fetchGuestToken = async (): Promise<string | undefined> => {
  const accessToken = await fetchAccessToken();
  try {
    const body = {
      resources: [
        {
          type: "dashboard",
          id: supersetID,
        },
      ],
      rls: [],
      user: {
        username: "guest",
        first_name: "Guest",
        last_name: "User",
      },
    };
    const response = await fetch(
      "http://localhost:8088/api/v1/security/guest_token",
      {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );
    const jsonResponse = await response.json();
    return jsonResponse?.token;
  } catch (error) {
    console.error(error);
  }
};
