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
    return jsonResponse?.access_token;
  } catch (error) {
    console.error(error);
  }
};

export const fetchCSRFToken = async (
  accessToken: string | undefined
): Promise<string | undefined> => {
  console.log("Authorization Header:", `Bearer ${accessToken}`);
  if (!accessToken) {
    console.error("Access Token is missing, cannot proceed");
    return undefined;
  }

  try {
    const response = await fetch(
      "http://localhost:8088/api/v1/security/csrf_token",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
        credentials: "include",
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
    console.log("CSRF Token:", jsonResponse?.result);
    return jsonResponse?.result;
  } catch (error) {
    console.error(error);
  }
};

export const getGuestToken = async (): Promise<string | undefined> => {
  const accessToken = await fetchAccessToken();
  const csrfToken = await fetchCSRFToken(accessToken);

  if (!accessToken || !csrfToken) {
    console.error("Tokens are missing, cannot proceed");
    return undefined;
  }

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
          "X-CSRFToken": csrfToken,
        },
        credentials: "include",
      }
    );

    if (!response.ok) {
      const errorResponse = await response.text();
      console.error("Failed to fetch guest token:", errorResponse);
      return undefined;
    }

    const jsonResponse = await response.json();
    console.log("Guest Token:", jsonResponse?.token); // Log the guest token
    return jsonResponse?.token;
  } catch (error) {
    console.error(error);
  }
};
