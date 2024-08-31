import React, { useEffect, useState } from "react";
import {
  Modal,
  TextInput,
  Text,
  NumberInput,
  Button,
  Checkbox,
  Group,
  Tooltip,
} from "@mantine/core";
import { useQueryClient } from "@tanstack/react-query";
import { updateConversation, deleteConversation } from "@/services/apiService";
import { CreateConversationPayload } from "@/types/types";

interface ConfigureModalProps {
  opened: boolean;
  onClose: () => void;
  conversationId: string;
  initialName: string;
  initialTemperature?: number;
  initialMaxTokens?: number;
  onConversationDeleted: () => void;
}

const ConfigureModal: React.FC<ConfigureModalProps> = ({
  opened,
  onClose,
  conversationId,
  initialName,
  initialTemperature,
  initialMaxTokens,
  onConversationDeleted,
}) => {
  useEffect(() => {
    if (!opened) {
      setName(initialName);
      setIncludeTemperature(initialTemperature !== undefined);
      setIncludeMaxTokens(initialMaxTokens !== undefined);
      setTemperature(initialTemperature);
      setMaxTokens(initialMaxTokens);
      setConfirmDelete(false);
    }
  }, [opened, initialName, initialTemperature, initialMaxTokens]);
  const [name, setName] = useState(initialName);
  const [includeTemperature, setIncludeTemperature] = useState(
    initialTemperature !== undefined
  );
  const [includeMaxTokens, setIncludeMaxTokens] = useState(
    initialMaxTokens !== undefined
  );
  const [temperature, setTemperature] = useState<any>(initialTemperature);
  const [maxTokens, setMaxTokens] = useState<any>(initialMaxTokens);
  const [confirmDelete, setConfirmDelete] = useState(false);

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
      await updateConversation(conversationId, payload);
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      queryClient.invalidateQueries({
        queryKey: ["conversation", conversationId],
      });
      setName("");
      setIncludeTemperature(false);
      setIncludeMaxTokens(false);
      setTemperature(null);
      setMaxTokens(null);
      onClose();
    } catch (error) {
      console.error("Error updating conversation:", error);
    }
  };

  const handleDelete = async () => {
    if (!confirmDelete) {
      alert("Please confirm deletion");
      return;
    }

    try {
      await deleteConversation(conversationId);
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      setConfirmDelete(false);
      onConversationDeleted();
      onClose();
    } catch (error) {
      console.error("Error deleting conversation:", error);
    }
  };

  return (
    <Modal opened={opened} onClose={onClose} title={`Edit LLM`}>
      <Tooltip label={initialName} multiline withinPortal>
        <Text
          style={{
            whiteSpace: "nowrap",
            overflow: "hidden",
            textOverflow: "ellipsis",
            maxWidth: "100%",
          }}
        >
          <strong>Name:</strong> {initialName}
        </Text>
      </Tooltip>
      <Text>
        <strong>Temperature:</strong>{" "}
        {initialTemperature !== undefined ? initialTemperature : "Not Set"}
      </Text>
      <Text style={{ marginBottom: "2ch" }}>
        <strong>Max Tokens:</strong>{" "}
        {initialMaxTokens !== undefined ? initialMaxTokens : "Not Set"}
      </Text>
      <TextInput
        label="New Conversation Name"
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

      <Group
        style={{ marginTop: "20px", display: "flex", justifyContent: "center" }}
      >
        <Button onClick={handleSubmit}>Update</Button>

        <Button color="red" onClick={() => setConfirmDelete(!confirmDelete)}>
          {confirmDelete ? "Cancel" : "Delete"}
        </Button>
      </Group>

      {confirmDelete && (
        <Button
          fullWidth
          color="red"
          style={{ marginTop: "10px" }}
          onClick={handleDelete}
        >
          Confirm and Delete
        </Button>
      )}
    </Modal>
  );
};

export default ConfigureModal;
