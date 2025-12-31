"use client"

import { motion } from "framer-motion"
import { Activity, Clock, RefreshCw, Zap } from "lucide-react"
import type { SystemState } from "../soc-dashboard"
import { Sparkline } from "./sparkline"

interface ForensicsPanelProps {
  mttr: number
  lazarusCount: number
  tokenVelocity: number[]
  systemState: SystemState
}

export function ForensicsPanel({ mttr, lazarusCount, tokenVelocity, systemState }: ForensicsPanelProps) {
  return (
    <div className="h-full border border-border rounded-lg bg-card/30 backdrop-blur-sm flex flex-col overflow-hidden border-glow-cyan">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border flex items-center gap-2 bg-card/50">
        <Activity className="w-4 h-4 text-primary" />
        <span className="text-sm font-bold tracking-wider text-primary">FORENSICS</span>
      </div>

      {/* Stats */}
      <div className="flex-1 p-4 space-y-4">
        {/* MTTR */}
        <div className="border border-border rounded p-4 bg-card/30">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-muted-foreground" />
              <span className="text-xs text-muted-foreground tracking-wider">MTTR</span>
            </div>
            <span className="text-xs text-muted-foreground">Mean Time to Recovery</span>
          </div>
          <motion.p
            className="text-3xl font-bold text-primary text-glow-cyan tabular-nums"
            key={mttr}
            initial={{ scale: 1.2, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
          >
            {mttr > 0 ? `${mttr}ms` : "---"}
          </motion.p>
        </div>

        {/* Lazarus Count */}
        <div className="border border-border rounded p-4 bg-card/30">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4 text-muted-foreground" />
              <span className="text-xs text-muted-foreground tracking-wider">LAZARUS COUNT</span>
            </div>
            <span className="text-xs text-muted-foreground">Total Resurrections</span>
          </div>
          <motion.p
            className="text-3xl font-bold text-[#00ff00] text-glow-green tabular-nums"
            key={lazarusCount}
            initial={{ scale: 1.5 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", damping: 10 }}
          >
            {lazarusCount}
          </motion.p>
        </div>

        {/* Token Velocity */}
        <div className="border border-border rounded p-4 bg-card/30 flex-1">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-muted-foreground" />
              <span className="text-xs text-muted-foreground tracking-wider">TOKEN VELOCITY</span>
            </div>
            <span className={`text-xs font-bold ${systemState === "CRASH" ? "text-[#ff0040]" : "text-[#00ff00]"}`}>
              {systemState === "CRASH" ? "FLATLINE" : "ACTIVE"}
            </span>
          </div>
          <div className="h-24">
            <Sparkline data={tokenVelocity} color={systemState === "CRASH" ? "#ff0040" : "#00ffff"} />
          </div>
        </div>

        {/* System Uptime */}
        <div className="border border-border rounded p-3 bg-card/30">
          <div className="flex items-center justify-between">
            <span className="text-xs text-muted-foreground tracking-wider">SYSTEM INTEGRITY</span>
            <span className={`text-sm font-bold ${systemState === "CRASH" ? "text-[#ff0040]" : "text-[#00ff00]"}`}>
              {systemState === "CRASH" ? "0%" : systemState === "HEALING" ? "47%" : "100%"}
            </span>
          </div>
          <div className="mt-2 h-2 bg-border rounded-full overflow-hidden">
            <motion.div
              className={`h-full ${
                systemState === "CRASH" ? "bg-[#ff0040]" : systemState === "HEALING" ? "bg-[#ffaa00]" : "bg-[#00ff00]"
              }`}
              initial={false}
              animate={{
                width: systemState === "CRASH" ? "0%" : systemState === "HEALING" ? "47%" : "100%",
              }}
              transition={{ duration: 0.5 }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
