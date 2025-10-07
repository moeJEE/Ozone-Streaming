import { NextResponse } from 'next/server';

export async function GET() {
  // Mock metrics data - in production, this would fetch from your API
  const metrics = [
    { timestamp: '2024-01-01T00:00:00Z', value: 120, category: 'A' },
    { timestamp: '2024-01-01T01:00:00Z', value: 135, category: 'A' },
    { timestamp: '2024-01-01T02:00:00Z', value: 98, category: 'B' },
    { timestamp: '2024-01-01T03:00:00Z', value: 156, category: 'A' },
    { timestamp: '2024-01-01T04:00:00Z', value: 142, category: 'B' },
    { timestamp: '2024-01-01T05:00:00Z', value: 178, category: 'A' },
  ];

  return NextResponse.json(metrics);
}
