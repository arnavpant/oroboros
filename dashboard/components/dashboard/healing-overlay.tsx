"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { Cpu, Loader2 } from "lucide-react"

export function HealingOverlay() {
  const [progress, setProgress] = useState(0)
  const [phase, setPhase] = useState<"analyzing" | "injecting">("analyzing")

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 2
      })
    }, 100)

    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (progress >= 50) {
      setPhase("injecting")
    }
  }, [progress])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-30 bg-background/80 backdrop-blur-sm flex items-center justify-center"
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        className="bg-card border border-[#ffaa00]/50 rounded-lg p-8 max-w-md w-full mx-4 border-glow-cyan"
      >
        <div className="flex items-center gap-4 mb-6">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Number.POSITIVE_INFINITY, ease: "linear" }}
          >
            <Cpu className="w-10 h-10 text-[#ffaa00]" />
          </motion.div>
          <div>
            <h2 className="text-lg font-bold text-[#ffaa00] tracking-wider">SELF-REPAIR PROTOCOL</h2>
            <p className="text-xs text-muted-foreground">Autonomous remediation in progress</p>
          </div>
        </div>

        {/* Progress bar */}
        <div className="space-y-2 mb-6">
          <div className="flex justify-between text-xs">
            <span className="text-muted-foreground">
              {phase === "analyzing" ? "ANALYZING ERROR PATTERN..." : "INJECTING REMEDIATION..."}
            </span>
            <span className="text-[#ffaa00] tabular-nums">{progress}%</span>
          </div>
          <div className="h-3 bg-border rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-linear-to-r from-[#ffaa00] to-[#00ff00]"
              style={{ width: `${progress}%` }}
              transition={{ duration: 0.1 }}
            />
          </div>
        </div>

        {/* Status messages */}
        <div className="space-y-2 font-mono text-xs">
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-2 text-[#00ff00]"
          >
            <span>✓</span>
            <span>Error signature captured</span>
          </motion.div>
          {progress >= 30 && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2 text-[#00ff00]"
            >
              <span>✓</span>
              <span>Pattern analysis complete</span>
            </motion.div>
          )}
          {progress >= 60 && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2 text-[#00ff00]"
            >
              <span>✓</span>
              <span>Remediation strategy generated</span>
            </motion.div>
          )}
          {progress >= 90 && (
            <motion.div
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-2 text-[#ffaa00]"
            >
              <Loader2 className="w-3 h-3 animate-spin" />
              <span>Integrating immunity...</span>
            </motion.div>
          )}
        </div>
      </motion.div>
    </motion.div>
  )
}
