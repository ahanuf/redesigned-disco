import {
    useEffect,
    useState,
    useCallback,
    type ReactNode,
} from "react";

import useWebSocket from "../hooks/useWebSocket";
import { getRoomMessages } from "../api/messages";

import type {
    IncomingEvent,
    ChatMessage,
    DeliveryStatusMap,
} from "../types/chat";

import { ChatContext } from "./chatContextValue";

interface ChatProviderProps {
    roomName: string;
    children: ReactNode;
}

export function ChatProvider({
    roomName,
    children,
}: ChatProviderProps) {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [typingUsers, setTypingUsers] = useState<Set<string>>(new Set());
    const [deliveryStatus, setDeliveryStatus] =
        useState<DeliveryStatusMap>({});

    // const [historyLoading, setHistoryLoading] = useState(true);
    // const [historyError, setHistoryError] = useState<string | null>(null);

    useEffect(() => {
        let cancelled = false;

        async function loadHistory() {
            try {
                const history = await getRoomMessages(roomName);

                if (!cancelled) {
                    setMessages(history);
                }
            } catch (error) {
                console.error("Failed to load message history:", error);
            }
        }

        loadHistory();

        return () => {
            cancelled = true;
        };
    }, [roomName]);

    const handleEvent = useCallback(
        (data: IncomingEvent) => {
            console.log("CHAT EVENT RECEIVED:", data);

            if (!("type" in data)) {
                setMessages((msgs) => {
                    // Prevent duplicate messages.
                    if (msgs.some((msg) => msg.id === data.id)) {
                        return msgs;
                    }

                    return [...msgs, data];
                });

                return;
            }

            switch (data.type) {
                case "connection":
                    console.log("WebSocket connected:", data.room_id);
                    break;

                case "typing":
                    setTypingUsers((users) => {
                        const updated = new Set(users);

                        if (data.status === "started") {
                            updated.add(data.username);
                        } else {
                            updated.delete(data.username);
                        }

                        return updated;
                    });
                    break;

                case "status":
                    setDeliveryStatus((statuses) => ({
                        ...statuses,
                        [data.id]: data.status,
                    }));
                    break;

                case "error":
                    console.error(
                        "Chat WebSocket error:",
                        data.message,
                    );
                    break;
            }
        },
        [],
    );

    const { send } = useWebSocket(roomName, handleEvent);

    return (
        <ChatContext.Provider
            value={{
                messages,
                typingUsers,
                deliveryStatus,
                send,
            }}
        >
            {children}
        </ChatContext.Provider>
    );
}