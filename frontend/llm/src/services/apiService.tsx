import { Conversation } from "@/types/types";
import { useQuery } from "@tanstack/react-query";

const BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export const getAllConversations = () => {
  return useQuery<Conversation[], Error>({
    queryKey: ["conversations"],
    queryFn: async () => {
      const res = await fetch(`${BASE_URL}/conversations`);
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    },
  });
};

export const getOneConversation = (id: string) => {
  return useQuery<Conversation, Error>({
    queryKey: ["conversations"],
    queryFn: async () => {
      const res = await fetch(`${BASE_URL}/conversations/${id}`);
      if (!res.ok) {
        throw new Error("Network response was not ok");
      }
      return res.json();
    },
  });
};
