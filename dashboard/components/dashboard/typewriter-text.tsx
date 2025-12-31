"use client"

import { useState, useEffect } from "react"

interface TypewriterTextProps {
  text: string
  speed?: number
}

export function TypewriterText({ text, speed = 30 }: TypewriterTextProps) {
  const [displayText, setDisplayText] = useState("")

  useEffect(() => {
    let index = 0
    setDisplayText("")

    const interval = setInterval(() => {
      if (index < text.length) {
        setDisplayText(text.slice(0, index + 1))
        index++
      } else {
        clearInterval(interval)
      }
    }, speed)

    return () => clearInterval(interval)
  }, [text, speed])

  return <span>{displayText}</span>
}
