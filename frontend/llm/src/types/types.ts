export interface Message {
  text: string;
  isBot: boolean;
}

export interface ConversationMessage {
  role: string;
  content: string;
}

export interface Params {
  temperature: number;
  max_tokens: number;
}

export interface Conversation {
  id: string;
  name: string;
  params?: Params;
  tokens?: number;
  messages?: ConversationMessage[];
}

export interface ConversationListProps {
  onSelectConversation: (conversationId: number) => void;
}

export interface QueryResult {
  id: string;
  response: string;
}

export interface CreateConversationPayload {
  name: string;
  temperature?: number;
  max_tokens?: number;
}
