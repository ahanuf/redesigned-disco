import {
    useEffect,
    useRef,
    useCallback,
} from "react";

import type {
    IncomingEvent,
    OutgoingEvent,
} from "../types/chat";

import { useAuth } from "../contexts/AuthContext";

export default function useWebSocket(
    roomName: string,
    onEvent: (data: IncomingEvent) => void,
) {
    const socketRef = useRef<WebSocket | null>(null);

    const { accessToken } = useAuth();

    const wsBaseUrl = import.meta.env.VITE_WS_URL;

    const send = useCallback((msg: OutgoingEvent) => {
        const socket = socketRef.current;

        if (!socket) {
            console.warn("WebSocket is not connected.");
            return;
        }

        if (socket.readyState !== WebSocket.OPEN) {
            console.warn("WebSocket is not ready.");
            return;
        }

        socket.send(JSON.stringify(msg));
    }, []);

    useEffect(() => {
        if (!accessToken) {
            return;
        }

        const wsUrl =
            `${wsBaseUrl}${roomName}/?token=${encodeURIComponent(accessToken)}`;

        const socket = new WebSocket(wsUrl);

        socketRef.current = socket;

        socket.onopen = () => {
            console.log(
                `WebSocket connected to room ${roomName}`,
            );
        };

        socket.onmessage = (event: MessageEvent<string>) => {
            try {
                const data = JSON.parse(event.data) as IncomingEvent;
                onEvent(data);
            } catch (error) {
                console.error(
                    "Invalid WebSocket message:",
                    error,
                );
            }
        };

        socket.onerror = (error) => {
            console.error(
                "WebSocket error:",
                error,
            );
        };

        socket.onclose = (event) => {
            console.log(
                `WebSocket closed. Code: ${event.code}`,
            );

            socketRef.current = null;
        };

        return () => {
            socket.close();
            socketRef.current = null;
        };
    }, [
        accessToken,
        roomName,
        wsBaseUrl,
        onEvent,
    ]);

    return { send };
}