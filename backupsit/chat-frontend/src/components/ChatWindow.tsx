import { useEffect, useRef, useState } from "react";

import { useChat } from "../contexts/chatContextValue";
import { useAuth } from "../contexts/AuthContext";

export default function ChatWindow() {
    const {
        messages,
        send,
        typingUsers,
        deliveryStatus,
    } = useChat();

    const { username } = useAuth();

    const [message, setMessage] = useState("");

    const messagesEndRef = useRef<HTMLDivElement | null>(null);

    /*
     * Automatically mark incoming messages as delivered/read.
     *
     * We keep track of messages that have already been processed
     * so React re-renders don't repeatedly send status updates.
     */
    const processedMessagesRef = useRef<Set<number>>(new Set());

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({
            behavior: "smooth",
        });
    }, [messages]);

    useEffect(() => {
        for (const msg of messages) {
            // Ignore our own messages.
            if (msg.user === username) {
                continue;
            }

            // Ignore messages we already processed.
            if (processedMessagesRef.current.has(msg.id)) {
                continue;
            }

            processedMessagesRef.current.add(msg.id);

            // Message reached this client.
            send({
                type: "status_update",
                id: msg.id,
                status: "delivered",
            });

            // Message is currently visible in the chat.
            send({
                type: "status_update",
                id: msg.id,
                status: "read",
            });
        }
    }, [messages, username, send]);

    function handleSend() {
        const content = message.trim();

        if (!content) {
            return;
        }

        send({
            type: "chat_message",
            message: content,
        });

        setMessage("");
    }

    function handleKeyDown(
        event: React.KeyboardEvent<HTMLInputElement>,
    ) {
        if (event.key === "Enter") {
            event.preventDefault();
            handleSend();
        }
    }

    return (
        <div className="chat-window">
            <header className="chat-header">
                <div>
                    <h1>General</h1>
                    <span>Room 1</span>
                </div>

                <span className="connection-status">
                    ● Connected
                </span>
            </header>

            <main className="message-list">
                {messages.length === 0 ? (
                    <div className="empty-chat">
                        <h2>No messages yet</h2>
                        <p>Send the first message.</p>
                    </div>
                ) : (
                    messages.map((msg) => {
                        const isOwnMessage =
                            msg.user === username;

                        const status =
                            deliveryStatus[msg.id];

                        return (
                            <div
                                className={
                                    isOwnMessage
                                        ? "message message-own"
                                        : "message message-other"
                                }
                                key={msg.id}
                            >
                                <div className="message-user">
                                    {msg.user}
                                </div>

                                <div className="message-bubble">
                                    <div className="message-content">
                                        {msg.content}
                                    </div>

                                    <div className="message-time">
                                        {new Date(
                                            msg.timestamp,
                                        ).toLocaleTimeString([], {
                                            hour: "numeric",
                                            minute: "2-digit",
                                        })}

                                        {isOwnMessage && status && (
                                            <span className="message-status">
                                                {status === "read"
                                                    ? " ✓✓"
                                                    : " ✓"}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        );
                    })
                )}

                <div ref={messagesEndRef} />
            </main>

            {typingUsers.size > 0 && (
                <div className="typing-indicator">
                    Someone is typing...
                </div>
            )}

            <footer className="message-input">
                <input
                    type="text"
                    placeholder="Type a message..."
                    value={message}
                    onChange={(event) =>
                        setMessage(event.target.value)
                    }
                    onKeyDown={handleKeyDown}
                />

                <button
                    type="button"
                    onClick={handleSend}
                    disabled={!message.trim()}
                >
                    Send
                </button>
            </footer>
        </div>
    );
}