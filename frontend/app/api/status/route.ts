import { NextResponse } from 'next/server';

export async function GET() {
  // Mock system status - in production, this would check actual service health
  const status = {
    kafka: 'healthy' as const,
    spark: 'healthy' as const,
    postgres: 'healthy' as const,
    airflow: 'healthy' as const,
  };

  return NextResponse.json(status);
}
