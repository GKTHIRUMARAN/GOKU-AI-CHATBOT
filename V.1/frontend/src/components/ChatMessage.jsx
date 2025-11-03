import { motion } from "framer-motion";
import clsx from "clsx";

export default function ChatMessage({ role, text }) {
  const isUser = role === "user";
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={clsx(
        "my-2 flex",
        isUser ? "justify-end" : "justify-start"
      )}
    >
      <div
        className={clsx(
          "max-w-[80%] rounded-2xl px-4 py-2 text-sm shadow-md whitespace-pre-wrap",
          isUser
            ? "bg-slate-700 text-slate-50 self-end"
            : "bg-orange-500/20 border border-orange-400 text-orange-100"
        )}
      >
        {text}
      </div>
    </motion.div>
  );
}
