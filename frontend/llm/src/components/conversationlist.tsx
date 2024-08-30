import React from "react";
import { Paper, Text } from "@mantine/core";
import { Conversation } from "@/types/types";
import { getAllConversations } from "@/services/apiService";

interface ConversationListProps {
  onSelectConversation: (conversationId: string) => void;
}

const ConversationList: React.FC<ConversationListProps> = ({
  onSelectConversation,
}) => {
  const { data: conversations, error, isLoading } = getAllConversations();

  return (
    <Paper
      shadow="xs"
      className="p-4"
      style={{ height: "100%", overflow: "auto" }}
    >
      {conversations?.map((conversation: Conversation) => (
        <Text
          key={conversation.id}
          className="p-2"
          style={{ cursor: "pointer" }}
          onClick={() => onSelectConversation(conversation.id)}
        >
          {conversation.name}
        </Text>
      ))}
    </Paper>
  );
};

export default ConversationList;
