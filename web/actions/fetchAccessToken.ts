"use server";

import { cookies } from "next/headers";

const supersetID = process.env.NEXT_PUBLIC_SUPERSET_EMBED_ID;

type TCSRFTokenResponse = {
  csrfToken: string | undefined;
  sessionCookie: string | undefined;
};

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
        credentials: "include",
        cache: "no-store",
      }
    );

    if (!response.ok) {
      console.error("Failed to log in:", response.status, response.statusText);
      return undefined;
    }

    const jsonResponse = await response.json();

    const accessToken = jsonResponse.access_token;

    return accessToken;
  } catch (error) {
    console.error(error);
    return undefined;
  }
};

export const fetchCSRFToken = async (
  accessToken: string | undefined
): Promise<TCSRFTokenResponse> => {
  if (!accessToken) {
    return { csrfToken: undefined, sessionCookie: undefined };
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
      return { csrfToken: undefined, sessionCookie: undefined };
    }

    const jsonResponse = await response.json();
    const sessionCookieArr = await response.headers.getSetCookie();
    const sessionCookie = sessionCookieArr[0];
    return {
      csrfToken: jsonResponse?.result,
      sessionCookie,
    };
  } catch (error) {
    console.error(error);
    return { csrfToken: undefined, sessionCookie: undefined };
  }
};

export const getGuestToken = async (): Promise<string | undefined> => {
  const accessToken = await fetchAccessToken();
  const { csrfToken, sessionCookie } = await fetchCSRFToken(accessToken);
  console.log(`Access Token: ${accessToken}`);
  console.log(`Session Cookie: ${sessionCookie}`);
  console.log(`CSRF Token: ${csrfToken}`);
  console.log(`Superset ID: ${supersetID}`);

  if (!accessToken || !csrfToken || !sessionCookie) {
    console.error("Tokens or Session Cookie are missing, cannot proceed");
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
          Cookie: sessionCookie,
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
    console.log("Guest Token:", jsonResponse?.token); 
    return jsonResponse?.token;
  } catch (error) {
    console.error(error);
  }
};
