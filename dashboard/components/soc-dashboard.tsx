"use client"

import { useState, useEffect, useCallback } from "react"
import { AnimatePresence } from "framer-motion"
import { Header } from "./dashboard/header"
import { ThoughtStream } from "./dashboard/thought-stream"
import { ThreatMatrix } from "./dashboard/threat-matrix"
import { ForensicsPanel } from "./dashboard/forensics-panel"
import { CriticalBanner } from "./dashboard/critical-banner"
import { HealingOverlay } from "./dashboard/healing-overlay"

export type SystemState = "IDLE" | "CRASH" | "HEALING" | "EVOLVED"

export interface Immunity {
  id: string
  name: string
  type: string
  timestamp: Date
  recoveryTime: number
}

export interface ThoughtMessage {
  id: string
  content: string
  timestamp: Date
  type: "info" | "warning" | "error" | "success"
}

export function SOCDashboard() {
  const [systemState, setSystemState] = useState<SystemState>("IDLE")
  const [immunities, setImmunities] = useState<Immunity[]>([])
  const [thoughts, setThoughts] = useState<ThoughtMessage[]>([])
  const [lazarusCount, setLazarusCount] = useState(0)
  const [mttr, setMttr] = useState(0)
  const [tokenVelocity, setTokenVelocity] = useState<number[]>([])
  const [crashTimestamp, setCrashTimestamp] = useState<Date | null>(null)

  // Add thought to stream
  const addThought = useCallback((content: string, type: ThoughtMessage["type"] = "info") => {
    const thought: ThoughtMessage = {
      id: crypto.randomUUID(),
      content,
      timestamp: new Date(),
      type,
    }
    setThoughts((prev) => [...prev.slice(-50), thought])
  }, [])

  // Simulate token velocity
  useEffect(() => {
    const interval = setInterval(() => {
      setTokenVelocity((prev) => {
        const newValue = systemState === "CRASH" ? 0 : Math.random() * 100 + 50
        return [...prev.slice(-30), newValue]
      })
    }, 500)
    return () => clearInterval(interval)
  }, [systemState])

  // Idle state thoughts
  useEffect(() => {
    if (systemState !== "IDLE") return

    const thoughts_list = [
      "Monitoring system health metrics...",
      "Scanning for anomalous patterns...",
      "Neural pathway integrity: OPTIMAL",
      "Memory allocation stable at 67%",
      "Processing incoming data streams...",
      "All subsystems operating within parameters",
      "Threat detection algorithms active",
      "Performing routine integrity check...",
    ]

    const interval = setInterval(() => {
      const randomThought = thoughts_list[Math.floor(Math.random() * thoughts_list.length)]
      addThought(randomThought, "info")
    }, 2000)

    return () => clearInterval(interval)
  }, [systemState, addThought])

  // Trigger crash simulation
  const triggerCrash = useCallback(() => {
    if (systemState !== "IDLE") return

    setSystemState("CRASH")
    setCrashTimestamp(new Date())
    addThought("CRITICAL: Memory buffer overflow detected!", "error")
    addThought("ALERT: System integrity compromised", "error")
    addThought("ERROR: Unable to allocate memory block 0xFFFA2B", "error")

    // After 3 seconds, start healing
    setTimeout(() => {
      setSystemState("HEALING")
      addThought("Initiating self-repair protocol...", "warning")
      addThought("Analyzing error pattern signature...", "warning")

      setTimeout(() => {
        addThought("Pattern identified: Memory Buffer Overflow", "warning")
        addThought("Generating remediation strategy...", "warning")
      }, 1500)

      setTimeout(() => {
        addThought("Injecting remediation into runtime...", "success")
      }, 3000)

      // Complete healing after 5 seconds
      setTimeout(() => {
        const recoveryTime = Date.now() - (crashTimestamp?.getTime() || Date.now())
        const newImmunity: Immunity = {
          id: crypto.randomUUID(),
          name: "Memory Buffer Overflow",
          type: "MEMORY_PROTECTION",
          timestamp: new Date(),
          recoveryTime: recoveryTime || 420,
        }

        setImmunities((prev) => [...prev, newImmunity])
        setLazarusCount((prev) => prev + 1)
        setMttr(recoveryTime || 420)
        setSystemState("EVOLVED")
        addThought("IMMUNITY ACQUIRED: Memory Buffer Overflow", "success")
        addThought("System evolved. New defense pattern integrated.", "success")

        // Return to idle after showing evolved state
        setTimeout(() => {
          setSystemState("IDLE")
          addThought("Returning to nominal operations...", "info")
        }, 3000)
      }, 5000)
    }, 3000)
  }, [systemState, addThought, crashTimestamp])

  return (
    <div className="min-h-screen bg-background text-foreground font-mono relative overflow-hidden">
      {/* Scanline effect */}
      <div className="pointer-events-none fixed inset-0 z-50 opacity-5">
        <div className="h-1 w-full bg-primary animate-scanline" />
      </div>

      {/* Critical failure banner */}
      <AnimatePresence>{systemState === "CRASH" && <CriticalBanner />}</AnimatePresence>

      {/* Healing overlay */}
      <AnimatePresence>{systemState === "HEALING" && <HealingOverlay />}</AnimatePresence>

      <div className="relative z-10">
        <Header systemState={systemState} onTriggerCrash={triggerCrash} />

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4 p-4 h-[calc(100vh-80px)]">
          {/* Left sidebar - Thought Stream */}
          <div className="lg:col-span-1">
            <ThoughtStream thoughts={thoughts} systemState={systemState} />
          </div>

          {/* Center - Threat Matrix */}
          <div className="lg:col-span-2">
            <ThreatMatrix immunities={immunities} systemState={systemState} />
          </div>

          {/* Right sidebar - Forensics */}
          <div className="lg:col-span-1">
            <ForensicsPanel
              mttr={mttr}
              lazarusCount={lazarusCount}
              tokenVelocity={tokenVelocity}
              systemState={systemState}
            />
          </div>
        </div>
      </div>
    </div>
  )
}
