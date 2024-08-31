import {
  Conversation,
  CreateConversationPayload,
  QueryResult,
} from "@/types/types";
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

export const getOneConversation = async (id: string): Promise<Conversation> => {
  const res = await fetch(`${BASE_URL}/conversations/${id}`);
  if (!res.ok) {
    throw new Error("Network response was not ok");
  }
  return res.json();
};

export const postQuery = async (
  id: string,
  payload: any
): Promise<QueryResult> => {
  console.log(payload);
  const res = await fetch(`${BASE_URL}/queries?id=${id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Network response was not ok");
  }

  return res.json();
};

export const createConversation = async (
  payload: CreateConversationPayload
): Promise<string> => {
  const { name, temperature, max_tokens } = payload;

  const params: { temperature?: number; max_tokens?: number } = {};
  if (temperature !== undefined) {
    params.temperature = temperature;
  }
  if (max_tokens !== undefined) {
    params.max_tokens = max_tokens;
  }

  const res = await fetch(`${BASE_URL}/conversations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      params: Object.keys(params).length ? params : {},
    }),
  });

  if (!res.ok) {
    throw new Error("Network response was not ok");
  }

  return res.json();
};

export const updateConversation = async (
  id: string,
  payload: CreateConversationPayload
) => {
  const { name, temperature, max_tokens } = payload;

  const params: { temperature?: number; max_tokens?: number } = {};
  if (temperature !== undefined) {
    params.temperature = temperature;
  }
  if (max_tokens !== undefined) {
    params.max_tokens = max_tokens;
  }

  const res = await fetch(`${BASE_URL}/conversations/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      name: name,
      params: Object.keys(params).length ? params : {},
    }),
  });

  if (!res.ok) {
    throw new Error("Network response was not ok");
  }
};

export const deleteConversation = async (id: string) => {
  const res = await fetch(`${BASE_URL}/conversations/${id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!res.ok) {
    throw new Error("Network response was not ok");
  }
};
