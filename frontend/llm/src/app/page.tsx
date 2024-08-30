"use client";

import React, { useState } from "react";
import { Container } from "@mantine/core";
import ConversationList from "@/components/conversationlist";
import ChatTab from "@/components/chattab";

const Home: React.FC = () => {
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | null
  >(null);

  const handleSelectConversation = (conversationId: string): void => {
    setSelectedConversationId(conversationId);
  };

  return (
    <Container
      className="p-4"
      style={{
        display: "flex",
        height: "100%",
        width: "100%",
        justifyContent: "center",
      }}
    >
      <div style={{ width: "35%" }}>
        <ConversationList onSelectConversation={handleSelectConversation} />
      </div>
      <div style={{ width: "75%" }}>
        <ChatTab conversationId={selectedConversationId} />
      </div>
    </Container>
  );
};

export default Home;
