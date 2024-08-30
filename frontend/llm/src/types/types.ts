// Define interfaces for the messages and props
export interface Message {
  text: string;
  isBot: boolean;
}

export interface Conversation {
  id: string;
  name: string;
}

export interface ConversationListProps {
  onSelectConversation: (conversationId: number) => void;
}
