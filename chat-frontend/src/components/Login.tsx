import { useState, type FormEvent } from "react";
import { useAuth } from "../contexts/AuthContext";

export default function Login() {
    const { loginUser } = useAuth();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleSubmit(event: FormEvent) {
        event.preventDefault();

        setError("");
        setLoading(true);

        try {
            await loginUser({
                username,
                password,
            });
        } catch {
            setError("Invalid username or password.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit}>
            <h1>Login</h1>

            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(event) =>
                    setUsername(event.target.value)
                }
            />

            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(event) =>
                    setPassword(event.target.value)
                }
            />

            <button type="submit" disabled={loading}>
                {loading ? "Logging in..." : "Login"}
            </button>

            {error && <p>{error}</p>}
        </form>
    );
}