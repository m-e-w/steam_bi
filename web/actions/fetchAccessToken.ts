"use server";

const supersetID = process.env.SUPERSET_EMBED_ID ?? "";

export const fetchAccessToken = async (): Promise<string | undefined> => {
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

    if (!response.ok) {
      console.error("Failed to log in:", response.status, response.statusText);
      return undefined;
    }

    const jsonResponse = await response.json();
    console.log("Access Token:", jsonResponse?.access_token); // for testing
    return jsonResponse?.access_token;
  } catch (error) {
    console.error(error);
  }
};

export const fetchCSRFToken = async (
  accessToken: string | undefined
): Promise<string | undefined> => {
  try {
    const response = await fetch(
      "http://localhost:8088/api/v1/security/csrf_token",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      }
    );

    if (!response.ok) {
      console.error(
        "Failed to GET CSRF Token:",
        response.status,
        response.statusText
      );
      return undefined;
    }

    const jsonResponse = await response.json();
    console.log("CSRF Token:", jsonResponse?.result); // for testing
    return jsonResponse?.result;
  } catch (error) {
    console.error(error);
  }
};

export const getGuestToken = async (): Promise<string | undefined> => {
  const accessToken = await fetchAccessToken();
  const csrfToken = await fetchCSRFToken(accessToken);
  try {
    const body = {
      user: {
        username: "guest",
        first_name: "Guest",
        last_name: "User",
      },
      resources: [
        {
          type: "dashboard",
          id: supersetID,
        },
      ],
      rls: [],
    };
    const response = await fetch(
      "http://localhost:8088/api/v1/security/guest_token",
      {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
          "X-CSRFToken": `${csrfToken}`,
        },
      }
    );
    const responseText = await response.text();
    const jsonResponse = await response.json();
    console.log("Guest Token:", jsonResponse?.token); // Log the guest token
    console.log("Full response:", responseText);
    return jsonResponse?.token;
  } catch (error) {
    console.error(error);
  }
};
