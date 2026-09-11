import {
    createContext,
    useCallback,
    useContext,
    useEffect,
    useMemo,
    useState,
    type ReactNode,
} from "react";

import { login, refreshAccessToken } from "../api/auth";
import type { LoginCredentials } from "../types/auth";

interface AuthContextValue {
    accessToken: string | null;
    refreshToken: string | null;
    username: string | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    loginUser: (credentials: LoginCredentials) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(
    undefined,
);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [accessToken, setAccessToken] = useState<string | null>(
        () => localStorage.getItem("access_token"),
    );

    const [refreshToken, setRefreshToken] = useState<string | null>(
        () => localStorage.getItem("refresh_token"),
    );

    const [username, setUsername] = useState<string | null>(
        () => localStorage.getItem("username"),
    );

    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function restoreSession() {
            const storedRefresh =
                localStorage.getItem("refresh_token");

            if (!storedRefresh) {
                setIsLoading(false);
                return;
            }

            try {
                const data =
                    await refreshAccessToken(storedRefresh);

                setAccessToken(data.access);

                localStorage.setItem(
                    "access_token",
                    data.access,
                );
            } catch {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                localStorage.removeItem("username");

                setAccessToken(null);
                setRefreshToken(null);
                setUsername(null);
            } finally {
                setIsLoading(false);
            }
        }

        restoreSession();
    }, []);

    const loginUser = useCallback(
        async (credentials: LoginCredentials) => {
            const data = await login(credentials);

            localStorage.setItem(
                "access_token",
                data.access,
            );

            localStorage.setItem(
                "refresh_token",
                data.refresh,
            );

            localStorage.setItem(
                "username",
                credentials.username,
            );

            setAccessToken(data.access);
            setRefreshToken(data.refresh);
            setUsername(credentials.username);
        },
        [],
    );

    const logout = useCallback(() => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("username");

        setAccessToken(null);
        setRefreshToken(null);
        setUsername(null);
    }, []);

    const value = useMemo(
        () => ({
            accessToken,
            refreshToken,
            username,
            isAuthenticated: accessToken !== null,
            isLoading,
            loginUser,
            logout,
        }),
        [
            accessToken,
            refreshToken,
            username,
            isLoading,
            loginUser,
            logout,
        ],
    );

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error(
            "useAuth must be used inside AuthProvider",
        );
    }

    return context;
}