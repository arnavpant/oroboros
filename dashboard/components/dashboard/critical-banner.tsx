"use client"

import { motion } from "framer-motion"
import { AlertTriangle, XCircle } from "lucide-react"

export function CriticalBanner() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -100 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -100 }}
      className="fixed inset-x-0 top-0 z-40 bg-[#ff0040] py-4"
    >
      <motion.div
        animate={{ opacity: [1, 0.7, 1] }}
        transition={{ duration: 0.5, repeat: Number.POSITIVE_INFINITY }}
        className="container mx-auto flex items-center justify-center gap-4"
      >
        <motion.div
          animate={{ rotate: [0, 10, -10, 0] }}
          transition={{ duration: 0.3, repeat: Number.POSITIVE_INFINITY }}
        >
          <AlertTriangle className="w-8 h-8 text-white" />
        </motion.div>
        <div className="flex items-center gap-3">
          <XCircle className="w-6 h-6 text-white" />
          <span className="text-xl font-bold text-white tracking-widest animate-glitch">
            CRITICAL FAILURE: MEMORY_OVERFLOW
          </span>
          <XCircle className="w-6 h-6 text-white" />
        </div>
        <motion.div
          animate={{ rotate: [0, -10, 10, 0] }}
          transition={{ duration: 0.3, repeat: Number.POSITIVE_INFINITY }}
        >
          <AlertTriangle className="w-8 h-8 text-white" />
        </motion.div>
      </motion.div>

      {/* Glitch overlay */}
      <motion.div
        className="absolute inset-0 bg-white/10"
        animate={{ opacity: [0, 0.2, 0] }}
        transition={{ duration: 0.1, repeat: Number.POSITIVE_INFINITY, repeatDelay: 0.5 }}
      />
    </motion.div>
  )
}
