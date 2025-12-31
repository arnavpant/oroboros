"use client"

import { motion, AnimatePresence } from "framer-motion"
import { Shield, CheckCircle, AlertTriangle } from "lucide-react"
import type { SystemState, Immunity } from "../soc-dashboard"

interface ThreatMatrixProps {
  immunities: Immunity[]
  systemState: SystemState
}

export function ThreatMatrix({ immunities, systemState }: ThreatMatrixProps) {
  return (
    <div className="h-full border border-border rounded-lg bg-card/30 backdrop-blur-sm flex flex-col overflow-hidden border-glow-cyan">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border flex items-center justify-between bg-card/50">
        <div className="flex items-center gap-2">
          <Shield className="w-4 h-4 text-primary" />
          <span className="text-sm font-bold tracking-wider text-primary">THREAT MATRIX</span>
        </div>
        <span className="text-xs text-muted-foreground tracking-wider">LEARNED IMMUNITIES: {immunities.length}</span>
      </div>

      {/* Content */}
      <div className="flex-1 p-4 overflow-y-auto">
        {immunities.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-muted-foreground">
            <motion.div
              animate={{ opacity: [0.3, 0.6, 0.3] }}
              transition={{ duration: 3, repeat: Number.POSITIVE_INFINITY }}
            >
              <AlertTriangle className="w-16 h-16 mb-4 text-border" />
            </motion.div>
            <p className="text-sm tracking-wider">NO IMMUNITIES ACQUIRED</p>
            <p className="text-xs mt-2">System awaiting threat exposure for learning</p>
          </div>
        ) : (
          <div className="space-y-3">
            <AnimatePresence>
              {immunities.map((immunity, index) => (
                <motion.div
                  key={immunity.id}
                  initial={{
                    opacity: 0,
                    scale: 0.8,
                    x: -50,
                    filter: "blur(10px)",
                  }}
                  animate={{
                    opacity: 1,
                    scale: 1,
                    x: 0,
                    filter: "blur(0px)",
                  }}
                  transition={{
                    type: "spring",
                    damping: 15,
                    delay: index * 0.1,
                  }}
                  className="relative"
                >
                  {/* Glitch effect on entry */}
                  <motion.div
                    initial={{ opacity: 1 }}
                    animate={{ opacity: 0 }}
                    transition={{ duration: 0.5 }}
                    className="absolute inset-0 bg-[#00ff00]/20 animate-glitch pointer-events-none"
                  />

                  <div className="border border-[#00ff00]/50 bg-[#00ff00]/5 rounded p-4 border-glow-green">
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          transition={{ delay: 0.3, type: "spring" }}
                        >
                          <CheckCircle className="w-6 h-6 text-[#00ff00]" />
                        </motion.div>
                        <div>
                          <p className="text-sm font-bold text-[#00ff00] tracking-wider text-glow-green">
                            [ACTIVE] {immunity.name}
                          </p>
                          <p className="text-xs text-muted-foreground mt-1">Type: {immunity.type}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-muted-foreground">Recovery Time</p>
                        <p className="text-sm font-bold text-primary tabular-nums">{immunity.recoveryTime}ms</p>
                      </div>
                    </div>
                    <div className="mt-3 pt-3 border-t border-[#00ff00]/20">
                      <p className="text-xs text-muted-foreground">Acquired: {immunity.timestamp.toLocaleString()}</p>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  )
}
