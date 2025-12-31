"use client"

import { useEffect, useRef } from "react"
import { motion } from "framer-motion"
import { Brain, Terminal } from "lucide-react"
import type { SystemState, ThoughtMessage } from "../soc-dashboard"
import { TypewriterText } from "./typewriter-text"

interface ThoughtStreamProps {
  thoughts: ThoughtMessage[]
  systemState: SystemState
}

export function ThoughtStream({ thoughts, systemState }: ThoughtStreamProps) {
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [thoughts])

  const getTypeColor = (type: ThoughtMessage["type"]) => {
    switch (type) {
      case "error":
        return "text-[#ff0040]"
      case "warning":
        return "text-[#ffaa00]"
      case "success":
        return "text-[#00ff00]"
      default:
        return "text-primary"
    }
  }

  return (
    <div
      className={`h-full border rounded-lg bg-card/30 backdrop-blur-sm flex flex-col overflow-hidden transition-all duration-300 ${
        systemState === "CRASH" ? "border-[#ff0040] border-glow-red" : "border-border border-glow-cyan"
      }`}
    >
      {/* Header */}
      <div className="px-4 py-3 border-b border-border flex items-center gap-2 bg-card/50">
        <Brain className="w-4 h-4 text-primary" />
        <span className="text-sm font-bold tracking-wider text-primary">THE MIND</span>
        <Terminal className="w-3 h-3 text-muted-foreground ml-auto" />
      </div>

      {/* Terminal Content */}
      <div
        ref={scrollRef}
        className={`flex-1 overflow-y-auto p-4 font-mono text-xs space-y-2 ${
          systemState === "CRASH" ? "bg-[#ff0040]/5" : ""
        }`}
      >
        {thoughts.map((thought, index) => (
          <motion.div
            key={thought.id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className={`flex gap-2 ${getTypeColor(thought.type)}`}
          >
            <span className="text-muted-foreground shrink-0">[{thought.timestamp.toLocaleTimeString()}]</span>
            <span className="text-muted-foreground">{">"}</span>
            {index === thoughts.length - 1 ? <TypewriterText text={thought.content} /> : <span>{thought.content}</span>}
          </motion.div>
        ))}

        {/* Cursor */}
        <div className="flex items-center gap-2 text-primary">
          <span className="text-muted-foreground">{">"}</span>
          <motion.span
            animate={{ opacity: [1, 0] }}
            transition={{ duration: 0.8, repeat: Number.POSITIVE_INFINITY }}
            className="w-2 h-4 bg-primary"
          />
        </div>
      </div>
    </div>
  )
}
