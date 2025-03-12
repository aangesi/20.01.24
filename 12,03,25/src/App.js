import React, { useState, useEffect } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000");

function App() {
    const [username, setUsername] = useState("");
    const [message, setMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [selectedImage, setSelectedImage] = useState(null);
    const [showFullImage, setShowFullImage] = useState(false);

    useEffect(() => {
        socket.on("message", (data) => {
            setMessages((prev) => [...prev, { type: "text", ...data }]);
        });

        socket.on("image", (data) => {
            setMessages((prev) => [...prev, { type: "image", ...data }]);
        });

        socket.on("user_joined", (data) => {
            setMessages((prev) => [...prev, { type: "system", message: `🔵 ${data.username} joined the chat` }]);
        });

        socket.on("user_left", (data) => {
            setMessages((prev) => [...prev, { type: "system", message: `🔴 ${data.username} left the chat` }]);
        });

        return () => {
            socket.off("message");
            socket.off("image");
            socket.off("user_joined");
            socket.off("user_left");
        };
    }, []);

    const joinChat = () => {
        if (username.trim()) {
            socket.emit("join", username);
        }
    };

    const sendMessage = () => {
        if (username.trim() && message.trim()) {
            socket.emit("message", { message });
            setMessage("");
        }
    };

    const sendImage = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                socket.emit("image", { image: reader.result });
            };
            reader.readAsDataURL(file);
        }
    };

    const addEmoji = (emoji) => {
        setMessage((prev) => prev + emoji);
    };

    return (
        <div style={{ textAlign: "center", fontFamily: "Arial", padding: "20px" }}>
            <h2>🔥 Chat Room 🔥</h2>

            {/* Увеличенное окно чата */}
            <div style={{
                height: "500px", width: "70%", overflowY: "auto", border: "2px solid #333",
                padding: "15px", margin: "20px auto", background: "#f9f9f9", borderRadius: "10px"
            }}>
                {messages.map((msg, index) => (
                    <div key={index}>
                        {msg.type === "text" && <p><strong>{msg.username}:</strong> {msg.message}</p>}
                        {msg.type === "image" && (
                            <p>
                                <strong>{msg.username}:</strong> <br />
                                <img 
                                    src={msg.image} 
                                    alt="Sent by user" 
                                    style={{ maxWidth: "250px", cursor: "pointer", borderRadius: "5px" }}
                                    onClick={() => { setSelectedImage(msg.image); setShowFullImage(true); }}
                                />
                            </p>
                        )}
                        {msg.type === "system" && <p style={{ fontStyle: "italic", color: "gray" }}>{msg.message}</p>}
                    </div>
                ))}
            </div>

            {/* Поля ввода */}
            <input 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                placeholder="Enter your name" 
                style={{ padding: "10px", margin: "5px", width: "200px" }}
            />
            <button onClick={joinChat} style={{ padding: "10px 15px", cursor: "pointer" }}>Join</button>

            <br /><br />

            <input 
                value={message} 
                onChange={(e) => setMessage(e.target.value)} 
                placeholder="Type a message" 
                style={{ padding: "10px", width: "60%", marginRight: "10px" }}
            />
            <button onClick={sendMessage} style={{ padding: "10px 15px", cursor: "pointer" }}>Send</button>

            {/* БОЛЬШЕ СМАЙЛИКОВ (увеличенные кнопки) */}
            <div style={{ marginTop: "10px" }}>
                {["😊", "😂", "🤣", "❤️", "😍", "😎", "👍", "👎", "🎉", "💯", "🔥", "🤯", "🧐", "💀", "💤", "🥳"].map((emoji) => (
                    <button key={emoji} onClick={() => addEmoji(emoji)} style={{ 
                        fontSize: "24px", margin: "5px", padding: "5px 10px", cursor: "pointer" 
                    }}>
                        {emoji}
                    </button>
                ))}
            </div>

            {/* Отправка изображения */}
            <input type="file" accept="image/*" onChange={sendImage} style={{ marginTop: "10px" }} />

            {/* Полноэкранное изображение */}
            {showFullImage && selectedImage && (
                <div style={{
                    position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
                    background: "rgba(0,0,0,0.8)", display: "flex",
                    justifyContent: "center", alignItems: "center"
                }} onClick={() => setShowFullImage(false)}>
                    <img src={selectedImage} alt="Full size" style={{ maxWidth: "90%", maxHeight: "90%" }} />
                </div>
            )}
        </div>
    );
}

export default App;
