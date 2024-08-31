import React, { useState } from "react";
import { Button, Container } from "@mantine/core";
import { Conversation } from "@/types/types";
import { getAllConversations } from "@/services/apiService";
import CreateModal from "./createModal";

interface ConversationListProps {
  onSelectConversation: (conversationId: string) => void;
}

const ConversationList: React.FC<ConversationListProps> = ({
  onSelectConversation,
}) => {
  const { data: conversations, error, isLoading } = getAllConversations();
  const [selectedConversationId, setSelectedConversationId] = useState<
    string | null
  >(null);

  const [openModal, setOpenModal] = useState(false);

  const handleSelectConversation = (conversationId: string) => {
    setSelectedConversationId(conversationId);
    onSelectConversation(conversationId);
  };

  const closeModal = () => setOpenModal(false);

  return (
    <>
      <CreateModal opened={openModal} onClose={closeModal} />
      <Container
        className="p-4"
        style={{
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Button
          className="p-2"
          onClick={() => setOpenModal(true)}
          style={{
            cursor: "pointer",
            width: "35ch",
            marginBottom: "1ch",
            marginTop: "1ch",
            marginRight: "10ch",
          }}
          variant="filled"
        >
          + Create Conversation
        </Button>
        {conversations?.map((conversation: Conversation) => (
          <Button
            key={conversation.id}
            className="p-2"
            style={{
              cursor: "pointer",
              width: "35ch",
              marginRight: "10ch",
              marginBottom: "1ch",
            }}
            onClick={() => handleSelectConversation(conversation.id)}
            variant={
              selectedConversationId === conversation.id ? "light" : "outline"
            }
          >
            {conversation.name}
          </Button>
        ))}
      </Container>
    </>
  );
};

export default ConversationList;
