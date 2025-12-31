"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Shield, Zap } from "lucide-react"
import type { SystemState } from "../soc-dashboard"

interface HeaderProps {
  systemState: SystemState
  onTriggerCrash: () => void
}

export function Header({ systemState, onTriggerCrash }: HeaderProps) {
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(interval)
  }, [])

  const getStatusConfig = () => {
    switch (systemState) {
      case "CRASH":
        return { label: "CRITICAL FAILURE", color: "text-[#ff0040]", glow: "text-glow-red", pulse: true }
      case "HEALING":
        return { label: "SELF-REPAIR ACTIVE", color: "text-[#ffaa00]", glow: "", pulse: true }
      case "EVOLVED":
        return { label: "RECOVERY COMPLETE", color: "text-[#00ff00]", glow: "text-glow-green", pulse: false }
      default:
        return { label: "NOMINAL", color: "text-[#00ff00]", glow: "text-glow-green", pulse: true }
    }
  }

  const status = getStatusConfig()

  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="flex items-center justify-between px-6 py-4">
        {/* Logo & Title */}
        <div className="flex items-center gap-4">
          <motion.div
            animate={{ rotate: systemState === "IDLE" ? 360 : 0 }}
            transition={{ duration: 20, repeat: Number.POSITIVE_INFINITY, ease: "linear" }}
          >
            <Shield className="w-8 h-8 text-primary" />
          </motion.div>
          <div>
            <h1 className="text-xl font-bold tracking-wider text-primary text-glow-cyan">
              OUROBOROS // ACTIVE DEFENSE CONSOLE
            </h1>
            <p className="text-xs text-muted-foreground tracking-widest">AI SECURITY OPERATIONS CENTER</p>
          </div>
        </div>

        {/* Center - Demo Trigger */}
        <motion.button
          onClick={onTriggerCrash}
          disabled={systemState !== "IDLE"}
          className="px-4 py-2 bg-[#ff0040]/20 border border-[#ff0040]/50 text-[#ff0040] text-sm 
                     tracking-wider hover:bg-[#ff0040]/30 transition-colors disabled:opacity-30 
                     disabled:cursor-not-allowed flex items-center gap-2"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Zap className="w-4 h-4" />
          SIMULATE ATTACK
        </motion.button>

        {/* Right - Status & Clock */}
        <div className="flex items-center gap-8">
          {/* System Status */}
          <div className="flex items-center gap-3">
            <span className="text-xs text-muted-foreground tracking-wider">SYSTEM STATUS:</span>
            <div className="flex items-center gap-2">
              <motion.div
                className={`w-2 h-2 rounded-full ${
                  systemState === "CRASH" ? "bg-[#ff0040]" : systemState === "HEALING" ? "bg-[#ffaa00]" : "bg-[#00ff00]"
                }`}
                animate={status.pulse ? { opacity: [1, 0.3, 1] } : {}}
                transition={{ duration: 1, repeat: Number.POSITIVE_INFINITY }}
              />
              <span className={`text-sm font-bold tracking-wider ${status.color} ${status.glow}`}>{status.label}</span>
            </div>
          </div>

          {/* UTC Clock */}
          <div className="text-right">
            <p className="text-xs text-muted-foreground tracking-wider">UTC TIME</p>
            <p className="text-lg font-bold text-primary text-glow-cyan tabular-nums">
              {time.toUTCString().split(" ")[4]}
            </p>
          </div>
        </div>
      </div>
    </header>
  )
}
