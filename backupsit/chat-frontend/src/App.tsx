import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { ChatProvider } from "./contexts/chatContext";
import Login from "./components/Login";
import ChatWindow from "./components/ChatWindow";

function AppContent() {
    const {
        isAuthenticated,
        isLoading,
    } = useAuth();

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
        return <Login />;
    }

    return (
        <ChatProvider roomName="1">
            <ChatWindow />
        </ChatProvider>
    );
}

export default function App() {
    return (
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    );
}