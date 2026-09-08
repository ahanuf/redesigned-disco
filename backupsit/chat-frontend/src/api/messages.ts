import apiClient from "./client";
import type { ChatMessage } from "../types/chat";

export async function getRoomMessages(
    roomId: string,
): Promise<ChatMessage[]> {
    const response = await apiClient.get<ChatMessage[]>(
        `messages/?room=${encodeURIComponent(roomId)}`,
    );

    return response.data;
}