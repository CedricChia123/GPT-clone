"use client";

import { useState, useEffect, useRef } from "react";
import { TextInput, Button, Paper, Text, Stack } from "@mantine/core";

interface Message {
  text: string;
  isBot: boolean;
}

interface ChatTabProps {
  conversationId: string | null;
}

export default function ChatTab({ conversationId }: ChatTabProps) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const endOfMessagesRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    if (conversationId) {
      setMessages([
        { text: `Loaded conversation ${conversationId}`, isBot: true },
      ]);
    }
  }, [conversationId]);

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessages = [...messages, { text: input, isBot: false }];
    setTimeout(() => {
      newMessages.push({ text: `You said: "${input}"`, isBot: true });
      setMessages(newMessages);
    }, 1000);

    setInput("");
    setMessages(newMessages);
  };

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div style={{ position: "fixed", bottom: 10, width: "50%" }}>
      <Paper
        shadow="xs"
        className="overflow-hidden"
        style={{
          height: "90vh",
          display: "flex",
          flexDirection: "column-reverse",
        }}
      >
        <Stack style={{ flex: 1, overflowY: "auto" }}>
          {messages.map((message, index) => (
            <Text key={index} color={message.isBot ? "blue" : "black"}>
              {message.text}
            </Text>
          ))}
          <div ref={endOfMessagesRef} />
        </Stack>
      </Paper>
      <TextInput
        placeholder="Type your message..."
        value={input}
        style={{ marginTop: "8px" }}
        onChange={(event) => setInput(event.currentTarget.value)}
        rightSection={
          <Button onClick={handleSend} color="blue">
            Send
          </Button>
        }
        onKeyPress={(event) => {
          if (event.key === "Enter") {
            handleSend();
          }
        }}
      />
    </div>
  );
}
