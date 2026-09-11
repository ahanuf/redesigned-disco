export interface MediaItem {
    id: number;
    message: number | null;
    file: string;
    type: "image" | "audio";
}

export interface ReactionItem {
    id: number;
    message: number;
    user: string;
    emoji: string;
    timestamp: string;
}

export interface ChatMessage {
    id: number;
    room: number;
    user: string;
    content: string;
    timestamp: string;
    delivered: boolean;
    read: boolean;
    ttl: string | null;
    media: MediaItem[];
    reactions: ReactionItem[];
}

export type IncomingEvent =
    | ChatMessage
    | {
        type: "typing";
        user_id: number;
        username: string;
        status: "started" | "stopped";
    }
    | {
        type: "status";
        id: number;
        status: "delivered" | "read";
        user_id: number;
        username: string;
    }
    | {
        type: "connection";
        status: "connected";
        room_id: number;
    }
    | {
        type: "error";
        message: string;
    };

export type OutgoingEvent =
    | {
        type: "chat_message";
        message: string;
        ttl?: number;
    }
    | {
        type: "typing";
        status: "started" | "stopped";
    }
    | {
        type: "status_update";
        id: number;
        status: "delivered" | "read";
    }
    | {
        type: "file";
        media_id: number;
    };

export type DeliveryStatusMap = Record<
    number,
    "delivered" | "read"
>;