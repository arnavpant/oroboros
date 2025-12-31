"use client"

import { useMemo } from "react"
import { motion } from "framer-motion"

interface SparklineProps {
  data: number[]
  color: string
}

export function Sparkline({ data, color }: SparklineProps) {
  const path = useMemo(() => {
    if (data.length === 0) return ""

    const max = Math.max(...data, 1)
    const min = Math.min(...data, 0)
    const range = max - min || 1

    const width = 100
    const height = 100
    const step = width / Math.max(data.length - 1, 1)

    const points = data.map((value, index) => {
      const x = index * step
      const y = height - ((value - min) / range) * height
      return `${x},${y}`
    })

    return `M ${points.join(" L ")}`
  }, [data])

  const areaPath = useMemo(() => {
    if (data.length === 0) return ""
    return `${path} L 100,100 L 0,100 Z`
  }, [path, data.length])

  return (
    <svg viewBox="0 0 100 100" className="w-full h-full" preserveAspectRatio="none">
      {/* Gradient fill */}
      <defs>
        <linearGradient id={`gradient-${color}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor={color} stopOpacity="0.3" />
          <stop offset="100%" stopColor={color} stopOpacity="0" />
        </linearGradient>
      </defs>

      {/* Area fill */}
      <motion.path d={areaPath} fill={`url(#gradient-${color})`} initial={{ opacity: 0 }} animate={{ opacity: 1 }} />

      {/* Line */}
      <motion.path
        d={path}
        fill="none"
        stroke={color}
        strokeWidth="2"
        vectorEffect="non-scaling-stroke"
        initial={{ pathLength: 0 }}
        animate={{ pathLength: 1 }}
        transition={{ duration: 0.5 }}
        style={{
          filter: `drop-shadow(0 0 4px ${color})`,
        }}
      />

      {/* Current point */}
      {data.length > 0 && (
        <motion.circle
          cx={100}
          cy={100 - ((data[data.length - 1] - Math.min(...data)) / (Math.max(...data) - Math.min(...data) || 1)) * 100}
          r="3"
          fill={color}
          animate={{ opacity: [1, 0.5, 1] }}
          transition={{ duration: 1, repeat: Number.POSITIVE_INFINITY }}
          style={{
            filter: `drop-shadow(0 0 6px ${color})`,
          }}
        />
      )}
    </svg>
  )
}
