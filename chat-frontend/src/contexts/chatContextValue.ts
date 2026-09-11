import {
    createContext,
    useContext,
} from "react";

import type {
    ChatMessage,
    DeliveryStatusMap,
    OutgoingEvent,
} from "../types/chat";

export interface ChatContextValue {
    messages: ChatMessage[];
    typingUsers: Set<string>;
    deliveryStatus: DeliveryStatusMap;
    send: (msg: OutgoingEvent) => void;
}

export const ChatContext =
    createContext<ChatContextValue | undefined>(
        undefined,
    );

export function useChat(): ChatContextValue {
    const context = useContext(ChatContext);

    if (!context) {
        throw new Error(
            "useChat must be used inside ChatProvider",
        );
    }

    return context;
}