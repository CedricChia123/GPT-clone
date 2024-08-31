import React, { useState } from "react";
import {
  Modal,
  TextInput,
  NumberInput,
  Button,
  Checkbox,
  Group,
} from "@mantine/core";
import { useQueryClient } from "@tanstack/react-query";
import { createConversation } from "@/services/apiService";
import { CreateConversationPayload } from "@/types/types";

interface CreateModalProps {
  opened: boolean;
  onClose: () => void;
}

const CreateModal: React.FC<CreateModalProps> = ({ opened, onClose }) => {
  const [name, setName] = useState("");
  const [includeTemperature, setIncludeTemperature] = useState(false);
  const [includeMaxTokens, setIncludeMaxTokens] = useState(false);
  const [temperature, setTemperature] = useState<any>(0.5);
  const [maxTokens, setMaxTokens] = useState<any>(100);

  const queryClient = useQueryClient();

  const handleSubmit = async () => {
    if (!name) {
      alert("Please fill in the conversation name");
      return;
    }

    const payload: CreateConversationPayload = { name };

    if (includeTemperature && temperature !== undefined) {
      payload.temperature = temperature;
    }

    if (includeMaxTokens && maxTokens !== undefined) {
      payload.max_tokens = maxTokens;
    }

    try {
      await createConversation(payload);
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      setIncludeMaxTokens(false);
      setIncludeTemperature(false);
      setMaxTokens(null);
      setTemperature(null);
      setName("");
      onClose();
    } catch (error) {
      console.error("Error creating conversation:", error);
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title="Create New Conversation">
      <TextInput
        label="Conversation Name"
        placeholder="Enter conversation name"
        value={name}
        onChange={(event) => setName(event.currentTarget.value)}
        required
      />

      <Checkbox
        label="Include Temperature"
        checked={includeTemperature}
        onChange={(event) => setIncludeTemperature(event.currentTarget.checked)}
        style={{ marginTop: "15px" }}
      />
      <NumberInput
        label="Temperature"
        placeholder="Enter temperature (0 to 1)"
        value={temperature}
        onChange={(value) => setTemperature(value)}
        min={0}
        max={1}
        step={0.1}
        disabled={!includeTemperature}
      />

      <Checkbox
        label="Include Max Tokens"
        checked={includeMaxTokens}
        onChange={(event) => setIncludeMaxTokens(event.currentTarget.checked)}
        style={{ marginTop: "15px" }}
      />
      <NumberInput
        label="Max Tokens"
        placeholder="Enter max tokens"
        value={maxTokens}
        onChange={(value) => setMaxTokens(value)}
        min={1}
        disabled={!includeMaxTokens}
      />

      <Button onClick={handleSubmit} style={{ marginTop: "20px" }}>
        Create Conversation
      </Button>
    </Modal>
  );
};

export default CreateModal;
