import apiClient from "./client";
import type { LoginCredentials, TokenResponse } from "../types/auth";

export async function login(
    credentials: LoginCredentials,
): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>(
        "token/",
        credentials,
    );

    return response.data;
}

export async function refreshAccessToken(
    refresh: string,
): Promise<{ access: string }> {
    const response = await apiClient.post<{ access: string }>(
        "token/refresh/",
        {
            refresh,
        },
    );

    return response.data;
}