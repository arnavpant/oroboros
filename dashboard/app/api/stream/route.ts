// app/api/stream/route.ts
import { Kafka } from 'kafkajs';
import { NextRequest } from 'next/server';

// Initialize Kafka Client
const kafka = new Kafka({
  clientId: 'dashboard-ui',
  brokers: [process.env.KAFKA_BOOTSTRAP_SERVER!],
  ssl: true,
  sasl: {
    mechanism: 'plain',
    username: process.env.KAFKA_API_KEY!,
    password: process.env.KAFKA_API_SECRET!,
  },
});

// Unique group ID so every tab gets its own stream
const consumer = kafka.consumer({ groupId: 'dashboard-group-' + Date.now() });

export async function GET(req: NextRequest) {
  const stream = new TransformStream();
  const writer = stream.writable.getWriter();
  const encoder = new TextEncoder();

  // Start fetching in the background
  (async () => {
    try {
      await consumer.connect();
      await consumer.subscribe({ topic: process.env.KAFKA_TOPIC_THOUGHTS!, fromBeginning: false });

      await consumer.run({
        eachMessage: async ({ message }) => {
          const value = message.value?.toString();
          if (value) {
            // Send data to browser as Server-Sent Event (SSE)
            await writer.write(encoder.encode(`data: ${value}\n\n`));
          }
        },
      });
    } catch (error) {
      console.error("Kafka Error:", error);
      await writer.write(encoder.encode(`event: error\ndata: ${JSON.stringify(error)}\n\n`));
    }
  })();

  return new Response(stream.readable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}