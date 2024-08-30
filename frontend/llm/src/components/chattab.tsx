"use client";

import { useState, useEffect, useRef, useLayoutEffect } from "react";
import { TextInput, Button, Paper, Text, Stack } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import { getOneConversation, postQuery } from "@/services/apiService";
import { ConversationMessage, Message, Conversation } from "@/types/types";
import { IconArrowRight } from "@tabler/icons-react";

interface ChatTabProps {
  conversationId: string | null;
}

export default function ChatTab({ conversationId }: ChatTabProps) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSending, setIsSending] = useState(false);
  const endOfMessagesRef = useRef<null | HTMLDivElement>(null);

  const {
    data: conversation,
    error,
    isLoading,
  } = useQuery({
    queryKey: ["conversation", conversationId],
    queryFn: () => getOneConversation(conversationId as string),
    enabled: !!conversationId,
  });

  useEffect(() => {
    if (conversation) {
      const formattedMessages: Message[] =
        conversation.messages?.map((msg: ConversationMessage) => ({
          text: msg.content,
          isBot: msg.role === "assistant",
        })) || [];
      setMessages(formattedMessages);
    } else {
      setMessages([]);
    }
  }, [conversation]);

  const handleSend = async () => {
    if (input.trim() === "" || !conversationId || isSending) return;

    setIsSending(true);

    const newMessages = [...messages, { text: input, isBot: false }];
    setMessages(newMessages);

    try {
      const response = await postQuery(conversationId, {
        role: "user",
        content: input,
      });

      newMessages.push({
        text: response.response,
        isBot: true,
      });

      setMessages(newMessages);
    } catch (error) {
      console.error("Error sending query:", error);
      newMessages.push({
        text: "An error occurred while sending your message.",
        isBot: true,
      });
      setMessages(newMessages);
    } finally {
      setIsSending(false);
    }

    setInput("");
  };

  useLayoutEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages.length]);

  return (
    <div style={{ position: "fixed", bottom: 10, width: "50%" }}>
      <Paper
        shadow="xs"
        className="overflow-hidden"
        style={{
          height: "90vh",
          display: "flex",
          flexDirection: "column-reverse",
          padding: "10px",
        }}
      >
        <Stack style={{ flex: 1, overflowY: "auto", overflowX: "auto" }}>
          {isLoading && <Text>Loading...</Text>}
          {error && <Text c="red">Failed to load conversation</Text>}
          {messages.map((message, index) => (
            <Text key={index} c={message.isBot ? "blue" : "black"}>
              {message.text}
            </Text>
          ))}
          <div ref={endOfMessagesRef} />
        </Stack>
      </Paper>
      <div style={{ display: "flex", alignItems: "center", marginTop: "8px" }}>
        <TextInput
          placeholder="Type your message..."
          value={input}
          style={{ flex: 1 }}
          onChange={(event) => setInput(event.currentTarget.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              handleSend();
            }
          }}
        />
        <Button
          variant="filled"
          onClick={handleSend}
          color="blue"
          style={{ marginLeft: "8px" }}
          disabled={isSending}
        >
          <IconArrowRight size={16} />
        </Button>
      </div>
    </div>
  );
}
