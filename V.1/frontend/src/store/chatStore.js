import { create } from "zustand";
import axios from "axios";

const useChatStore = create((set, get) => ({
  messages: [],
  loading: false,

  sendMessage: async (userText) => {
    if (!userText.trim()) return;

    // push user message once
    set((state) => ({
      messages: [...state.messages, { role: "user", text: userText }],
      loading: true,
    }));

    try {
      const res = await axios.post("http://127.0.0.1:8000/api/chat", {
        message: userText,
      });
      const reply = res.data.response || "[No response]";

      // append only the AI reply now
      set((state) => ({
        messages: [...state.messages, { role: "goku", text: reply }],
        loading: false,
      }));
    } catch (err) {
      set((state) => ({
        messages: [
          ...state.messages,
          { role: "goku", text: `[Error] ${err.message}` },
        ],
        loading: false,
      }));
    }
  },

  clearChat: () => set({ messages: [] }),
}));

export default useChatStore;
